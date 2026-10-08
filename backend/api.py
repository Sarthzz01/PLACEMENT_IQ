import sys
import os
import json
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure backend root is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from src.config import DB_PATH, OUTPUT_DIR, BASE_NUMERIC, DISPLAY_NAMES
from src.preprocessing import load_data, get_dataset_counts, validate_dataset
from src.database import (
    init_database, authenticate_user, register_user, hash_password,
    get_student_profile, save_student_profile,
    log_prediction_to_db, get_student_prediction_history, save_admin_feedback,
    get_student_feedback, get_all_student_profiles_df,
    get_system_setting, set_system_setting, log_olap_query, get_olap_history
)
from src.prediction import predict_placement, get_production_model_name, batch_predict, MODEL_FILENAME_MAP
from src.recommendations import generate_recommendations
from src.warehouse import (
    build_warehouse, get_warehouse_summary, get_sample_records,
    query as run_sql, STAR_SCHEMA_DEF, RELATIONSHIPS
)
from src.olap import (
    slice_op, dice_op, rollup_2d, drilldown_2d, pivot_op, drill_across
)
from src.classification import train_models
from src.regression import train_regression
from src.clustering import kmeans, elbow, agglomerative, dendrogram_data
from src.data_mining import correlation, mutual_information, feature_importance, association_insights
from src.profile_fetcher import fetch_external_profile_stats

init_database()

DIMENSIONS = [
    "branch", "gender", "placement_training", "placement_status",
    "cgpa_band", "aptitude_band", "attendance_band", "coding_band",
    "internship_band", "projects_band", "backlog_band", "data_source"
]

MEASURES = [
    "cgpa", "attendance_percentage", "dsa_questions_solved",
    "leetcode_questions_solved", "hackerrank_questions_solved",
    "internships_count", "projects_count", "hackathons_count",
    "certifications_count", "aptitude_score", "communication_score",
    "coding_skill_score", "github_repos", "mock_interview_score",
    "placement_prediction"
]

AGG_FUNCS = ["Average", "Sum", "Count", "Min", "Max", "Median"]

app = FastAPI(
    title="PLACEMENT IQ — API Engine",
    description="REST backend for Student Placement Analytics, Data Warehousing, and Machine Learning Suite",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "PLACEMENT IQ API Engine",
        "version": "2.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

# -------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------
class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None
    bypass_password: Optional[bool] = False

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    branch: Optional[str] = "CSE"
    role: Optional[str] = "Student"

class ProfileUpdateRequest(BaseModel):
    email: str
    data: Dict[str, Any]

class FetchExternalStatsRequest(BaseModel):
    github_url: Optional[str] = ""
    leetcode_url: Optional[str] = ""
    hackerrank_url: Optional[str] = ""

class PredictRequest(BaseModel):
    email: Optional[str] = None
    data: Dict[str, Any]
    model_name: Optional[str] = None

class FeedbackRequest(BaseModel):
    student_email: str
    admin_name: str
    status: str
    notes: str

class SQLQueryRequest(BaseModel):
    sql: str

class OLAPQueryRequest(BaseModel):
    operation: str
    dimension: Optional[str] = None
    row_dim: Optional[str] = None
    col_dim: Optional[str] = None
    slice_value: Optional[Any] = None
    measure: str = "cgpa"
    agg_func: str = "mean"
    filters: Optional[Dict[str, Any]] = None
    dice_conditions: Optional[Dict[str, Any]] = None
    measures: Optional[List[str]] = None

class SettingRequest(BaseModel):
    key: str
    value: str

class ClassificationTrainRequest(BaseModel):
    test_size: Optional[float] = 0.2
    random_state: Optional[int] = 42
    dt_depth: Optional[int] = 6
    rf_estimators: Optional[int] = 150
    rf_depth: Optional[int] = 10
    gb_estimators: Optional[int] = 100
    gb_depth: Optional[int] = 3
    gb_learning_rate: Optional[float] = 0.1
    lr_max_iter: Optional[int] = 1000
    lr_C: Optional[float] = 1.0

# -------------------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------------------
@app.post("/api/auth/login")
def login(req: LoginRequest):
    user = authenticate_user(req.email.strip().lower(), req.password, bypass_password=req.bypass_password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {
        "status": "success",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": "Admin" if user["role"].lower() == "admin" else "Student",
            "student_id": user.get("student_id", "")
        }
    }

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    success, msg, user = register_user(
        name=req.name.strip(),
        email=req.email.strip().lower(),
        password=req.password,
        branch=req.branch or "CSE"
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    user_data = authenticate_user(req.email.strip().lower(), req.password)
    return {
        "status": "success",
        "message": msg,
        "user": {
            "id": user_data["id"],
            "name": user_data["name"],
            "email": user_data["email"],
            "role": "Student",
            "student_id": user_data.get("student_id", "")
        }
    }

def normalize_student_features(d: Dict[str, Any]) -> Dict[str, Any]:
    norm = dict(d)
    alias_map = {
        "dsa_problems_solved": "dsa_questions_solved",
        "leetcode_problems_solved": "leetcode_questions_solved",
        "hackerrank_score": "hackerrank_questions_solved",
        "internships_completed": "internships_count",
        "hackathons_participated": "hackathons_count",
        "github_repos_count": "github_repos",
        "placement_training_enrolled": "placement_training"
    }
    for old_k, new_k in alias_map.items():
        if old_k in norm and new_k not in norm:
            val = norm[old_k]
            if new_k == "placement_training" and isinstance(val, (int, bool)):
                norm[new_k] = "Yes" if val else "No"
            else:
                norm[new_k] = val
        elif new_k in norm and old_k not in norm:
            norm[old_k] = norm[new_k]
    return norm

# -------------------------------------------------------------
# STUDENT PORTAL ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/student/dashboard/{email}")
def student_dashboard(email: str):
    email = email.strip().lower()
    profile = get_student_profile(email) or {}
    preds_df = get_student_prediction_history(email)
    preds = preds_df.to_dict(orient="records") if len(preds_df) > 0 else []
    feedback_df = get_student_feedback(email)
    feedback = feedback_df.to_dict(orient="records") if len(feedback_df) > 0 else []
    
    df = load_data()
    def get_pct(col, val):
        if col in df.columns and len(df) > 0:
            try:
                v = float(val)
                return round(float((df[col] <= v).mean() * 100), 1)
            except Exception:
                return 50.0
        return 50.0

    kpis = {
        "cgpa": float(profile.get("cgpa", 0.0) or 0.0),
        "cgpa_pct": get_pct("cgpa", profile.get("cgpa", 0.0) or 0.0),
        "dsa": int(profile.get("dsa_questions_solved", 0) or 0),
        "dsa_pct": get_pct("dsa_questions_solved", profile.get("dsa_questions_solved", 0) or 0),
        "aptitude": float(profile.get("aptitude_score", 0.0) or 0.0),
        "aptitude_pct": get_pct("aptitude_score", profile.get("aptitude_score", 0.0) or 0.0),
        "coding": float(profile.get("coding_skill_score", 0.0) or 0.0),
        "coding_pct": get_pct("coding_skill_score", profile.get("coding_skill_score", 0.0) or 0.0)
    }
    
    check_fields = ["cgpa", "attendance_percentage", "dsa_questions_solved", "aptitude_score", "coding_skill_score", "internships_count", "projects_count"]
    filled = sum(1 for f in check_fields if profile.get(f) is not None and profile.get(f) != 0)
    completeness = int(round((filled / len(check_fields)) * 100))

    cgpa_val = float(profile.get("cgpa", 0.0) or 0.0)
    apt_val = float(profile.get("aptitude_score", 0.0) or 0.0)
    cod_val = float(profile.get("coding_skill_score", 0.0) or 0.0)
    skill_score = int(round((cgpa_val * 4.0) + (apt_val * 0.3) + (cod_val * 3.0)))
    skill_score = max(10, min(99, skill_score)) if (cgpa_val > 0 or apt_val > 0) else 65

    latest_pred = preds[0] if preds else None
    
    return {
        "profile": profile,
        "kpis": kpis,
        "completeness": completeness,
        "skill_score": skill_score,
        "latest_prediction": latest_pred,
        "feedback": feedback
    }

@app.get("/api/student/profile/{email}")
def student_profile_get(email: str):
    email = email.strip().lower()
    profile = get_student_profile(email) or {}
    return {"profile": profile}

@app.post("/api/student/profile")
def student_profile_save(req: ProfileUpdateRequest):
    payload = normalize_student_features(req.data)
    payload["email"] = req.email.strip().lower()
    save_student_profile(payload)
    return {"status": "success", "message": "Profile updated successfully."}

@app.post("/api/student/fetch-external-stats")
def api_fetch_external_stats(req: FetchExternalStatsRequest):
    result = fetch_external_profile_stats(
        github_url=req.github_url or "",
        leetcode_url=req.leetcode_url or "",
        hackerrank_url=req.hackerrank_url or ""
    )
    return result

@app.post("/api/student/predict")
def student_predict(req: PredictRequest):
    norm_data = normalize_student_features(req.data)
    result = predict_placement(norm_data, model_name=req.model_name)
    if req.email:
        email = req.email.strip().lower()
        profile = get_student_profile(email) or {}
        sid = profile.get("student_id", f"STU-{abs(hash(email)) % 90000 + 10000}")
        log_prediction_to_db(
            student_id=sid,
            email=email,
            status=result.get("status", "Not Placed"),
            prob=result.get("probability", 0.0),
            model_name=result.get("model_name", req.model_name or "Random Forest"),
            features=norm_data,
            evaluated_by="Student Self-Assessment"
        )
    return result

@app.get("/api/student/history/{email}")
def student_history(email: str):
    email = email.strip().lower()
    df_history = get_student_prediction_history(email)
    records = df_history.replace({np.nan: None}).to_dict(orient="records") if len(df_history) > 0 else []
    for r in records:
        ts = r.get("predicted_at") or r.get("created_at") or ""
        r["timestamp"] = ts
        r["predicted_at"] = ts
        prob = float(r.get("probability", 0) or 0)
        status = r.get("predicted_status") or r.get("status") or ("Placed" if prob >= 0.5 else "Not Placed")
        is_placed = (status.lower() == "placed") or (prob >= 0.5)
        r["predicted_status"] = "Placed" if is_placed else "Not Placed"
        r["status"] = r["predicted_status"]
        r["prediction"] = 1 if is_placed else 0
        r["probability"] = prob
    return {"history": records}

@app.get("/api/student/skills/{email}")
def student_skills(email: str):
    email = email.strip().lower()
    profile = get_student_profile(email) or {}
    profile = normalize_student_features(profile)
    
    df = load_data()
    placed_df = df[df["placement_prediction"] == 1]
    
    benchmarks = {
        "CGPA": round(float(placed_df["cgpa"].mean()), 2) if "cgpa" in placed_df else 8.5,
        "DSA Practice": round(float(placed_df["dsa_questions_solved"].median()), 1) if "dsa_questions_solved" in placed_df else 250,
        "Aptitude": round(float(placed_df["aptitude_score"].mean()), 1) if "aptitude_score" in placed_df else 82,
        "Coding Skill": round(float(placed_df["coding_skill_score"].mean()), 1) if "coding_skill_score" in placed_df else 8.2,
        "Projects": round(float(placed_df["projects_count"].median()), 1) if "projects_count" in placed_df else 3,
        "Internships": round(float(placed_df["internships_count"].median()), 1) if "internships_count" in placed_df else 1,
        "Mock Interviews": round(float(placed_df["mock_interview_score"].mean()), 1) if "mock_interview_score" in placed_df else 8.0,
        "Attendance": round(float(placed_df["attendance_percentage"].mean()), 1) if "attendance_percentage" in placed_df else 85
    }
    
    student_scores = {
        "CGPA": round(float(profile.get("cgpa", 0.0) or 0.0), 2),
        "DSA Practice": round(float(profile.get("dsa_questions_solved", 0) or 0), 1),
        "Aptitude": round(float(profile.get("aptitude_score", 0.0) or 0.0), 1),
        "Coding Skill": round(float(profile.get("coding_skill_score", 0.0) or 0.0), 1),
        "Projects": round(float(profile.get("projects_count", 0) or 0), 1),
        "Internships": round(float(profile.get("internships_count", 0) or 0), 1),
        "Mock Interviews": round(float(profile.get("mock_interview_score", 0.0) or 0.0), 1),
        "Attendance": round(float(profile.get("attendance_percentage", 0.0) or 0.0), 1)
    }

    radar_data = [
        {"subject": k, "student": student_scores[k], "benchmark": benchmarks[k]}
        for k in benchmarks.keys()
    ]
    
    return {
        "radar_data": radar_data,
        "benchmarks": benchmarks,
        "student_scores": student_scores
    }

@app.get("/api/student/plan/{email}")
def student_plan(email: str):
    email = email.strip().lower()
    profile = get_student_profile(email) or {}
    df = load_data()
    plan = generate_recommendations(profile, df)
    return {"plan": plan}

# -------------------------------------------------------------
# ADMIN WORKSPACE ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/admin/overview")
def admin_overview():
    counts = get_dataset_counts()
    df = load_data(include_new_students=True)
    profiles_df = get_all_student_profiles_df()
    
    total_stu = len(df)
    placed_count = int((df["placement_prediction"] == 1).sum()) if "placement_prediction" in df.columns else 0
    not_placed_count = total_stu - placed_count
    placed_pct = round(float((df["placement_prediction"] == 1).mean() * 100), 1) if "placement_prediction" in df.columns else 0.0
    
    dept_stats = []
    dept_dist = []
    if "branch" in df.columns:
        dept_grp = df.groupby("branch").agg(
            total=("placement_prediction", "count"),
            placed=("placement_prediction", lambda x: int((x == 1).sum())),
            not_placed=("placement_prediction", lambda x: int((x == 0).sum()))
        ).reset_index()
        dept_grp["placement_rate"] = (dept_grp["placed"] / dept_grp["total"] * 100).round(1)
        dept_stats = dept_grp.to_dict(orient="records")
        dept_dist = dept_grp[["branch", "placed", "not_placed"]].to_dict(orient="records")

    avg_cgpa = round(float(df["cgpa"].mean()), 2) if "cgpa" in df.columns else 7.52
    metrics = {
        "total_students": total_stu,
        "placed_students": placed_count,
        "not_placed_students": not_placed_count,
        "placement_rate": placed_pct,
        "registered_students": len(profiles_df),
        "average_cgpa": avg_cgpa
    }

    recent_preds_df = get_student_prediction_history().head(5)
    recent_preds = recent_preds_df.replace({np.nan: None}).to_dict(orient="records") if len(recent_preds_df) > 0 else []
    for r in recent_preds:
        r["timestamp"] = r.get("predicted_at") or r.get("created_at") or "Today"
        r["event_type"] = f"Prediction: {r.get('predicted_status', 'Evaluated')} ({r.get('model_name', 'Model')})"

    return {
        "metrics": metrics,
        "counts": counts,
        "dept_distribution": dept_dist,
        "department_stats": dept_stats,
        "overall_placement_rate": placed_pct,
        "registered_students_count": len(profiles_df),
        "recent_activity": recent_preds
    }

@app.get("/api/admin/students")
def admin_students():
    df = get_all_student_profiles_df()
    df_clean = df.replace({np.nan: None})
    return {"students": df_clean.to_dict(orient="records") if len(df_clean) > 0 else []}

@app.post("/api/admin/feedback")
def admin_feedback_post(req: FeedbackRequest):
    profile = get_student_profile(req.student_email) or {}
    sid = profile.get("student_id", f"STU-{abs(hash(req.student_email)) % 90000 + 10000}")
    save_admin_feedback(
        student_id=sid,
        email=req.student_email.strip().lower(),
        prediction=req.status,
        recommendation=req.notes,
        priority="High" if req.status in ["At Risk", "Not Placed"] else "Medium",
        admin_name=req.admin_name
    )
    return {"status": "success", "message": "Feedback saved."}

@app.post("/api/admin/predict")
def admin_predict(req: PredictRequest):
    result = predict_placement(req.data, model_name=req.model_name)
    if req.email:
        email = req.email.strip().lower()
        profile = get_student_profile(email) or {}
        sid = profile.get("student_id", f"STU-{abs(hash(email)) % 90000 + 10000}")
        log_prediction_to_db(
            student_id=sid,
            email=email,
            status=result.get("status", "Not Placed"),
            prob=result.get("probability", 0.0),
            model_name=result.get("model_name", req.model_name or "Random Forest"),
            features=req.data,
            evaluated_by="Admin Assessment"
        )
    return result

@app.post("/api/admin/predict/compare")
def admin_predict_compare(req: PredictRequest):
    df = load_data()
    models_to_test = list(MODEL_FILENAME_MAP.keys())
    results = {}
    placed_count = 0
    total_models = len(models_to_test)
    
    for m in models_to_test:
        try:
            res = predict_placement(req.data, reference_df=df, model_name=m)
            is_placed = res["status"] == "Placed"
            if is_placed:
                placed_count += 1
            results[m] = {
                "status": res["status"],
                "probability": res["probability"],
                "probability_percent": res["probability_percent"],
                "readiness_level": res.get("readiness_level", "")
            }
        except Exception as e:
            results[m] = {"error": str(e)}
            
    consensus_percent = round((placed_count / total_models) * 100, 1) if total_models > 0 else 0
    consensus_status = "Placed" if placed_count >= (total_models / 2) else "Not Placed"
    
    return {
        "models": results,
        "consensus": {
            "status": consensus_status,
            "placed_votes": placed_count,
            "total_models": total_models,
            "consensus_percent": consensus_percent
        }
    }

@app.post("/api/admin/predict/batch")
async def admin_predict_batch(file: UploadFile = File(...), model_name: Optional[str] = "Random Forest"):
    try:
        import io
        contents = await file.read()
        df_upload = pd.read_csv(io.BytesIO(contents))
        out_df = batch_predict(df_upload, model_name=model_name)
        return {
            "total": len(out_df),
            "placed_count": int((out_df["Predicted_Placement"] == "Placed").sum()),
            "records": out_df.head(100).to_dict(orient="records"),
            "columns": list(out_df.columns)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/reports/summary")
def admin_reports_summary():
    df = load_data()
    ds_summary = df.describe().T.reset_index().rename(columns={"index": "Feature"})
    return {"summary": ds_summary.to_dict(orient="records")}

# -------------------------------------------------------------
# DATA WAREHOUSE ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/admin/warehouse")
def admin_warehouse_info():
    summary = get_warehouse_summary()
    return {
        "tables": summary,
        "schema_def": STAR_SCHEMA_DEF,
        "relationships": RELATIONSHIPS
    }

@app.get("/api/admin/warehouse/sample/{table_name}")
def admin_warehouse_sample(table_name: str, limit: int = 50):
    recs = get_sample_records(table_name, limit=limit)
    return {"table": table_name, "records": recs}

@app.post("/api/admin/warehouse/query")
def admin_warehouse_query(req: SQLQueryRequest):
    sql = req.sql.strip()
    # Security constraint: only allow SELECT queries
    if not sql.upper().startswith("SELECT"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are permitted in the warehouse workbench.")
    try:
        df_res = run_sql(sql)
        return {
            "columns": list(df_res.columns),
            "rows": df_res.to_dict(orient="records"),
            "count": len(df_res)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/warehouse/rebuild")
def admin_warehouse_rebuild():
    try:
        df = load_data(include_new_students=True)
        build_warehouse(df)
        return {"status": "success", "message": "Star schema warehouse rebuilt successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------
# OLAP ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/admin/olap/meta")
def admin_olap_meta():
    df = load_data()
    dimension_values = {}
    for d in DIMENSIONS:
        if d in df.columns:
            vals = df[d].dropna().unique().tolist()
            try:
                vals = sorted(vals, key=lambda x: str(x))
            except Exception:
                pass
            dimension_values[d] = [str(v) for v in vals]
        else:
            dimension_values[d] = []

    dim_labels = {d: DISPLAY_NAMES.get(d, d.replace("_", " ").title()) for d in DIMENSIONS}
    measure_labels = {m: DISPLAY_NAMES.get(m, m.replace("_", " ").title()) for m in MEASURES}

    return {
        "dimensions": DIMENSIONS,
        "measures": MEASURES,
        "agg_funcs": AGG_FUNCS,
        "aggregations": [a.lower() for a in AGG_FUNCS],
        "dimension_values": dimension_values,
        "dim_labels": dim_labels,
        "measure_labels": measure_labels,
        "branches": dimension_values.get("branch", ["CSE", "IT", "ECE", "ENTC", "Civil", "Mechanical"]),
        "genders": dimension_values.get("gender", ["Male", "Female", "Other"]),
        "placement_statuses": dimension_values.get("placement_status", ["Placed", "Not Placed"]),
        "training_options": dimension_values.get("placement_training", ["Yes", "No"])
    }

@app.post("/api/admin/olap/query")
def admin_olap_query(req: OLAPQueryRequest):
    df = load_data(include_new_students=True)
    op = req.operation.lower()
    
    before_df = None
    try:
        if op == "slice":
            res_df = slice_op(df, req.dimension, req.slice_value, req.measure, req.agg_func, display_dim=req.row_dim)
        elif op == "dice":
            rows = [req.row_dim] if req.row_dim else ["branch"]
            cols = [req.col_dim] if req.col_dim and req.col_dim != "None" else ["placement_status"]
            conditions = req.dice_conditions or req.filters or {}
            res_df = dice_op(df, conditions, rows, cols, req.measure, req.agg_func)
        elif op == "rollup":
            curr_rows = (req.filters.get("current_rows") if req.filters else None) or ([req.row_dim, "gender"] if req.row_dim else ["branch", "gender"])
            targ_rows = (req.filters.get("target_rows") if req.filters else None) or ([req.row_dim] if req.row_dim else ["branch"])
            curr_cols = (req.filters.get("current_cols") if req.filters else None) or ([req.col_dim] if req.col_dim else ["placement_status"])
            targ_cols = (req.filters.get("target_cols") if req.filters else None) or []
            before_df, res_df = rollup_2d(df, curr_rows, targ_rows, curr_cols, targ_cols, req.measure, req.agg_func)
        elif op == "drilldown":
            curr_rows = (req.filters.get("current_rows") if req.filters else None) or ([req.row_dim] if req.row_dim else ["branch"])
            targ_rows = (req.filters.get("target_rows") if req.filters else None) or ([req.row_dim, "gender"] if req.row_dim else ["branch", "gender"])
            curr_cols = (req.filters.get("current_cols") if req.filters else None) or ([req.col_dim] if req.col_dim else ["placement_status"])
            targ_cols = (req.filters.get("target_cols") if req.filters else None) or []
            before_df, res_df = drilldown_2d(df, curr_rows, targ_rows, curr_cols, targ_cols, req.measure, req.agg_func)
        elif op == "pivot":
            rows = [req.row_dim] if req.row_dim else ["branch"]
            cols = [req.col_dim] if req.col_dim else ["gender"]
            res_df = pivot_op(df, rows, cols, req.measure, req.agg_func)
        elif op == "drill_across":
            measures = req.measures if req.measures and len(req.measures) > 0 else [req.measure, "aptitude_score", "coding_skill_score"]
            row = req.row_dim or req.dimension or "branch"
            col = req.col_dim if req.col_dim and req.col_dim != "None" else None
            res_df = drill_across(df, row, col, measures, req.agg_func)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported OLAP operation: {op}")

        # Clean NaN/Inf in res_df and before_df
        res_df = res_df.replace({np.nan: None})
        if before_df is not None:
            before_df = before_df.replace({np.nan: None})

        # Log query to history
        try:
            log_olap_query(
                user_email="admin@college.com",
                operation=req.operation,
                row_dims=[req.row_dim] if req.row_dim else ([req.dimension] if req.dimension else []),
                col_dims=[req.col_dim] if req.col_dim else [],
                measure=req.measure,
                agg_func=req.agg_func,
                filters=req.filters or req.dice_conditions or {},
                result_rows=len(res_df)
            )
        except Exception:
            pass

        return {
            "operation": req.operation,
            "columns": list(res_df.columns),
            "rows": res_df.to_dict(orient="records"),
            "data": res_df.to_dict(orient="records"),
            "count": len(res_df),
            "row_count": len(res_df),
            "before_columns": list(before_df.columns) if before_df is not None else None,
            "before_rows": before_df.to_dict(orient="records") if before_df is not None else None,
            "before_data": before_df.to_dict(orient="records") if before_df is not None else None,
            "measure": req.measure,
            "agg_func": req.agg_func
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/olap/history")
def admin_olap_history():
    hist_df = get_olap_history(limit=50)
    records = hist_df.replace({np.nan: None}).to_dict(orient="records") if len(hist_df) > 0 else []
    for r in records:
        r["timestamp"] = r.get("executed_at") or r.get("timestamp") or ""
        r["filters"] = r.get("filters_json") or r.get("filters") or ""
    return {"history": records}

# -------------------------------------------------------------
# DATA MINING & MACHINE LEARNING
# -------------------------------------------------------------
@app.get("/api/admin/data-mining")
def admin_data_mining():
    df = load_data()
    corr_df = correlation(df)
    mi_df = mutual_information(df)
    fi_df = feature_importance(df)
    rules_df = association_insights(df)

    mi_records = mi_df.to_dict(orient="records") if mi_df is not None else []
    return {
        "correlation": corr_df.reset_index().to_dict(orient="records") if corr_df is not None else [],
        "mutual_info": mi_records,
        "mutual_information": mi_records,
        "feature_importance": fi_df.to_dict(orient="records") if fi_df is not None else [],
        "association_rules": rules_df.to_dict(orient="records") if rules_df is not None else []
    }

@app.get("/api/admin/classification")
def admin_classification():
    df = load_data()
    metrics_df, artifacts, _ = train_models(df)
    
    formatted_metrics = metrics_df.to_dict(orient="records")
    for row in formatted_metrics:
        row["ROC AUC"] = row.get("ROC-AUC", 0.0)
    
    serialized_artifacts = {}
    for m_name, art in artifacts.items():
        serialized_artifacts[m_name] = {
            "roc_auc": round(float(art["roc_auc"]), 4),
            "pr_auc": round(float(art["pr_auc"]), 4),
            "confusion_matrix": art["cm"].tolist(),
            "fpr": art["fpr"][::max(1, len(art["fpr"]) // 50)].tolist(),
            "tpr": art["tpr"][::max(1, len(art["tpr"]) // 50)].tolist(),
            "feature_importance": art["feature_importance"].head(10).to_dict(orient="records") if art["feature_importance"] is not None else None
        }

    return {
        "metrics": formatted_metrics,
        "artifacts": serialized_artifacts
    }

@app.post("/api/admin/classification/train")
def admin_classification_train(req: Optional[ClassificationTrainRequest] = None):
    df = load_data(include_new_students=True)
    kwargs = {}
    if req:
        if req.test_size is not None: kwargs["test_size"] = req.test_size
        if req.random_state is not None: kwargs["random_state"] = req.random_state
        if req.dt_depth is not None: kwargs["dt_depth"] = req.dt_depth
        if req.rf_estimators is not None: kwargs["rf_estimators"] = req.rf_estimators
        if req.rf_depth is not None: kwargs["rf_depth"] = req.rf_depth
        if req.gb_estimators is not None: kwargs["gb_estimators"] = req.gb_estimators
        if req.gb_depth is not None: kwargs["gb_depth"] = req.gb_depth
        if req.gb_learning_rate is not None: kwargs["gb_learning_rate"] = req.gb_learning_rate
        if req.lr_max_iter is not None: kwargs["lr_max_iter"] = req.lr_max_iter
        if req.lr_C is not None: kwargs["lr_C"] = req.lr_C

    metrics_df, artifacts, _ = train_models(df, **kwargs)
    
    formatted_metrics = metrics_df.to_dict(orient="records")
    for row in formatted_metrics:
        row["ROC AUC"] = row.get("ROC-AUC", 0.0)
    
    serialized_artifacts = {}
    for m_name, art in artifacts.items():
        serialized_artifacts[m_name] = {
            "roc_auc": round(float(art["roc_auc"]), 4),
            "pr_auc": round(float(art["pr_auc"]), 4),
            "confusion_matrix": art["cm"].tolist(),
            "fpr": art["fpr"][::max(1, len(art["fpr"]) // 50)].tolist(),
            "tpr": art["tpr"][::max(1, len(art["tpr"]) // 50)].tolist(),
            "feature_importance": art["feature_importance"].head(10).to_dict(orient="records") if art["feature_importance"] is not None else None
        }

    return {
        "status": "success",
        "message": f"Successfully trained {len(metrics_df)} classification algorithms.",
        "metrics": formatted_metrics,
        "artifacts": serialized_artifacts
    }

@app.get("/api/admin/regression")
def admin_regression(target_col: str = "aptitude_score"):
    df = load_data()
    metrics_df, artifacts = train_regression(df, target_col=target_col)
    
    formatted_metrics = metrics_df.to_dict(orient="records")
    for row in formatted_metrics:
        r2_val = row.get("R²") if row.get("R²") is not None else row.get("R2", 0.0)
        row["R² Score"] = float(r2_val)
        row["R2"] = float(r2_val)
    
    serialized_art = {}
    for m_name, art in artifacts.items():
        m_row = metrics_df[metrics_df["Model"] == m_name].iloc[0]
        serialized_art[m_name] = {
            "r2": round(float(m_row["R²"]), 4),
            "mse": round(float(m_row["MSE"]), 4),
            "mae": round(float(m_row["MAE"]), 4),
            "equation": str(m_row["Equation"]),
            "coefficients": art["coefficients"].tolist() if hasattr(art["coefficients"], "tolist") else list(art["coefficients"]),
            "actual_sample": art["actual"][:100].tolist() if hasattr(art["actual"], "tolist") else list(art["actual"][:100]),
            "pred_sample": art["pred"][:100].tolist() if hasattr(art["pred"], "tolist") else list(art["pred"][:100]),
            "residuals_sample": art["residuals"][:100].tolist() if hasattr(art["residuals"], "tolist") else list(art["residuals"][:100])
        }

    return {
        "target": target_col,
        "metrics": formatted_metrics,
        "artifacts": serialized_art
    }

@app.get("/api/admin/kmeans")
def admin_kmeans(k: int = 4):
    df = load_data()
    features = [c for c in BASE_NUMERIC if c in df.columns]
    res_df, profile, sil, model, t_fit = kmeans(df, features, k=k)
    
    size_df = res_df["Cluster"].value_counts().sort_index().reset_index()
    size_df.columns = ["Cluster", "Count"]
    
    sample_pca = res_df.sample(n=min(200, len(res_df)), random_state=42)[["PC1", "PC2", "Cluster"]].to_dict(orient="records")
    for s in sample_pca:
        s["PCA1"] = s.get("PC1")
        s["PCA2"] = s.get("PC2")

    return {
        "k": k,
        "silhouette": round(float(sil), 4),
        "cluster_sizes": size_df.to_dict(orient="records"),
        "profile": profile.reset_index().to_dict(orient="records"),
        "pca_sample": sample_pca
    }

@app.get("/api/admin/kmeans/elbow")
def admin_kmeans_elbow(k_min: int = 2, k_max: int = 8):
    df = load_data()
    features = [c for c in BASE_NUMERIC if c in df.columns]
    elb_df = elbow(df, features, k_min=k_min, k_max=k_max)
    return {"elbow": elb_df.to_dict(orient="records")}

@app.get("/api/admin/agglomerative")
def admin_agglomerative(k: int = 4, sample_size: int = 1500, linkage_method: str = "ward"):
    df = load_data()
    features = [c for c in BASE_NUMERIC if c in df.columns]
    sample_df, profile, sil, model, t_fit = agglomerative(
        df, features, k=k, sample_size=sample_size, linkage_method=linkage_method
    )
    
    size_df = sample_df["Cluster"].value_counts().sort_index().reset_index()
    size_df.columns = ["Cluster", "Count"]
    
    sample_pca = sample_df.sample(n=min(200, len(sample_df)), random_state=42)[["PC1", "PC2", "Cluster"]].to_dict(orient="records")
    for s in sample_pca:
        s["PCA1"] = s.get("PC1")
        s["PCA2"] = s.get("PC2")

    return {
        "k": k,
        "silhouette": round(float(sil), 4),
        "sample_size": sample_size,
        "linkage": linkage_method,
        "cluster_sizes": size_df.to_dict(orient="records"),
        "profile": profile.reset_index().to_dict(orient="records"),
        "pca_sample": sample_pca
    }

@app.get("/api/admin/cluster-comparison")
def admin_cluster_comparison(k: int = 4):
    df = load_data()
    features = [c for c in BASE_NUMERIC if c in df.columns]
    
    sample_df = df.sample(n=min(1500, len(df)), random_state=42).copy()
    _, km_prof, km_sil, _, _ = kmeans(sample_df, features, k=k)
    _, agg_prof, agg_sil, _, _ = agglomerative(sample_df, features, k=k, sample_size=1500)
    
    return {
        "k": k,
        "kmeans": {
            "silhouette": round(float(km_sil), 4),
            "profile": km_prof.reset_index().to_dict(orient="records")
        },
        "agglomerative": {
            "silhouette": round(float(agg_sil), 4),
            "profile": agg_prof.reset_index().to_dict(orient="records")
        }
    }

@app.get("/api/admin/settings")
def admin_settings_get():
    counts = get_dataset_counts()
    curr_model = get_system_setting("production_model", "Random Forest")
    return {
        "production_model": curr_model,
        "available_models": list(MODEL_FILENAME_MAP.keys()),
        "dataset_counts": counts,
        "database_path": str(DB_PATH.name)
    }

@app.post("/api/admin/settings")
def admin_settings_save(req: SettingRequest):
    set_system_setting(req.key, req.value)
    return {"status": "success", "message": f"Setting {req.key} set to {req.value}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
