import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data
from src.clustering import CLUSTER_DEFAULTS, kmeans, agglomerative
from src.ui import css, hero, render_top_navbar, label

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
        # Run K-Means on sample for apples-to-apples comparison
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
        color_continuous_scale="Viridis",
        opacity=0.8
    )
    fig_km.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_km, use_container_width=True)

with col_agg:
    st.markdown("#### Agglomerative Clusters")
    fig_agg = px.scatter(
        comp["agg_res"], x="PC1", y="PC2", color="Cluster",
        title=f"Agglomerative (Silhouette: {comp['agg_sil']:.3f})",
        color_continuous_scale="Turbo",
        opacity=0.8
    )
    fig_agg.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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

st.markdown("---")
st.markdown("### ⚖️ Architectural Insights: K-Means vs Agglomerative")
st.markdown(f"""
<div class="glass-card">
    <p style="color:#cbd5e1; font-size:0.92rem; margin-bottom:0;">
        • <b>Scalability:</b> K-Means scales linearly with dataset size, making it suitable for clustering all 15,000 students in ~0.5s. Agglomerative clustering requires pairwise distance matrix computations (O(n²)), making sub-sampling necessary for large cohorts.<br>
        • <b>Cluster Geometry:</b> K-Means assumes spherical, centroid-based convex partitions. Agglomerative clustering with Ward linkage creates balanced merges based on variance minimization.<br>
        • <b>Use Case:</b> Use <b>K-Means</b> for fast campus-wide cohort profiling, and <b>Agglomerative Hierarchical</b> when taxonomy and tree lineage (e.g. tiering students into academic readiness brackets) is required.
    </p>
</div>
""", unsafe_allow_html=True)
