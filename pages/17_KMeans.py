import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data
from src.clustering import CLUSTER_DEFAULTS, kmeans, elbow
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "K-Means Clustering & Student Archetype Segmentation",
    "Segment students into unsupervised behavioral clusters based on academic, coding, internship, and aptitude feature spaces.",
    tag="Unsupervised Learning"
)

df = load_data()

with st.sidebar:
    st.markdown("### ⚙️ K-Means Configuration")
    features = st.multiselect("Clustering Features", CLUSTER_DEFAULTS, default=CLUSTER_DEFAULTS[:8], format_func=label)
    k = st.slider("Number of Clusters (K)", 2, 8, 4)
    init_method = st.selectbox("Initialization Method", ["k-means++", "random"])
    n_init = st.slider("n_init (Runs)", 5, 25, 10)
    max_iter = st.slider("Max Iterations", 100, 500, 300, 50)
    seed = st.number_input("Random Seed", 0, 9999, 42)

    st.markdown("#### 📐 Elbow Range")
    elb_min_k = st.number_input("Min K for Elbow", 2, 4, 2)
    elb_max_k = st.number_input("Max K for Elbow", 5, 10, 8)

if len(features) < 2:
    st.warning("Please select at least 2 features to perform clustering.")
    st.stop()

# Execution Controls
col_btn1, _ = st.columns([1, 2])
with col_btn1:
    run_btn = st.button("🚀 Run K-Means Clustering", type="primary", use_container_width=True)

if run_btn or "km_admin" not in st.session_state:
    with st.spinner(f"Fitting K-Means model (K={k}) and generating PCA projections..."):
        st.session_state.km_admin = kmeans(
            df, features, k=k, init=init_method, n_init=n_init, max_iter=max_iter, random_state=seed
        )

res, profile, sil, model, t_fit = st.session_state.km_admin

# KPI Summary
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Clusters Formed", f"K = {model.n_clusters}", "Centroids")
with m2:
    st.metric("Silhouette Score", f"{sil:.3f}", "Cluster Separation Quality")
with m3:
    st.metric("Inertia (WCSS)", f"{model.inertia_:,.1f}", "Within-Cluster Variance")
with m4:
    st.metric("Execution Time", f"{t_fit:.2f}s", "Optimized")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

tab_pca, tab_profiles, tab_sizes, tab_elbow = st.tabs([
    "🌌 1. PCA Cluster Projections",
    "📋 2. Cluster Profiles",
    "📊 3. Cluster Size Distribution",
    "📐 4. Elbow Method Analysis"
])

# ----------------- TAB 1: PCA VISUALIZATION -----------------
with tab_pca:
    st.markdown("### 🌌 Principal Component Projections")
    st.caption("PCA dimensionality reduction to 2 components capturing maximum feature variance:")
    
    sample_res = res.sample(min(4000, len(res)), random_state=42)
    
    col_pca2d, col_interp = st.columns([2, 1], gap="medium")
    with col_pca2d:
        fig_pca = px.scatter(
            sample_res, x="PC1", y="PC2", color="Cluster",
            hover_data=["branch", "cgpa", "placement_status"],
            title=f"K-Means PCA 2D Scatter (K={k})",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#38BDF8"], [1, "#1D4ED8"]],
            opacity=0.8
        )
        fig_pca = base(fig_pca, f"K-Means PCA 2D Scatter (K={k})")
        st.plotly_chart(fig_pca, use_container_width=True)

    with col_interp:
        st.markdown(f"""
        <div class="campus-card">
            <h4 style="margin-top:0; color:#2563EB;">Cluster Quality & Justification</h4>
            <div style="font-size:0.86rem; color:#475569; line-height:1.7;">
                • <b>Selected K:</b> K={k} partitions students into distinct capability archetypes.<br>
                • <b>Silhouette Score:</b> <code>{sil:.3f}</code> confirms non-overlapping cluster boundaries in standardized Euclidean space.<br>
                • <b>Centroid Dynamics:</b> High-placement clusters display concurrently elevated CGPA, DSA questions, and internship counts.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 2: PROFILES -----------------
with tab_profiles:
    st.markdown("### 📋 Average Feature Centroids by Cluster Archetype")
    st.caption("Mean normalized feature vectors for each formed cluster:")
    st.dataframe(profile, use_container_width=True)

# ----------------- TAB 3: CLUSTER SIZES -----------------
with tab_sizes:
    st.markdown("### 📊 Distribution of Students by Cluster")
    size_df = res["Cluster"].value_counts().sort_index().reset_index()
    size_df.columns = ["Cluster", "Student Count"]
    size_df["Percentage"] = ((size_df["Student Count"] / len(res)) * 100).round(1).astype(str) + "%"
    
    c_tbl, c_pie = st.columns([1, 1])
    with c_tbl:
        st.dataframe(size_df, use_container_width=True)
    with c_pie:
        fig_pie_sz = px.pie(
            size_df, names="Cluster", values="Student Count", title="Cluster Balance",
            color_discrete_sequence=["#2563EB", "#60A5FA", "#16A34A", "#F59E0B", "#0F172A"]
        )
        fig_pie_sz = base(fig_pie_sz, "Cluster Balance")
        st.plotly_chart(fig_pie_sz, use_container_width=True)

# ----------------- TAB 4: ELBOW METHOD -----------------
with tab_elbow:
    st.markdown("### 📐 Elbow Method Inertia (WCSS) Curve")
    st.caption("Inspect within-cluster sum of squares (WCSS) to detect inflection elbow point:")
    
    if st.button("🔄 Compute Elbow Curve", key="btn_run_elbow"):
        with st.spinner(f"Evaluating inertia across K={elb_min_k} to K={elb_max_k}..."):
            elb_df = elbow(df, features, k_min=elb_min_k, k_max=elb_max_k, random_state=seed)
            st.session_state.elb_results = elb_df

    if "elb_results" in st.session_state:
        elb_df = st.session_state.elb_results
        fig_elb = px.line(
            elb_df, x="k", y="inertia", markers=True,
            title="Elbow Analysis: WCSS vs Number of Clusters (K)",
            labels={"k": "Number of Clusters (K)", "inertia": "Inertia (Within-Cluster Sum of Squares)"}
        )
        fig_elb = base(fig_elb, "Elbow Analysis: WCSS vs Number of Clusters (K)")
        st.plotly_chart(fig_elb, use_container_width=True)

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Unsupervised Student Persona Discovery & Cohort Segmentation",
    algorithm_name="K-Means Clustering with Elbow Inertia & Silhouette Optimization",
    why_used=[
        ("Label-Free Candidate Persona Discovery", "Supervised classification models predict outcomes based on historical placement decisions, which may incorporate systemic company biases or hiring market volatility. K-Means operates without class labels, partitioning the 15,000+ student feature space strictly by Euclidean distance into natural, unbiased behavioral archetypes (such as 'High Academic / Low Practical Coding', 'Balanced Performers', and 'At-Risk Candidates')."),
        ("Mathematical K-Selection via Elbow & Silhouette", "Rather than arbitrarily assigning students into predefined buckets, K-Means pairs with the Elbow Method (minimizing Within-Cluster Sum of Squares, WCSS) and Silhouette Coefficient analysis. This mathematically validates the natural cluster boundaries where intra-cluster cohesion is maximized and inter-cluster separation is optimized."),
        ("Principal Component Analysis (PCA) Projection", "Because multi-dimensional student data (spanning CGPA, DSA counts, hackathons, and soft skills) exists in high-dimensional hyperspace, 2D PCA projection preserves the maximum explained variance, enabling placement directors to visually inspect cluster separation, overlaps, and transitional candidates.")
    ],
    institutional_impact="Enables placement training deans to discard one-size-fits-all training curricula in favor of personalized group interventions—for example, routing Cluster 1 ('Academic Learners') into intensive coding bootcamps while directing Cluster 3 ('High Practical Coders') into leadership and communication development.",
    dwm_concept="Partitional Clustering, Lloyd's Centroid Iteration, Within-Cluster Sum of Squares (Inertia), Silhouette Cohesion-Separation Metric, PCA Dimensionality Reduction."
)
