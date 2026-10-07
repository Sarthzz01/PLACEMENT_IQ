import pandas as pd
from .config import DATA_PATH, TARGET, BASE_NUMERIC

EXPECTED = BASE_NUMERIC + [
    "gender_Male", "gender_Other", "branch_CSE", "branch_Civil", "branch_ECE",
    "branch_ENTC", "branch_IT", "branch_Mechanical", "placement_training_Yes", TARGET
]

_DATA_CACHE = {}

def clear_data_cache():
    """Clear in-memory cached datasets."""
    _DATA_CACHE.clear()

def validate_dataset(path=DATA_PATH):
    """Inspect dataset and return health summary metrics."""
    df_raw = pd.read_csv(path)
    missing_cols = [c for c in EXPECTED if c not in df_raw.columns]
    null_counts = int(df_raw.isnull().sum().sum())
    duplicates = int(df_raw.duplicated().sum())
    target_dist = df_raw[TARGET].value_counts().to_dict() if TARGET in df_raw.columns else {}
    
    return {
        "valid": len(missing_cols) == 0,
        "rows": len(df_raw),
        "columns": df_raw.shape[1],
        "missing_columns": missing_cols,
        "null_count": null_counts,
        "duplicates": duplicates,
        "target_distribution": target_dist
    }

def convert_profiles_to_dataset_format(profiles_df):
    """
    Transform student profiles from SQLite database into the exact
    26-column schema matching placement_prediction_cleaned.csv.
    """
    if profiles_df is None or len(profiles_df) == 0:
        return pd.DataFrame(columns=EXPECTED)

    rows = []
    for _, r in profiles_df.iterrows():
        row = {}
        # Base numerical features
        for num_col in BASE_NUMERIC:
            val = r.get(num_col)
            try:
                row[num_col] = float(val) if pd.notnull(val) else 0.0
            except (ValueError, TypeError):
                row[num_col] = 0.0

        # One-hot encoded gender (Female is reference category)
        g = str(r.get("gender", "Male")).capitalize()
        row["gender_Male"] = (g == "Male")
        row["gender_Other"] = (g == "Other")

        # One-hot encoded branch
        b = str(r.get("branch", "CSE")).upper()
        for branch_name in ["CSE", "Civil", "ECE", "ENTC", "IT", "Mechanical"]:
            row[f"branch_{branch_name}"] = (b == branch_name.upper())

        # One-hot encoded placement training (No is reference category)
        train_val = str(r.get("placement_training", "Yes")).lower()
        row["placement_training_Yes"] = train_val in ["yes", "true", "1"]

        # Target (Placement status: 1 if Placed, 0 if Not Placed)
        pred_val = r.get("placement_prediction", 1 if row.get("cgpa", 0) >= 7.5 else 0)
        try:
            row[TARGET] = int(pred_val)
        except (ValueError, TypeError):
            row[TARGET] = 0

        rows.append(row)

    out_df = pd.DataFrame(rows)
    for col in EXPECTED:
        if col not in out_df.columns:
            out_df[col] = 0
    return out_df[EXPECTED]

def load_data(path=DATA_PATH, include_new_students=False, force_reload=False):
    """
    Load, validate, clean, and enrich placement prediction dataset.
    If include_new_students is True, merges original dataset with valid newly
    registered students from SQLite database to form a Unified Analytics Dataset.
    """
    cache_key = (str(path), bool(include_new_students))
    if not force_reload and cache_key in _DATA_CACHE:
        return _DATA_CACHE[cache_key].copy()

    df = pd.read_csv(path)
    missing = [c for c in EXPECTED if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    
    for c in BASE_NUMERIC + [TARGET]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    
    bool_cols = [c for c in EXPECTED if c not in BASE_NUMERIC + [TARGET]]
    for c in bool_cols:
        df[c] = df[c].astype(bool)
        
    df = df.drop_duplicates().copy()
    df = df.dropna(subset=[TARGET]).copy()
    
    for c in BASE_NUMERIC:
        df[c] = df[c].fillna(df[c].median())
        
    df[TARGET] = df[TARGET].astype(int)
    
    # Tag dataset origin
    df["data_source"] = "Original Dataset"

    # Merge newly added student records from database if requested
    if include_new_students:
        try:
            from .database import get_all_student_profiles_df
            new_profiles = get_all_student_profiles_df()
            if len(new_profiles) > 0:
                new_df = convert_profiles_to_dataset_format(new_profiles)
                new_df["data_source"] = "New Student Record"
                df = pd.concat([df, new_df], ignore_index=True)
        except Exception:
            pass

    result_df = add_derived(df)
    _DATA_CACHE[cache_key] = result_df
    return result_df.copy()

def get_dataset_counts():
    """Retrieve counts for Original, New, and Combined datasets."""
    orig_cnt = 15000
    try:
        df_orig = pd.read_csv(DATA_PATH)
        orig_cnt = len(df_orig)
    except Exception:
        pass

    new_cnt = 0
    try:
        from .database import get_all_student_profiles_df
        new_profiles = get_all_student_profiles_df()
        new_cnt = len(new_profiles)
    except Exception:
        pass

    return {
        "original_students": orig_cnt,
        "new_students": new_cnt,
        "combined_students": orig_cnt + new_cnt
    }

def add_derived(df):
    """Add analytical and categorical helper columns for OLAP and visualizations."""
    out = df.copy()
    
    # Reconstruct human-readable gender
    out["gender"] = out.apply(
        lambda r: "Other" if r.get("gender_Other", False) else ("Male" if r.get("gender_Male", False) else "Female"),
        axis=1
    )
    
    # Reconstruct human-readable branch
    branch_cols = [c for c in out.columns if c.startswith("branch_")]
    if branch_cols:
        out["branch"] = out[branch_cols].idxmax(axis=1).str.replace("branch_", "", regex=False)
    else:
        out["branch"] = "CSE"
        
    out["placement_training"] = out["placement_training_Yes"].map({True: "Yes", False: "No"})
    out["placement_status"] = out[TARGET].map({1: "Placed", 0: "Not Placed"})
    
    out["cgpa_band"] = pd.cut(out["cgpa"], bins=[0, 6, 7, 8, 9, 10.1], labels=["<6", "6-7", "7-8", "8-9", "9+"], right=False).astype(str)
    out["aptitude_band"] = pd.cut(out["aptitude_score"], bins=[0, 50, 60, 70, 80, 101], labels=["<50", "50-60", "60-70", "70-80", "80+"], right=False).astype(str)
    out["attendance_band"] = pd.cut(out["attendance_percentage"], bins=[0, 60, 75, 85, 95, 101], labels=["<60", "60-75", "75-85", "85-95", "95+"], right=False).astype(str)
    out["coding_band"] = pd.cut(out["coding_skill_score"], bins=[0, 4, 6, 8, 10.1], labels=["<4", "4-6", "6-8", "8+"], right=False).astype(str)
    out["internship_band"] = out["internships_count"].astype(int).astype(str).replace({"0": "0", "1": "1", "2": "2", "3": "3", "4": "4+"})
    out["projects_band"] = pd.cut(out["projects_count"], bins=[-1, 0, 2, 4, 100], labels=["0", "1-2", "3-4", "5+"]).astype(str)
    out["backlog_band"] = out["backlogs"].astype(int).astype(str)
    return out

def model_matrix(df):
    """Extract features matrix X, labels y, and feature column list for ML models."""
    feature_cols = BASE_NUMERIC + [
        "gender_Male", "gender_Other", "branch_CSE", "branch_Civil", "branch_ECE",
        "branch_ENTC", "branch_IT", "branch_Mechanical", "placement_training_Yes"
    ]
    X = df[feature_cols].astype(float)
    y = df[TARGET].astype(int) if TARGET in df.columns else None
    return X, y, feature_cols
