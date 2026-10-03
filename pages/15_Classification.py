import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.classification import train_models
from src.visualizations import confusion_matrix_heatmap
from src.database import get_system_setting, set_system_setting
from src.ui import css, hero, render_top_navbar

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
<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 10px 18px; margin-bottom: 16px; font-size: 0.86rem; color: #cbd5e1;">
    Active Training Cohort: <b style="color:#38bdf8;">{len(df):,}</b> students 
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

# ----------------- BENCHMARK TABLE -----------------
st.markdown("### 📊 Cross-Model Benchmark Comparison")

# Safe subset formatting ensuring text columns are NEVER touched
num_cols = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "Training Time (s)"]
valid_num_cols = [c for c in num_cols if c in metrics_df.columns]

styled_table = metrics_df.style.format("{:.3f}", subset=valid_num_cols)
st.dataframe(styled_table, use_container_width=True)

# Metric Summary Strip
m_cols = st.columns(3)
for col, (_, r) in zip(m_cols, metrics_df.iterrows()):
    col.metric(r["Model"], f"F1: {r['F1']:.3f}", f"Acc: {r['Accuracy']:.3f} • {r['Training Time (s)']}s")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

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
    <div class="glass-card">
        <b style="color: #38bdf8;">Leader for {comp_metric}:</b><br>
        <span style="font-size: 1.3rem; font-weight: 800; color: #f8fafc;">{best_model['Model']} ({best_model[comp_metric]:.3f})</span>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 10px; line-height: 1.6;">
            <b>Technical Justification:</b> Random Forest builds an ensemble of decorrelated decision trees, minimizing variance and mitigating overfitting on noisy boundary features like LeetCode and aptitude scores. 
            Decision Tree provides single-rule explainability with lower training latency. Naive Bayes assumes conditional independence between features given the class label.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_cmp_chart:
    fig_cmp = px.bar(
        metrics_df, x="Model", y=["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        barmode="group",
        title="Comprehensive Performance Indices Across Models"
    )
    fig_cmp.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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
    fig_roc.add_trace(go.Scatter(x=art["fpr"], y=art["tpr"], mode="lines", name=f"{chosen_model} (AUC = {art['roc_auc']:.3f})", line=dict(color="#38bdf8", width=3)))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random Guess (AUC = 0.50)", line=dict(color="#64748b", dash="dash")))
    fig_roc.update_layout(title="Receiver Operating Characteristic (ROC)", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_roc, use_container_width=True)

with tab_pr:
    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=art["pr_rec"], y=art["pr_prec"], mode="lines", name=f"{chosen_model} (PR-AUC = {art['pr_auc']:.3f})", line=dict(color="#c084fc", width=3)))
    fig_pr.update_layout(title="Precision-Recall Curve", xaxis_title="Recall", yaxis_title="Precision", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pr, use_container_width=True)

with tab_feat:
    if art["feature_importance"] is not None:
        fig_feat = px.bar(
            art["feature_importance"].head(15), x="Importance", y="Feature", orientation="h",
            title=f"Top 15 Predictive Features — {chosen_model}",
            color="Importance", color_continuous_scale="Purples"
        )
        fig_feat.update_layout(yaxis=dict(autorange="reversed"), template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_feat, use_container_width=True)
    else:
        st.info("Feature importance is available for tree-based models (Random Forest, Decision Tree).")
