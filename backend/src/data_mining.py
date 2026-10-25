import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from .preprocessing import model_matrix
from .config import DISPLAY_NAMES

def correlation(df, target="placement_prediction"):
    """
    Compute Pearson correlation of all numeric features with target.
    Includes feature labels, directional classification, and strength metrics.
    """
    num_df = df.select_dtypes(include="number")
    if target not in num_df.columns:
        return pd.DataFrame(columns=["Feature", "Correlation", "Abs_Correlation", "Direction", "Strength", "Feature_Label"])
    
    corr_series = num_df.corr()[target].drop(target, errors="ignore")
    corr_df = corr_series.reset_index()
    corr_df.columns = ["Feature", "Correlation"]
    
    corr_df["Correlation"] = corr_df["Correlation"].round(4)
    corr_df["Abs_Correlation"] = corr_df["Correlation"].abs().round(4)
    corr_df["Direction"] = corr_df["Correlation"].apply(lambda x: "Positive" if x >= 0 else "Negative")
    
    def classify_strength(abs_val):
        if abs_val >= 0.50:
            return "Strong"
        elif abs_val >= 0.30:
            return "Moderate"
        elif abs_val >= 0.10:
            return "Weak"
        return "Negligible"
        
    corr_df["Strength"] = corr_df["Abs_Correlation"].apply(classify_strength)
    corr_df["Feature_Label"] = corr_df["Feature"].apply(lambda f: DISPLAY_NAMES.get(f, f.replace("_", " ").title()))
    
    return corr_df.sort_values("Abs_Correlation", ascending=False).reset_index(drop=True)

def correlation_matrix(df, top_features=None):
    """Compute full pairwise correlation matrix for key numeric features."""
    num_df = df.select_dtypes(include="number").copy()
    if top_features:
        cols = [c for c in top_features if c in num_df.columns]
    else:
        cols = [
            "cgpa", "aptitude_score", "coding_skill_score", "dsa_questions_solved",
            "attendance_percentage", "internships_count", "projects_count",
            "mock_interview_score", "backlogs", "placement_prediction"
        ]
        cols = [c for c in cols if c in num_df.columns]
        
    matrix = num_df[cols].corr().round(3)
    return matrix

def mutual_information(df, target="placement_prediction"):
    """
    Compute non-linear dependency via Shannon Mutual Information (I(X;Y)).
    Ranks features by information gain and compares against linear correlation rank.
    """
    X, y, features = model_matrix(df)
    if y is None or len(y) == 0:
        return pd.DataFrame(columns=["Feature", "Mutual Information", "Normalized_MI_Pct", "Feature_Label"])
        
    mi = mutual_info_classif(X, y, random_state=42)
    mi_df = pd.DataFrame({
        "Feature": features,
        "Mutual Information": np.round(mi, 4)
    })
    
    max_mi = mi_df["Mutual Information"].max()
    mi_df["Normalized_MI_Pct"] = (mi_df["Mutual Information"] / max_mi * 100.0).round(1) if max_mi > 0 else 0.0
    mi_df["Feature_Label"] = mi_df["Feature"].apply(lambda f: DISPLAY_NAMES.get(f, f.replace("_", " ").title()))
    
    return mi_df.sort_values("Mutual Information", ascending=False).reset_index(drop=True)

def feature_importance(df):
    """
    Calculate Gini feature importance using a Random Forest ensemble (MDI).
    Computes individual percentage weights and cumulative Pareto distribution.
    """
    X, y, features = model_matrix(df)
    m = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42, n_jobs=-1).fit(X, y)
    
    fi_df = pd.DataFrame({
        "Feature": features,
        "Importance": np.round(m.feature_importances_, 4)
    }).sort_values("Importance", ascending=False).reset_index(drop=True)
    
    fi_df["Importance_Pct"] = (fi_df["Importance"] * 100.0).round(2)
    fi_df["Cumulative_Pct"] = fi_df["Importance_Pct"].cumsum().round(2)
    fi_df["Feature_Label"] = fi_df["Feature"].apply(lambda f: DISPLAY_NAMES.get(f, f.replace("_", " ").title()))
    
    return fi_df

def association_insights(df, min_support=0.03, min_confidence=0.40, min_lift=1.0):
    """
    Generate Apriori-style Association Rules based on academic and technical milestones.
    Mines both single-item and multi-item antecedents (IF {A, B} -> THEN {Placed}).
    Evaluates Support, Confidence, Lift, and Leverage.
    """
    work = df.copy()
    
    items = {
        "High CGPA (>= 8.0)": work.cgpa >= 8.0,
        "High Aptitude (>= 75)": work.aptitude_score >= 75.0,
        "Strong Coding (>= 7.5)": work.coding_skill_score >= 7.5,
        "Active DSA Solver (>= 150)": work.dsa_questions_solved >= 150,
        "Multiple Projects (>= 3)": work.projects_count >= 3,
        "Internship Done (>= 1)": work.internships_count >= 1,
        "Zero Active Backlogs": work.backlogs == 0,
        "High Attendance (>= 85%)": work.attendance_percentage >= 85.0,
        "Placement Trained": work.get("placement_training", "") == "Yes",
        "Mock Interview Ready (>= 7.5)": work.mock_interview_score >= 7.5
    }
    
    outcomes = {
        "Placed": work.placement_prediction == 1,
        "Strong Coding (>= 7.5)": work.coding_skill_score >= 7.5,
        "Internship Done (>= 1)": work.internships_count >= 1
    }
    
    item_keys = list(items.keys())
    base_placed = float(outcomes["Placed"].mean())
    rows = []
    
    # 1. Single-Item Antecedent Rules
    for a in item_keys:
        a_series = items[a]
        a_count = int(a_series.sum())
        if a_count < 30:
            continue
            
        for b_name, b_series in outcomes.items():
            if a == b_name:
                continue
            both = a_series & b_series
            support = float(both.mean())
            conf = float(both.sum() / a_count)
            base_b = float(b_series.mean())
            lift = float(conf / base_b) if base_b > 0 else 0.0
            leverage = float(support - (a_series.mean() * base_b))
            
            if support >= min_support and conf >= min_confidence and lift >= min_lift:
                interp = (
                    f"Students with {a} have a {conf*100:.1f}% probability of being {b_name} "
                    f"({lift:.2f}x higher than the baseline rate of {base_b*100:.1f}%)."
                )
                rows.append({
                    "Rule": f"{a} -> {b_name}",
                    "rule": f"{a} -> {b_name}",
                    "antecedents": a,
                    "antecedent": a,
                    "consequents": b_name,
                    "consequent": b_name,
                    "Support": round(support, 3),
                    "support": round(support, 3),
                    "Confidence": round(conf, 3),
                    "confidence": round(conf, 3),
                    "Lift": round(lift, 2),
                    "lift": round(lift, 2),
                    "leverage": round(leverage, 4),
                    "Interpretation": interp,
                    "interpretation": interp,
                    "item_count": 1
                })
                
    # 2. Multi-Item (2-Item Bundle) Antecedent Rules targeting "Placed"
    placed_series = outcomes["Placed"]
    for i in range(len(item_keys)):
        for j in range(i + 1, len(item_keys)):
            k1, k2 = item_keys[i], item_keys[j]
            cond = items[k1] & items[k2]
            cond_count = int(cond.sum())
            if cond_count < 30:
                continue
                
            both = cond & placed_series
            support = float(both.mean())
            conf = float(both.sum() / cond_count)
            lift = float(conf / base_placed) if base_placed > 0 else 0.0
            leverage = float(support - (cond.mean() * base_placed))
            
            if support >= min_support and conf >= 0.50 and lift >= 1.2:
                ant_text = f"{k1} + {k2}"
                interp = (
                    f"Students possessing BOTH [{k1}] and [{k2}] achieve a {conf*100:.1f}% placement probability "
                    f"({lift:.2f}x higher than institutional baseline)."
                )
                rows.append({
                    "Rule": f"{ant_text} -> Placed",
                    "rule": f"{ant_text} -> Placed",
                    "antecedents": ant_text,
                    "antecedent": ant_text,
                    "consequents": "Placed",
                    "consequent": "Placed",
                    "Support": round(support, 3),
                    "support": round(support, 3),
                    "Confidence": round(conf, 3),
                    "confidence": round(conf, 3),
                    "Lift": round(lift, 2),
                    "lift": round(lift, 2),
                    "leverage": round(leverage, 4),
                    "Interpretation": interp,
                    "interpretation": interp,
                    "item_count": 2
                })
                
    if rows:
        res_df = pd.DataFrame(rows).sort_values(["Lift", "Confidence"], ascending=[False, False]).reset_index(drop=True)
        return res_df
        
    return pd.DataFrame(columns=[
        "Rule", "rule", "antecedents", "antecedent", "consequents", "consequent",
        "Support", "support", "Confidence", "confidence", "Lift", "lift",
        "leverage", "Interpretation", "interpretation", "item_count"
    ])
