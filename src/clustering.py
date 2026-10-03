import time
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage
from .config import BASE_NUMERIC, MODEL_DIR, OUTPUT_DIR, CLUSTER_DEFAULTS

def prepare(df, features):
    """Scale numerical feature matrix for distance-based clustering."""
    X = df[features].astype(float)
    return StandardScaler().fit_transform(X)

def elbow(df, features, k_min=2, k_max=8, n_init=10, max_iter=300, random_state=42):
    """Compute within-cluster sum of squares (inertia) across a range of K values."""
    Z = prepare(df, features)
    rows = []
    for k in range(k_min, k_max + 1):
        m = KMeans(n_clusters=k, n_init=n_init, max_iter=max_iter, random_state=random_state).fit(Z)
        rows.append({"k": k, "inertia": m.inertia_})
    return pd.DataFrame(rows)

def kmeans(df, features, k=4, init="k-means++", n_init=10, max_iter=300, random_state=42):
    """
    Run K-Means clustering.
    Returns: (projected_df, cluster_profiles, silhouette_score, model, execution_time).
    """
    t0 = time.time()
    Z = prepare(df, features)
    m = KMeans(n_clusters=k, init=init, n_init=n_init, max_iter=max_iter, random_state=random_state)
    labels = m.fit_predict(Z)
    t_fit = time.time() - t0
    
    p = PCA(n_components=2, random_state=random_state).fit_transform(Z)
    
    result = df[["placement_status", "placement_prediction"]].copy()
    if "branch" in df.columns:
        result["branch"] = df["branch"]
    if "cgpa" in df.columns:
        result["cgpa"] = df["cgpa"]
    result["Cluster"] = labels
    result["PC1"] = p[:, 0]
    result["PC2"] = p[:, 1]
    
    prof = df.copy()
    prof["Cluster"] = labels
    cols_to_profile = features + (["placement_prediction"] if "placement_prediction" in prof.columns else [])
    profile = prof.groupby("Cluster")[cols_to_profile].mean().round(3)
    
    # Save outputs
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(m, MODEL_DIR / "kmeans.joblib")
    result.to_csv(OUTPUT_DIR / "kmeans_output.csv", index=False)
    profile.to_csv(OUTPUT_DIR / "kmeans_cluster_profiles.csv")
    
    sil = float(silhouette_score(Z, labels, sample_size=min(5000, len(Z)), random_state=random_state))
    return result, profile, sil, m, t_fit

def agglomerative(
    df,
    features,
    k=4,
    sample_size=3000,
    linkage_method="ward",
    metric="euclidean",
    random_state=42
):
    """
    Run Agglomerative Hierarchical clustering on a representative sample.
    Returns: (projected_df, cluster_profiles, silhouette_score, model, execution_time).
    """
    t0 = time.time()
    sample = df.sample(min(sample_size, len(df)), random_state=random_state).copy()
    Z = prepare(sample, features)
    
    if linkage_method == "ward":
        metric = "euclidean"
        
    m = AgglomerativeClustering(n_clusters=k, linkage=linkage_method, metric=metric)
    labels = m.fit_predict(Z)
    t_fit = time.time() - t0
    
    p = PCA(n_components=2, random_state=random_state).fit_transform(Z)
    
    sample["Cluster"] = labels
    sample["PC1"] = p[:, 0]
    sample["PC2"] = p[:, 1]
    
    cols_to_profile = features + (["placement_prediction"] if "placement_prediction" in sample.columns else [])
    profile = sample.groupby("Cluster")[cols_to_profile].mean().round(3)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample[["placement_status", "placement_prediction", "Cluster", "PC1", "PC2"]].to_csv(
        OUTPUT_DIR / "agglomerative_output.csv", index=False
    )
    profile.to_csv(OUTPUT_DIR / "agglomerative_cluster_profiles.csv")
    
    sil = float(silhouette_score(Z, labels, sample_size=min(3000, len(Z)), random_state=random_state))
    return sample, profile, sil, m, t_fit

def dendrogram_data(df, features, sample_size=300, method="ward", random_state=42):
    """Compute linkage matrix for hierarchical dendrogram visualization."""
    sample = df.sample(min(sample_size, len(df)), random_state=random_state)
    Z = prepare(sample, features)
    return linkage(Z, method=method)
