import streamlit as st
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data
from src.data_mining import correlation, mutual_information, feature_importance, association_insights
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Data Mining & Pattern Discovery",
    "Uncover latent behavioral correlations, non-linear dependencies, tree-based feature importances, and association rules.",
    tag="Data Mining Core"
)

df = load_data()

tab_corr, tab_mi, tab_imp, tab_assoc = st.tabs([
    "📊 1. Correlation Analysis",
    "🔗 2. Mutual Information",
    "🌲 3. Random Forest Feature Importance",
    "💡 4. Association Rules (Apriori)"
])

# ----------------- TAB 1: CORRELATION ANALYSIS -----------------
with tab_corr:
    st.markdown("### 📊 Pearson Correlation with Placement")
    st.caption("Measures linear dependency between numeric candidate features and the binary placement outcome:")

    corr_df = correlation(df)
    
    col_c1, col_c2 = st.columns([1, 1], gap="medium")
    with col_c1:
        st.dataframe(corr_df.style.format({"Correlation": "{:.3f}"}), use_container_width=True)
    with col_c2:
        fig_corr = px.bar(
            corr_df.head(10), x="Correlation", y="Feature", orientation="h",
            title="Top 10 Linear Correlates with Placement",
            color="Correlation",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]]
        )
        fig_corr = base(fig_corr, "Top 10 Linear Correlates with Placement")
        fig_corr.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    **Insight:** Features such as `cgpa`, `aptitude_score`, `coding_skill_score`, and `internships_count` demonstrate the highest positive correlation with placement. Active backlogs show an inverse (negative) correlation.
    """)

# ----------------- TAB 2: MUTUAL INFORMATION -----------------
with tab_mi:
    st.markdown("### 🔗 Mutual Information (Information Gain)")
    st.caption("Non-parametric estimation of information shared between candidate features and placement:")

    if "mi_df" not in st.session_state:
        with st.spinner("Computing mutual information metrics..."):
            st.session_state.mi_df = mutual_information(df)
    mi_df = st.session_state.mi_df

    col_m1, col_m2 = st.columns([1, 1], gap="medium")
    with col_m1:
        st.dataframe(mi_df.style.format({"Mutual Information": "{:.4f}"}), use_container_width=True)
    with col_m2:
        fig_mi = px.bar(
            mi_df.head(10), x="Mutual Information", y="Feature", orientation="h",
            title="Top 10 Information Gain Contributors",
            color="Mutual Information",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]]
        )
        fig_mi = base(fig_mi, "Top 10 Information Gain Contributors")
        fig_mi.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_mi, use_container_width=True)

# ----------------- TAB 3: FEATURE IMPORTANCE -----------------
with tab_imp:
    st.markdown("### 🌲 Random Forest Gini Importance")
    st.caption("Mean decrease in node impurity across 120 decision trees:")

    if "imp_df" not in st.session_state:
        with st.spinner("Calculating tree feature importances..."):
            st.session_state.imp_df = feature_importance(df)
    imp_df = st.session_state.imp_df

    col_i1, col_i2 = st.columns([1, 1], gap="medium")
    with col_i1:
        st.dataframe(imp_df.style.format({"Importance": "{:.4f}"}), use_container_width=True)
    with col_i2:
        fig_imp = px.bar(
            imp_df.head(10), x="Importance", y="Feature", orientation="h",
            title="Top 10 Feature Importances",
            color="Importance",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]]
        )
        fig_imp = base(fig_imp, "Top 10 Feature Importances")
        fig_imp.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_imp, use_container_width=True)

# ----------------- TAB 4: ASSOCIATION RULES -----------------
with tab_assoc:
    st.markdown("### 💡 Association Pattern Insights (Apriori)")
    st.caption("Uncover frequent co-occurrence patterns, rule support, confidence, and lift:")

    assoc_df = association_insights(df)
    st.dataframe(assoc_df, use_container_width=True)

    st.info("ℹ️ Association metrics describe co-occurrence patterns; they do not prove direct causation.")

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Multi-Perspective Feature Relevance & Association Discovery",
    algorithm_name="Pearson Correlation • Mutual Information • Gini Impurity (MDI) • Association Rules (Apriori)",
    why_used=[
        ("Triangulation of Linear and Non-Linear Signals", "Standard statistical methods often rely exclusively on linear Pearson correlation (r), which fails to detect complex non-linear or threshold-driven educational dependencies. By computing non-parametric Mutual Information (quantifying shared entropy I(X;Y)) alongside Pearson coefficients, we uncover subtle non-linear dependencies that standard correlation overlooks."),
        ("Mean Decrease in Impurity (MDI) Feature Importance", "Using an ensemble of 120 decision trees, Gini Importance measures the exact average reduction in node impurity achieved by splitting on each candidate attribute. This isolates the true predictive drivers of placement readiness, preventing placement cells from over-indexing on superficial markers."),
        ("Association Rule Mining for Prescriptive Curricular Bundles", "Applying the Apriori principle on binned student credentials computes Support, Confidence, and Lift for co-occurring success criteria (e.g. {DSA >= 70, Projects >= 3} → {Placed} with Lift > 1.4). Unlike point predictions, association rules provide easily intelligible, prescriptive roadmaps that students can directly execute.")
    ],
    institutional_impact="Enables university academic committees to audit their engineering syllabus with empirical evidence, identifying which co-curricular activities directly contribute to placement success and which outdated prerequisites should be modernized.",
    dwm_concept="Feature Selection, Information Theory (Mutual Information / Entropy Gain), Gini Impurity Reduction, Association Rule Mining (Support, Confidence, Lift)."
)
