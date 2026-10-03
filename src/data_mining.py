import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from .preprocessing import model_matrix

def correlation(df, target="placement_prediction"):
    """Compute Pearson correlation of all numeric features with target."""
    num_df = df.select_dtypes(include="number")
    if target not in num_df.columns:
        return pd.DataFrame(columns=["Feature", "Correlation"])
    corr = num_df.corr()[target].drop(target, errors="ignore").sort_values(ascending=False).reset_index()
    corr.columns = ["Feature", "Correlation"]
    return corr

def mutual_information(df, target="placement_prediction"):
    """Compute non-linear dependency via Mutual Information."""
    X, y, features = model_matrix(df)
    if y is None or len(y) == 0:
        return pd.DataFrame(columns=["Feature", "Mutual Information"])
    mi = mutual_info_classif(X, y, random_state=42)
    return pd.DataFrame({
        "Feature": features,
        "Mutual Information": mi
    }).sort_values("Mutual Information", ascending=False)

def feature_importance(df):
    """Calculate Gini feature importance using a Random Forest ensemble."""
    X, y, features = model_matrix(df)
    m = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42, n_jobs=-1).fit(X, y)
    return pd.DataFrame({
        "Feature": features,
        "Importance": m.feature_importances_
    }).sort_values("Importance", ascending=False)

def association_insights(df):
    """
    Generate Apriori-style Association Rules based on academic and skill thresholds.
    Evaluates Support, Confidence, and Lift.
    """
    work = df.copy()
    work["High_CGPA"] = work.cgpa >= 8.0
    work["High_Aptitude"] = work.aptitude_score >= 70.0
    work["High_Attendance"] = work.attendance_percentage >= 85.0
    work["Internship_Done"] = work.internships_count >= 1
    work["Multiple_Projects"] = work.projects_count >= 3
    work["Strong_Coding"] = work.coding_skill_score >= 7.0
    work["Placed"] = work.placement_prediction == 1
    
    antecedents = ["High_CGPA", "High_Aptitude", "High_Attendance", "Internship_Done", "Multiple_Projects", "Strong_Coding"]
    rows = []
    
    for a in antecedents:
        for b in antecedents + ["Placed"]:
            if a == b:
                continue
            support = float(((work[a]) & (work[b])).mean())
            conf = float(((work[a]) & (work[b])).sum() / max(work[a].sum(), 1))
            base_b = float(work[b].mean())
            lift = float(conf / base_b) if base_b > 0 else 0.0
            
            if support >= 0.05 and conf >= 0.35:
                interpretation = (
                    f"Students with {a.replace('_', ' ')} have a {conf*100:.1f}% probability of {b.replace('_', ' ')} "
                    f"({lift:.2f}x higher than average)."
                )
                rows.append({
                    "Rule": f"{a} → {b}",
                    "Support": round(support, 3),
                    "Confidence": round(conf, 3),
                    "Lift": round(lift, 3),
                    "Interpretation": interpretation
                })
                
    if rows:
        return pd.DataFrame(rows).sort_values("Lift", ascending=False)
    return pd.DataFrame(columns=["Rule", "Support", "Confidence", "Lift", "Interpretation"])
