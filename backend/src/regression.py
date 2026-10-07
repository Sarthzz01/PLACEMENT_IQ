import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from .config import BASE_NUMERIC, MODEL_DIR, OUTPUT_DIR, REGRESSION_TARGETS

def train_regression(
    df,
    target_col="aptitude_score",
    slr_feature="cgpa",
    mlr_features=None,
    test_size=0.2,
    random_state=42,
    fit_intercept=True
):
    """
    Fit Simple Linear Regression (SLR) and Multiple Linear Regression (MLR).
    Computes R², MSE, RMSE, MAE, regression equation coefficients, and residual distributions.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    if mlr_features is None:
        mlr_features = [c for c in BASE_NUMERIC if c != target_col]
    mlr_features = [c for c in mlr_features if c != target_col and c in df.columns]
    
    if slr_feature not in df.columns or slr_feature == target_col:
        slr_feature = mlr_features[0]
        
    X_mlr = df[mlr_features].astype(float)
    y = df[target_col].astype(float)
    
    Xtr, Xte, ytr, yte = train_test_split(
        X_mlr, y, test_size=test_size, random_state=random_state
    )
    
    # Train SLR
    slr = LinearRegression(fit_intercept=fit_intercept).fit(Xtr[[slr_feature]], ytr)
    slr_pred = slr.predict(Xte[[slr_feature]])
    
    # Train MLR
    mlr = LinearRegression(fit_intercept=fit_intercept).fit(Xtr, ytr)
    mlr_pred = mlr.predict(Xte)
    
    rows = []
    artifacts = {}
    
    models = [
        ("Simple Linear Regression", slr, slr_pred, [slr_feature]),
        ("Multiple Linear Regression", mlr, mlr_pred, mlr_features)
    ]
    
    for name, model, pred, feats in models:
        r2 = r2_score(yte, pred)
        mse = mean_squared_error(yte, pred)
        rmse = mse ** 0.5
        mae = mean_absolute_error(yte, pred)
        residuals = (yte - pred).to_numpy()
        
        # Build readable equation
        if name.startswith("Simple"):
            coef_val = model.coef_[0]
            intercept = model.intercept_
            eq = f"y = ({coef_val:.4f} × {slr_feature}) + ({intercept:.4f})"
        else:
            eq_terms = [f"({c:.3f} × {f})" for c, f in zip(model.coef_[:3], feats[:3])]
            eq = f"y = {' + '.join(eq_terms)} + ... + ({model.intercept_:.3f})"
            
        rows.append({
            "Model": name,
            "R²": r2,
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,
            "Equation": eq
        })
        
        artifacts[name] = {
            "model": model,
            "pred": pred,
            "actual": yte.to_numpy(),
            "residuals": residuals,
            "features": feats,
            "coefficients": model.coef_,
            "intercept": model.intercept_,
            "target": target_col
        }
        
        # Save model
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        fname = "slr.joblib" if name.startswith("Simple") else "mlr.joblib"
        joblib.dump(model, MODEL_DIR / fname)
        
    out = pd.DataFrame(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT_DIR / "regression_metrics.csv", index=False)
    
    return out, artifacts
