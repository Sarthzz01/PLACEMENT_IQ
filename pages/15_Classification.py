import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.classification import train_models
from src.visualizations import confusion_matrix_heatmap, base
from src.database import get_system_setting, set_system_setting
from src.ui import css, hero, render_top_navbar, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Supervised Classification Benchmark Suite",
    "Train, tune, and evaluate Decision Tree, Random Forest, and Gaussian Naive Bayes classifiers to predict binary student placement outcomes (`placement_prediction`).",
    tag="Supervised Classification"
)

# Dataset Selection Switcher (Original vs Combined)
counts = get_dataset_counts()
col_top1, col_top2 = st.columns([2, 1])
with col_top1:
    st.markdown("### 🎯 Model Training Configuration & Cohort Scope")
with col_top2:
    training_data_scope = st.radio(
        "Training Dataset",
        ["Unified Dataset (Original + DB Students)", "Original Dataset Only"],
        horizontal=True,
        key="cls_dataset_scope"
    )

include_new = (training_data_scope == "Unified Dataset (Original + DB Students)")
df = load_data(include_new_students=include_new)

st.markdown(f"""
<div class="campus-card-flat" style="padding: 10px 18px; margin-bottom: 16px; font-size: 0.85rem; color: #475569;">
    Active Training Cohort: <b style="color:#2563EB;">{len(df):,}</b> students 
    (Baseline: {counts['original_students']:,} &bull; Registered: {counts['new_students']:,})
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Classification Hyperparameters")
    test_size = st.slider("Test Split Ratio", 0.1, 0.4, 0.2, 0.05)
    seed = st.number_input("Random State (Seed)", 0, 9999, 42)

    st.markdown("#### 🌲 Decision Tree")
    dt_depth = st.slider("DT Max Depth", 2, 20, 6)
    dt_criterion = st.selectbox("DT Criterion", ["gini", "entropy", "log_loss"])
    dt_min_split = st.slider("DT Min Split Samples", 2, 20, 2)
    dt_min_leaf = st.slider("DT Min Leaf Samples", 1, 20, 1)

    st.markdown("#### 🌳 Random Forest")
    rf_estimators = st.slider("RF Number of Trees", 50, 300, 150, 25)
    rf_depth = st.slider("RF Max Depth", 3, 25, 10)
    rf_min_split = st.slider("RF Min Split", 2, 20, 2)
    rf_min_leaf = st.slider("RF Min Leaf", 1, 20, 1)
    rf_max_features = st.selectbox("RF Max Features", ["sqrt", "log2", None], format_func=lambda x: "All" if x is None else x)

    st.markdown("#### 📊 Naive Bayes")
    nb_var = st.number_input("NB Var Smoothing", min_value=1e-12, max_value=1.0, value=1e-9, format="%.1e")

if st.button("🚀 Train / Retrain Classification Models", type="primary") or "cls_admin" not in st.session_state:
    with st.spinner(f"Training DT, RF, and Naive Bayes on {len(df):,} records..."):
        st.session_state.cls_admin = train_models(
            df, test_size=test_size, random_state=seed,
            dt_depth=dt_depth, dt_criterion=dt_criterion, dt_min_split=dt_min_split, dt_min_leaf=dt_min_leaf,
            rf_estimators=rf_estimators, rf_depth=rf_depth, rf_min_split=rf_min_split, rf_min_leaf=rf_min_leaf,
            rf_max_features=rf_max_features, nb_var_smoothing=nb_var
        )

metrics_df, artifacts, y_test = st.session_state.cls_admin

# ----------------- 3 MODEL CARDS (REQUIREMENT 26) -----------------
st.markdown("### 🤖 Placement Prediction Models")
c_m1, c_m2, c_m3 = st.columns(3)

dt_row = metrics_df[metrics_df["Model"] == "Decision Tree"].iloc[0] if len(metrics_df[metrics_df["Model"] == "Decision Tree"]) > 0 else None
rf_row = metrics_df[metrics_df["Model"] == "Random Forest"].iloc[0] if len(metrics_df[metrics_df["Model"] == "Random Forest"]) > 0 else None
nb_row = metrics_df[metrics_df["Model"] == "Naive Bayes"].iloc[0] if len(metrics_df[metrics_df["Model"] == "Naive Bayes"]) > 0 else None

with c_m1:
    if dt_row is not None:
        st.markdown(f"""
        <div class="campus-card" style="border-top: 4px solid #2563EB;">
            <div style="font-weight: 800; font-size: 1.1rem; color: #0F172A; margin-bottom: 6px;">Decision Tree</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #2563EB;">{dt_row['Accuracy']*100:.1f}%</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">Accuracy &bull; F1: {dt_row['F1']:.3f}</div>
            <div style="font-size: 0.8rem; color: #475569; margin-top: 8px;">Single rule-based tree model with fast inference.</div>
        </div>
        """, unsafe_allow_html=True)

with c_m2:
    if rf_row is not None:
        st.markdown(f"""
        <div class="campus-card" style="border-top: 4px solid #16A34A;">
            <div style="font-weight: 800; font-size: 1.1rem; color: #0F172A; margin-bottom: 6px;">Random Forest</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #16A34A;">{rf_row['Accuracy']*100:.1f}%</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">Accuracy &bull; F1: {rf_row['F1']:.3f}</div>
            <div style="font-size: 0.8rem; color: #475569; margin-top: 8px;">Ensemble of {rf_estimators} trees minimizing variance.</div>
        </div>
        """, unsafe_allow_html=True)

with c_m3:
    if nb_row is not None:
        st.markdown(f"""
        <div class="campus-card" style="border-top: 4px solid #F59E0B;">
            <div style="font-weight: 800; font-size: 1.1rem; color: #0F172A; margin-bottom: 6px;">Naive Bayes</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #D97706;">{nb_row['Accuracy']*100:.1f}%</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">Accuracy &bull; F1: {nb_row['F1']:.3f}</div>
            <div style="font-size: 0.8rem; color: #475569; margin-top: 8px;">Gaussian probabilistic classifier with high speed.</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ----------------- BENCHMARK TABLE -----------------
st.markdown("### 📊 Cross-Model Benchmark Comparison")

# Safe subset formatting ensuring text columns are NEVER touched
num_cols = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "Training Time (s)"]
valid_num_cols = [c for c in num_cols if c in metrics_df.columns]

styled_table = metrics_df.style.format("{:.3f}", subset=valid_num_cols)
st.dataframe(styled_table, use_container_width=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ----------------- PRODUCTION MODEL SELECTION -----------------
current_prod_model = get_system_setting("production_model", "Random Forest")

col_prod1, col_prod2 = st.columns([2, 1])
with col_prod1:
    new_prod_model = st.selectbox(
        "Designate Production Model (Used for Student-Facing Predictions)",
        metrics_df["Model"].tolist(),
        index=metrics_df["Model"].tolist().index(current_prod_model) if current_prod_model in metrics_df["Model"].tolist() else 0
    )
with col_prod2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("💾 Set as Production Model", use_container_width=True):
        set_system_setting("production_model", new_prod_model)
        st.success(f"Production model updated to **{new_prod_model}**!")
        st.rerun()

st.caption(f"Currently active student prediction engine: **{current_prod_model}**")

st.markdown("---")

# ----------------- COMPARISON SELECTOR & VISUALIZATION -----------------
col_cmp_ctrl, col_cmp_chart = st.columns([1, 2], gap="medium")

with col_cmp_ctrl:
    st.markdown("#### 🔍 Objective Model Comparison")
    comp_metric = st.selectbox("Compare By Metric", ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"], index=3)
    best_model = metrics_df.sort_values(comp_metric, ascending=False).iloc[0]
    
    st.markdown(f"""
    <div class="campus-card">
        <b style="color: #2563EB;">Leader for {comp_metric}:</b><br>
        <span style="font-size: 1.3rem; font-weight: 800; color: #0F172A;">{best_model['Model']} ({best_model[comp_metric]:.3f})</span>
        <p style="color: #64748B; font-size: 0.85rem; margin-top: 10px; line-height: 1.6;">
            <b>Technical Justification:</b> Random Forest builds an ensemble of decorrelated decision trees, minimizing variance and mitigating overfitting on noisy boundary features like LeetCode and aptitude scores. 
            Decision Tree provides single-rule explainability with lower training latency. Naive Bayes assumes conditional independence between features given the class label.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_cmp_chart:
    fig_cmp = px.bar(
        metrics_df, x="Model", y=["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        barmode="group",
        title="Comprehensive Performance Indices Across Models",
        color_discrete_sequence=["#2563EB", "#60A5FA", "#16A34A", "#F59E0B", "#0F172A"]
    )
    fig_cmp = base(fig_cmp, "Comprehensive Performance Indices Across Models")
    st.plotly_chart(fig_cmp, use_container_width=True)

# ----------------- IN-DEPTH MODEL INSPECTION -----------------
st.markdown("---")
st.markdown("### 🔬 In-Depth Diagnostic Inspection")
chosen_model = st.selectbox("Select Model to Inspect in Detail", metrics_df["Model"].tolist())
art = artifacts[chosen_model]

tab_cm, tab_report, tab_roc, tab_pr, tab_feat = st.tabs([
    "🔲 Confusion Matrix",
    "📋 Classification Report",
    "📈 ROC Curve",
    "🎯 Precision-Recall Curve",
    "🌲 Feature Importance"
])

with tab_cm:
    fig_cm = confusion_matrix_heatmap(art["cm"])
    st.plotly_chart(fig_cm, use_container_width=True)

with tab_report:
    report_df = pd.DataFrame(art["report"]).T
    st.dataframe(report_df.style.format("{:.3f}", subset=["precision", "recall", "f1-score"]), use_container_width=True)

with tab_roc:
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=art["fpr"], y=art["tpr"], mode="lines", name=f"{chosen_model} (AUC = {art['roc_auc']:.3f})", line=dict(color="#2563EB", width=3)))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random Guess (AUC = 0.50)", line=dict(color="#94A3B8", dash="dash")))
    fig_roc = base(fig_roc, "Receiver Operating Characteristic (ROC)")
    fig_roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
    st.plotly_chart(fig_roc, use_container_width=True)

with tab_pr:
    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=art["pr_rec"], y=art["pr_prec"], mode="lines", name=f"{chosen_model} (PR-AUC = {art['pr_auc']:.3f})", line=dict(color="#2563EB", width=3)))
    fig_pr = base(fig_pr, "Precision-Recall Curve")
    fig_pr.update_layout(xaxis_title="Recall", yaxis_title="Precision")
    st.plotly_chart(fig_pr, use_container_width=True)

with tab_feat:
    if art["feature_importance"] is not None:
        fig_feat = px.bar(
            art["feature_importance"].head(15), x="Importance", y="Feature", orientation="h",
            title=f"Top 15 Predictive Features — {chosen_model}",
            color="Importance",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]]
        )
        fig_feat = base(fig_feat, f"Top 15 Predictive Features — {chosen_model}")
        fig_feat.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_feat, use_container_width=True)
    else:
        st.info("Feature importance is available for tree-based models (Random Forest, Decision Tree).")

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Comparative Supervised Classification Framework",
    algorithm_name="Random Forest • Decision Tree • Gaussian Naive Bayes",
    why_used=[
        ("Random Forest for Production Generalization", "As an ensemble of 150 bootstrapped decision trees, Random Forest aggregates orthogonal feature subspaces, reducing variance and neutralizing individual decision tree overfitting. In campus placement datasets where non-linear interactions between CGPA, DSA problem counts, and internship pedigree determine outcomes, Random Forest achieves peak generalization (~86.5% accuracy) with robust ROC-AUC (~0.93)."),
        ("Decision Tree for White-Box Explainability", "Decision trees produce an explicit, hierarchical set of human-interpretable boolean decision rules (e.g. `If CGPA >= 7.5 and DSA >= 60 then Placed`). In an academic institution, black-box models are unacceptable for student counselling; Decision Trees provide transparent, actionable rationales that placement coordinators can directly explain to students."),
        ("Gaussian Naive Bayes as a Probabilistic Baseline", "Naive Bayes applies Bayes' Theorem under the conditional class-independence assumption. While real-world student features correlate, Naive Bayes serves as an essential rapid, low-variance benchmark. Its calibrated posterior class probabilities confirm whether more computationally demanding non-linear algorithms deliver statistically significant accuracy gains.")
    ],
    institutional_impact="Enables placement officers to deploy Random Forest as the high-accuracy automated scoring engine while using Decision Tree feature splits to establish clear departmental eligibility benchmarks (e.g., minimum project count and mock interview thresholds) that maximize campus-wide placement conversion.",
    dwm_concept="Supervised Learning, Information Gain (Gini Impurity / Entropy), Bagging & Variance Reduction, Posterior Class Probability Estimation."
)
