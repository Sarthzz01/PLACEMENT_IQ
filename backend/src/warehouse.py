import sqlite3
import pandas as pd
from pathlib import Path
from .config import DB_PATH

STAR_SCHEMA_DEF = {
    "FactPlacement": [
        "fact_id (PK)", "student_key (FK)", "cgpa", "attendance_percentage",
        "aptitude_score", "coding_skill_score", "internships_count", "projects_count", "placement_prediction"
    ],
    "DimStudent": [
        "student_key (PK)", "age", "gender", "branch", "data_source"
    ],
    "DimAcademic": [
        "student_key (PK)", "cgpa", "backlogs", "attendance_percentage", "cgpa_band"
    ],
    "DimSkills": [
        "student_key (PK)", "dsa_questions_solved", "leetcode_questions_solved",
        "hackerrank_questions_solved", "aptitude_score", "communication_score",
        "coding_skill_score", "certifications_count", "coding_band"
    ],
    "DimEngagement": [
        "student_key (PK)", "internships_count", "projects_count",
        "hackathons_count", "github_repos", "mock_interview_score", "placement_training"
    ],
    "DimPlacement": [
        "student_key (PK)", "placement_prediction", "placement_status"
    ]
}

RELATIONSHIPS = [
    {"from": "FactPlacement.student_key", "to": "DimStudent.student_key", "cardinality": "N:1", "type": "Identifying"},
    {"from": "FactPlacement.student_key", "to": "DimAcademic.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimSkills.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimEngagement.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimPlacement.student_key", "cardinality": "1:1", "type": "Target Dimension"}
]

def build_warehouse(df, db_path=DB_PATH):
    """Construct or refresh the SQLite Star-Schema Data Warehouse."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    
    # Drop existing warehouse tables
    con.execute("DROP TABLE IF EXISTS FactPlacement")
    for t in ["DimStudent", "DimAcademic", "DimSkills", "DimEngagement", "DimPlacement"]:
        con.execute(f"DROP TABLE IF EXISTS {t}")
        
    base = df.reset_index(drop=True).copy()
    base["student_key"] = range(1, len(base) + 1)
    if "data_source" not in base.columns:
        base["data_source"] = "Original Dataset"
    
    # Populate Dimension Tables
    pd.DataFrame({
        "student_key": base.student_key,
        "age": base.age,
        "gender": base.gender,
        "branch": base.branch,
        "data_source": base.data_source
    }).to_sql("DimStudent", con, index=False)
    
    acad_cols = ["student_key", "cgpa", "backlogs", "attendance_percentage"]
    if "cgpa_band" in base.columns:
        acad_cols.append("cgpa_band")
    base[acad_cols].to_sql("DimAcademic", con, index=False)
    
    skills_cols = [
        "student_key", "dsa_questions_solved", "leetcode_questions_solved",
        "hackerrank_questions_solved", "aptitude_score", "communication_score",
        "coding_skill_score", "certifications_count"
    ]
    if "coding_band" in base.columns:
        skills_cols.append("coding_band")
    base[skills_cols].to_sql("DimSkills", con, index=False)
    
    base[[
        "student_key", "internships_count", "projects_count", "hackathons_count",
        "github_repos", "mock_interview_score", "placement_training"
    ]].to_sql("DimEngagement", con, index=False)
    
    base[["student_key", "placement_prediction", "placement_status"]].to_sql("DimPlacement", con, index=False)
    
    # Populate Central Fact Table
    fact = base[[
        "student_key", "cgpa", "attendance_percentage", "aptitude_score",
        "coding_skill_score", "internships_count", "projects_count", "placement_prediction"
    ]].copy()
    fact["fact_id"] = range(1, len(fact) + 1)
    fact.to_sql("FactPlacement", con, index=False)
    
    con.commit()
    con.close()
    return db_path

def query(sql, db_path=DB_PATH):
    """Execute arbitrary SQL queries against the warehouse database."""
    con = sqlite3.connect(db_path)
    try:
        out = pd.read_sql_query(sql, con)
    finally:
        con.close()
    return out

def get_warehouse_summary(db_path=DB_PATH):
    """Retrieve metadata, table row counts, and schema definitions."""
    if not db_path.exists():
        return {}
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    tables = [
        "FactPlacement", "DimStudent", "DimAcademic", "DimSkills", "DimEngagement", "DimPlacement"
    ]
    summary = {}
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]
            summary[t] = {
                "rows": cnt,
                "columns": STAR_SCHEMA_DEF.get(t, [])
            }
        except Exception:
            summary[t] = {"rows": 0, "columns": []}
    con.close()
    return summary

def get_sample_records(table_name, limit=5, db_path=DB_PATH):
    """Fetch sample rows from any warehouse table."""
    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", con)
    finally:
        con.close()
    return df
