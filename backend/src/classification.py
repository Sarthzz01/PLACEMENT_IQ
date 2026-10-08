import time
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve, average_precision_score
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from .preprocessing import model_matrix
from .config import MODEL_DIR, OUTPUT_DIR

def train_models(
    df,
    test_size=0.2,
    random_state=42,
    dt_depth=6,
    dt_criterion="gini",
    dt_min_split=2,
    dt_min_leaf=1,
    rf_estimators=150,
    rf_depth=10,
    rf_min_split=2,
    rf_min_leaf=1,
    rf_max_features="sqrt",
    gb_estimators=100,
    gb_depth=3,
    gb_learning_rate=0.1,
    lr_max_iter=1000,
    lr_C=1.0,
    nb_var_smoothing=1e-9
):
    """
    Train 5 diverse classification models (Random Forest, Gradient Boosting, Decision Tree,
    Logistic Regression, and Gaussian Naive Bayes) with customizable hyperparameters.
    Computes all standard DWM classification metrics, ROC & PR curves, feature importances, and execution times.
    """
    X, y, features = model_matrix(df)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=rf_estimators,
            max_depth=rf_depth,
            min_samples_split=rf_min_split,
            min_samples_leaf=rf_min_leaf,
            max_features=rf_max_features,
            random_state=random_state,
            n_jobs=-1,
            class_weight="balanced"
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=gb_estimators,
            max_depth=gb_depth,
            learning_rate=gb_learning_rate,
            random_state=random_state
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=dt_depth,
            criterion=dt_criterion,
            min_samples_split=dt_min_split,
            min_samples_leaf=dt_min_leaf,
            random_state=random_state,
            class_weight="balanced"
        ),
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(
                max_iter=lr_max_iter,
                C=lr_C,
                random_state=random_state,
                class_weight="balanced"
            ))
        ]),
        "Naive Bayes": Pipeline([
            ("scaler", StandardScaler()),
            ("model", GaussianNB(var_smoothing=nb_var_smoothing))
        ])
    }
    
    metrics = []
    artifacts = {}
    
    for name, m in models.items():
        t0 = time.time()
        m.fit(Xtr, ytr)
        t_fit = time.time() - t0
        
        pred = m.predict(Xte)
        prob = m.predict_proba(Xte)[:, 1]
        
        acc = accuracy_score(yte, pred)
        prec = precision_score(yte, pred, zero_division=0)
        rec = recall_score(yte, pred, zero_division=0)
        f1 = f1_score(yte, pred, zero_division=0)
        auc = roc_auc_score(yte, prob)
        
        fpr, tpr, _ = roc_curve(yte, prob)
        pr_prec, pr_rec, _ = precision_recall_curve(yte, prob)
        pr_auc = average_precision_score(yte, prob)
        
        # Feature importances
        feat_imp = None
        if hasattr(m, "feature_importances_"):
            feat_imp = pd.DataFrame({
                "Feature": features,
                "Importance": m.feature_importances_
            }).sort_values("Importance", ascending=False)
        elif hasattr(m, "named_steps") and hasattr(m.named_steps.get("model", None), "coef_"):
            coefs = np.abs(m.named_steps["model"].coef_[0])
            feat_imp = pd.DataFrame({
                "Feature": features,
                "Importance": coefs / (coefs.sum() if coefs.sum() > 0 else 1.0)
            }).sort_values("Importance", ascending=False)
        elif hasattr(m, "coef_"):
            coefs = np.abs(m.coef_[0])
            feat_imp = pd.DataFrame({
                "Feature": features,
                "Importance": coefs / (coefs.sum() if coefs.sum() > 0 else 1.0)
            }).sort_values("Importance", ascending=False)
            
        metrics.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1": f1,
            "ROC-AUC": auc,
            "Training Time (s)": round(t_fit, 3)
        })
        
        artifacts[name] = {
            "model": m,
            "pred": pred,
            "prob": prob,
            "cm": confusion_matrix(yte, pred),
            "report": classification_report(yte, pred, output_dict=True),
            "fpr": fpr,
            "tpr": tpr,
            "roc_auc": auc,
            "pr_prec": pr_prec,
            "pr_rec": pr_rec,
            "pr_auc": pr_auc,
            "feature_importance": feat_imp,
            "features": features
        }
        
        # Save trained artifact
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(m, MODEL_DIR / f"{name.lower().replace(' ', '_')}.joblib")
        
    out = pd.DataFrame(metrics)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT_DIR / "classification_metrics.csv", index=False)
    
    return out, artifacts, yte.reset_index(drop=True)
