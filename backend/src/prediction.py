import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from .config import MODEL_DIR, TARGET, BASE_NUMERIC
from .preprocessing import load_data, model_matrix
from .classification import train_models
from .recommendations import generate_recommendations
from .database import get_system_setting

MODEL_FILENAME_MAP = {
    "Random Forest": "random_forest.joblib",
    "Gradient Boosting": "gradient_boosting.joblib",
    "Decision Tree": "decision_tree.joblib",
    "Logistic Regression": "logistic_regression.joblib",
    "Naive Bayes": "naive_bayes.joblib"
}

def get_production_model_name():
    """Retrieve currently active production model from system settings."""
    return get_system_setting("production_model", "Random Forest")

def load_or_train_model(model_name=None, df=None):
    """Load specified model from disk, or train all classifiers if missing."""
    if not model_name:
        model_name = get_production_model_name()

    fname = MODEL_FILENAME_MAP.get(model_name, "random_forest.joblib")
    path = MODEL_DIR / fname

    if path.exists():
        try:
            return joblib.load(path), model_name
        except Exception:
            pass

    # Model file missing or corrupted, retrain
    if df is None:
        df = load_data()
    _, artifacts, _ = train_models(df)
    target_key = model_name if model_name in artifacts else "Random Forest"
    return artifacts[target_key]["model"], target_key

def format_student_row(input_dict, reference_df=None):
    """Format user form input into model feature matrix."""
    if reference_df is None:
        reference_df = load_data()
        
    row = {c: 0 for c in reference_df.columns if c not in ["placement_status", "cgpa_band", "aptitude_band", "attendance_band", "coding_band", "internship_band", "projects_band", "backlog_band", "data_source"]}
    
    # Assign numeric attributes
    for col in BASE_NUMERIC:
        if col in input_dict:
            try:
                row[col] = float(input_dict[col])
            except (ValueError, TypeError):
                row[col] = 0.0
            
    # Assign one-hot categoricals
    gender = str(input_dict.get("gender", "Male")).capitalize()
    row["gender_Male"] = (gender == "Male")
    row["gender_Other"] = (gender == "Other")
    
    branch = str(input_dict.get("branch", "CSE")).upper()
    for b_col in [c for c in row.keys() if c.startswith("branch_")]:
        row[b_col] = (b_col.upper() == f"BRANCH_{branch}")
        
    training = str(input_dict.get("placement_training", "Yes")).lower()
    row["placement_training_Yes"] = (training in ["yes", "true", "1"])
    
    row[TARGET] = 0
    df_row = pd.DataFrame([row])
    X, _, feature_names = model_matrix(df_row)
    return X, feature_names

def predict_placement(input_dict, model=None, reference_df=None, model_name=None):
    """
    Predict placement probability, binary outcome, and actionable data-driven recommendations.
    Uses specified model or current production model.
    """
    if reference_df is None:
        reference_df = load_data()

    if model is None:
        model, model_name = load_or_train_model(model_name, reference_df)
    elif not model_name:
        model_name = "Production Classifier"
        
    X, feature_names = format_student_row(input_dict, reference_df)
    
    # Model inference
    try:
        prob = float(model.predict_proba(X)[0, 1])
    except Exception:
        pred_raw = int(model.predict(X)[0])
        prob = 0.85 if pred_raw == 1 else 0.25

    outcome = "Placed" if prob >= 0.5 else "Not Placed"
    
    # Data-driven recommendations using actual dataset statistics
    rec_results = generate_recommendations(input_dict, reference_df)
    
    return {
        "status": outcome,
        "probability": prob,
        "probability_percent": round(prob * 100, 1),
        "model_name": model_name,
        "readiness_level": rec_results["readiness_level"],
        "top_improvements": rec_results["top_improvements"],
        "all_improvements": rec_results["all_improvements"],
        "recommendations": rec_results["top_improvements"],
        "strengths": rec_results["strengths"]
    }

def batch_predict(df_input, model=None, reference_df=None, model_name=None):
    """Run batch predictions on an uploaded DataFrame."""
    if reference_df is None:
        reference_df = load_data()
    if model is None:
        model, model_name = load_or_train_model(model_name, reference_df)
        
    results = []
    for _, row in df_input.iterrows():
        pred_dict = predict_placement(row.to_dict(), model, reference_df, model_name)
        results.append({
            "Prediction": pred_dict["status"],
            "Probability": f"{pred_dict['probability_percent']}%",
            "Readiness": pred_dict["readiness_level"]
        })
        
    out = df_input.copy()
    pred_df = pd.DataFrame(results)
    out["Predicted_Placement"] = pred_df["Prediction"]
    out["Confidence"] = pred_df["Probability"]
    out["Readiness_Tier"] = pred_df["Readiness"]
    return out
