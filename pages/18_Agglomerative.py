import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from src.auth import require_admin
from src.preprocessing import load_data
from src.clustering import CLUSTER_DEFAULTS, agglomerative, dendrogram_data
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Agglomerative Hierarchical Clustering",
    "Bottom-up hierarchical clustering with dendrogram visualization, custom distance metrics, and linkage criteria.",
    tag="Hierarchical Segmentation"
)

df = load_data()

with st.sidebar:
    st.markdown("### ⚙️ Agglomerative Settings")
    features = st.multiselect("Clustering Features", CLUSTER_DEFAULTS, default=CLUSTER_DEFAULTS[:8], format_func=label)
    k = st.slider("Number of Clusters (Cut Level)", 2, 8, 4)
    sample_size = st.slider("Clustering Sample Size", 500, 4000, 2000, 500)
    linkage_method = st.selectbox("Linkage Method", ["ward", "complete", "average", "single"])
    metric = st.selectbox("Distance Metric", ["euclidean", "manhattan", "cosine"])
    dendro_sample = st.slider("Dendrogram Sample Size", 100, 500, 250, 50)
    seed = st.number_input("Random Seed", 0, 9999, 42)

if linkage_method == "ward":
    metric = "euclidean"
    st.caption("ℹ️ Ward linkage requires Euclidean distance metric; set automatically.")

if len(features) < 2:
    st.warning("Please select at least 2 features to perform clustering.")
    st.stop()

if st.button("🚀 Run Agglomerative Clustering", type="primary") or "agg_admin" not in st.session_state:
    with st.spinner(f"Running hierarchical clustering on {sample_size:,} student sample..."):
        st.session_state.agg_admin = agglomerative(
            df, features, k=k, sample_size=sample_size,
            linkage_method=linkage_method, metric=metric, random_state=seed
        )

sample_df, profile, sil, model, t_fit = st.session_state.agg_admin

# KPI Summary
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Clusters Formed", f"K = {k}", f"Linkage: {linkage_method}")
with m2:
    st.metric("Silhouette Score", f"{sil:.3f}", "Cluster Quality")
with m3:
    st.metric("Sample Size", f"{len(sample_df):,}", "Students")
with m4:
    st.metric("Execution Time", f"{t_fit:.2f}s", "Hierarchical")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

tab_dendro, tab_pca, tab_prof, tab_sizes = st.tabs([
    "🌳 1. Hierarchical Dendrogram",
    "🌌 2. PCA 2D Cluster Projection",
    "📋 3. Cluster Profiles",
    "📊 4. Cluster Size Distribution"
])

with tab_dendro:
    st.markdown("### 🌳 Hierarchical Clustering Dendrogram")
    st.caption(f"Visualizes tree merges across {dendro_sample} student records using {linkage_method} linkage:")
    
    with st.spinner("Generating dendrogram linkage tree..."):
        Z = dendrogram_data(df, features, sample_size=dendro_sample, method=linkage_method, random_state=seed)
        fig, ax = plt.subplots(figsize=(10, 4.5))
        dendrogram(Z, no_labels=True, ax=ax, color_threshold=0.7 * max(Z[:, 2]))
        ax.set_title(f"Agglomerative Dendrogram ({linkage_method.title()} Linkage)", color="#0F172A", fontsize=13, fontweight="bold")
        ax.set_xlabel("Student Index", color="#64748B", fontsize=11)
        ax.set_ylabel("Linkage Distance", color="#64748B", fontsize=11)
        ax.tick_params(colors="#64748B")
        for spine in ax.spines.values():
            spine.set_color("#E2E8F0")
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')
        st.pyplot(fig)
        plt.close(fig)

with tab_pca:
    st.markdown("### 🌌 2D Principal Component Projection")
    fig_pca = px.scatter(
        sample_df, x="PC1", y="PC2", color="Cluster",
        title=f"Agglomerative PCA Projection (K={k})",
        color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#38BDF8"], [1, "#1D4ED8"]],
        opacity=0.8
    )
    fig_pca = base(fig_pca, f"Agglomerative PCA Projection (K={k})")
    st.plotly_chart(fig_pca, use_container_width=True)

with tab_prof:
    st.markdown("### 📋 Average Centroids by Hierarchical Cluster")
    st.dataframe(profile, use_container_width=True)

with tab_sizes:
    st.markdown("### 📊 Distribution of Sample Students by Cluster")
    size_df = sample_df["Cluster"].value_counts().sort_index().reset_index()
    size_df.columns = ["Cluster", "Student Count"]
    size_df["Percentage"] = ((size_df["Student Count"] / len(sample_df)) * 100).round(1).astype(str) + "%"
    st.dataframe(size_df, use_container_width=True)

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Bottom-Up Hierarchical Taxonomy & Multi-Level Skill Clustering",
    algorithm_name=f"Agglomerative Hierarchical Clustering ({linkage_method.title()} Linkage, K={k})",
    why_used=[
        ("Nested Hierarchical Skill Taxonomy", "Unlike flat partitional algorithms like K-Means which impose rigid sphere boundaries, Agglomerative Hierarchical Clustering begins with each candidate in their own singleton cluster and recursively merges nearest pairs based on Ward's variance minimization criterion. This constructs a complete phylogenetic-style dendrogram of student capabilities."),
        ("Continuous Multi-Granular Inspection", "Placement drives feature diverse hiring profiles—from specialized R&D roles seeking niche algorithmic depth to mass IT recruitment hiring generalists. By examining the dendrogram at variable horizontal cut thresholds (cophenetic distance), placement directors can inspect fine-grained micro-specializations (e.g. Competitive Coders vs Full-Stack Developers) or broad macro cohorts without re-running the model."),
        ("Validation of Partitioned Boundaries", "Comparing bottom-up hierarchical agglomerations against top-down K-Means centroids verifies whether identified student clusters are genuine natural structures in the educational data or mathematical artifacts of the K-Means distance function.")
    ],
    institutional_impact=f"Achieved a measured silhouette quality score of {sil:.3f} across the representative sample of {sample_size:,} candidates. Provides placement departments with an intuitive visual roadmap of how student skill profiles naturally coalesce, allowing recruiters from different market tiers (mass vs super-dream) to easily target cohorts at appropriate dendrogram cut depths.",
    dwm_concept="Hierarchical Clustering, Agglomerative Bottom-Up Merge, Ward Linkage Variance Optimization, Cophenetic Distance, Dendrogram Interpretation."
)
