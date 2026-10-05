import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data
from src.clustering import CLUSTER_DEFAULTS, kmeans, agglomerative
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Cluster Model Comparison: K-Means vs Agglomerative",
    "Side-by-side benchmarking of Partition-based (K-Means) and Hierarchical (Agglomerative) student segmentation.",
    tag="Clustering Benchmark"
)

df = load_data()

with st.sidebar:
    st.markdown("### ⚙️ Benchmark Parameters")
    features = st.multiselect("Clustering Features", CLUSTER_DEFAULTS, default=CLUSTER_DEFAULTS[:8], format_func=label)
    k_val = st.slider("Shared Cluster Count (K)", 2, 8, 4)
    sample_size = st.slider("Comparison Sample Size", 1000, 5000, 3000, 500)
    seed = st.number_input("Random Seed", 0, 9999, 42)

if len(features) < 2:
    st.warning("Please select at least 2 features.")
    st.stop()

if st.button("🚀 Run Side-by-Side Comparison", type="primary") or "cluster_comp" not in st.session_state:
    with st.spinner("Training both K-Means and Agglomerative clustering algorithms..."):
        sample_df = df.sample(min(sample_size, len(df)), random_state=seed).copy()
        km_res, km_prof, km_sil, km_model, km_time = kmeans(sample_df, features, k=k_val, random_state=seed)
        agg_res, agg_prof, agg_sil, agg_model, agg_time = agglomerative(sample_df, features, k=k_val, sample_size=sample_size, random_state=seed)
        
        st.session_state.cluster_comp = {
            "km_sil": km_sil, "km_time": km_time, "km_res": km_res, "km_prof": km_prof,
            "agg_sil": agg_sil, "agg_time": agg_time, "agg_res": agg_res, "agg_prof": agg_prof,
            "k": k_val, "sample": len(sample_df), "features": features
        }

comp = st.session_state.cluster_comp

st.markdown("### 📊 Side-by-Side Metrics Benchmark")
comp_df = pd.DataFrame([
    {
        "Algorithm": "K-Means (Partitioning)",
        "Clusters (K)": comp["k"],
        "Silhouette Score": f"{comp['km_sil']:.4f}",
        "Execution Time (s)": f"{comp['km_time']:.3f}",
        "Sample Evaluated": f"{comp['sample']:,}",
        "Complexity": "O(k × n × iterations)"
    },
    {
        "Algorithm": "Agglomerative (Hierarchical)",
        "Clusters (K)": comp["k"],
        "Silhouette Score": f"{comp['agg_sil']:.4f}",
        "Execution Time (s)": f"{comp['agg_time']:.3f}",
        "Sample Evaluated": f"{comp['sample']:,}",
        "Complexity": "O(n² log n)"
    }
])
st.dataframe(comp_df, use_container_width=True)

# 2D PCA Projections Side-by-Side
st.markdown("### 🌌 PCA 2D Cluster Visualization Comparison")
col_km, col_agg = st.columns(2)

with col_km:
    st.markdown("#### K-Means Clusters")
    fig_km = px.scatter(
        comp["km_res"], x="PC1", y="PC2", color="Cluster",
        title=f"K-Means (Silhouette: {comp['km_sil']:.3f})",
        color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#38BDF8"], [1, "#1D4ED8"]],
        opacity=0.8
    )
    fig_km = base(fig_km, f"K-Means (Silhouette: {comp['km_sil']:.3f})")
    st.plotly_chart(fig_km, use_container_width=True)

with col_agg:
    st.markdown("#### Agglomerative Clusters")
    fig_agg = px.scatter(
        comp["agg_res"], x="PC1", y="PC2", color="Cluster",
        title=f"Agglomerative (Silhouette: {comp['agg_sil']:.3f})",
        color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#34D399"], [1, "#047857"]],
        opacity=0.8
    )
    fig_agg = base(fig_agg, f"Agglomerative (Silhouette: {comp['agg_sil']:.3f})")
    st.plotly_chart(fig_agg, use_container_width=True)

# Cluster Size Distribution Comparison
st.markdown("### 📊 Cluster Size Distribution")
c_s1, c_s2 = st.columns(2)
with c_s1:
    st.markdown("**K-Means Student Distribution:**")
    st.dataframe(comp["km_res"]["Cluster"].value_counts().sort_index().rename("K-Means Students"), use_container_width=True)
with c_s2:
    st.markdown("**Agglomerative Student Distribution:**")
    st.dataframe(comp["agg_res"]["Cluster"].value_counts().sort_index().rename("Agglomerative Students"), use_container_width=True)

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Comparative Clustering Evaluation & Algorithmic Validation",
    algorithm_name="Partitional (K-Means) vs. Hierarchical (Agglomerative) Benchmarking",
    why_used=[
        ("Cross-Algorithmic Structural Validation", "Data mining best practices dictate that unsupervised clusters should never be accepted based on a single heuristic. Benchmarking centroid-based partitioning (K-Means) against variance-minimizing hierarchical agglomeration (Ward) provides cross-algorithmic validation: if student groupings consistently emerge across both distinct mathematical frameworks, we prove they represent genuine educational phenotypes rather than algorithmic artifacts."),
        ("Trade-Off Analysis: Linear Scalability vs Hierarchical Depth", "K-Means operates in O(n · K · I) time complexity, enabling real-time clustering across all 15,000+ candidates instantaneously in production. Conversely, Agglomerative clustering exhibits O(n² log n) complexity with quadratic memory requirements, making it computationally heavy for real-time web inference but invaluable for periodic deep academic curriculum reviews where tree hierarchy is essential."),
        ("Geometric Shape & Cluster Balance Diagnostics", "Comparing PCA cluster projections side-by-side demonstrates how K-Means enforces Voronoi tessellations (convex hulls around centroids), whereas Ward's agglomerative approach flexibly merges local density structures, preventing single-student outlier distortion.")
    ],
    institutional_impact="Provides placement deans and academic boards with rigorous evidence of cohort stability before enacting strategic training policies, ensuring interventions target robust candidate groups rather than unstable statistical noise.",
    dwm_concept="Partitional vs Hierarchical Taxonomy, Time & Space Complexity Trade-Offs, Silhouette Metric Comparison, Voronoi Convexity vs Pairwise Linkage."
)
