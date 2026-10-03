import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from src.auth import require_admin
from src.preprocessing import load_data
from src.clustering import CLUSTER_DEFAULTS, agglomerative, dendrogram_data
from src.ui import css, hero, render_top_navbar, label

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
        ax.set_title(f"Agglomerative Dendrogram ({linkage_method.title()} Linkage)", color="#f8fafc")
        ax.set_xlabel("Student Index", color="#94a3b8")
        ax.set_ylabel("Linkage Distance", color="#94a3b8")
        ax.tick_params(colors="#94a3b8")
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        st.pyplot(fig)
        plt.close(fig)

with tab_pca:
    st.markdown("### 🌌 2D Principal Component Projection")
    fig_pca = px.scatter(
        sample_df, x="PC1", y="PC2", color="Cluster",
        title=f"Agglomerative PCA Projection (K={k})",
        color_continuous_scale="Turbo",
        opacity=0.8
    )
    fig_pca.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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

# Technical Justification
st.markdown("---")
st.markdown("### ⚖️ Technical Hierarchical Clustering Justification")
st.markdown(f"""
<div class="glass-card" style="border-left: 4px solid #a855f7;">
    <h4 style="margin-top:0; color:#c084fc;">Hierarchical Agglomeration Evaluation</h4>
    <p style="color:#cbd5e1; font-size:0.92rem; margin-bottom:0;">
        • <b>Linkage Criteria:</b> <b>{linkage_method.title()}</b> linkage minimizes intra-cluster distance variance at each pairwise merge step.<br>
        • <b>Silhouette Quality:</b> Measured silhouette score of <b>{sil:.3f}</b> on the representative sample of <b>{sample_size:,} students</b>.<br>
        • <b>Tree Interpretability:</b> Unlike flat partition models, the hierarchical dendrogram provides a full continuum of groupings, allowing placement cells to trace granular student subgroups up into broader placement tiers.
    </p>
</div>
""", unsafe_allow_html=True)
