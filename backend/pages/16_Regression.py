import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data
from src.regression import train_regression
from src.config import BASE_NUMERIC, REGRESSION_TARGETS
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Continuous Numerical Regression Analysis",
    "Fit Simple Linear Regression (SLR) and Multiple Linear Regression (MLR) on candidate continuous placement competency scores.",
    tag="Numerical Estimation"
)

df = load_data()

st.markdown("""
<div class="campus-card" style="padding: 16px 20px; margin-bottom: 20px;">
    <b style="color: #2563EB;">📌 Dataset Target Integrity Notice:</b>
    <span style="color: #475569; font-size: 0.88rem;">
        The primary campus placement status in our verified dataset is binary (<code>placement_prediction</code>: 0 = Not Placed, 1 = Placed). 
        To avoid fabricating synthetic placement salary numbers, regression is rigorously evaluated on true continuous competency scores (<code>aptitude_score</code>, <code>coding_skill_score</code>, <code>cgpa</code>, <code>mock_interview_score</code>).
    </span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Regression Setup")
    target_col = st.selectbox("Select Continuous Target", REGRESSION_TARGETS, index=0, format_func=label)
    
    candidate_features = [c for c in BASE_NUMERIC if c != target_col]
    slr_feature = st.selectbox("SLR Single Predictor Feature", candidate_features, index=candidate_features.index("cgpa") if "cgpa" in candidate_features else 0, format_func=label)
    mlr_features = st.multiselect("MLR Multiple Predictor Features", candidate_features, default=candidate_features[:8], format_func=label)
    
    test_size = st.slider("Test Split Size", 0.1, 0.4, 0.2, 0.05)
    seed = st.number_input("Random Seed", 0, 9999, 42)
    fit_intercept = st.checkbox("Fit Intercept (Constant)", value=True)

if not mlr_features:
    mlr_features = candidate_features[:4]

if st.button("🚀 Train Regression Models", type="primary") or "reg_admin" not in st.session_state:
    with st.spinner(f"Fitting SLR and MLR models for target: {target_col}..."):
        st.session_state.reg_admin = train_regression(
            df, target_col=target_col, slr_feature=slr_feature,
            mlr_features=mlr_features, test_size=test_size,
            random_state=seed, fit_intercept=fit_intercept
        )

metrics_df, artifacts = st.session_state.reg_admin

# ----------------- BENCHMARK TABLE -----------------
st.markdown(f"### 📊 Benchmark Comparison: SLR vs. MLR (Target: `{target_col}`)")

# Safe numeric formatting on subset only
reg_num_cols = [c for c in ["R²", "MSE", "RMSE", "MAE"] if c in metrics_df.columns]
styled_reg = metrics_df.style.format("{:.4f}", subset=reg_num_cols)
st.dataframe(styled_reg, use_container_width=True)

col_bar, col_diag = st.columns([1.2, 1.8], gap="medium")
with col_bar:
    fig_cmp = px.bar(
        metrics_df, x="Model", y=["R²", "RMSE", "MAE"],
        barmode="group",
        title="Goodness-of-Fit (R²) & Error Comparison",
        color_discrete_sequence=["#2563EB", "#60A5FA", "#16A34A"]
    )
    fig_cmp = base(fig_cmp, "Goodness-of-Fit (R²) & Error Comparison")
    st.plotly_chart(fig_cmp, use_container_width=True)

with col_diag:
    st.markdown("#### 📐 Mathematical Equations & Coefficients")
    for _, r in metrics_df.iterrows():
        st.markdown(f"**{r['Model']}:**")
        st.code(r["Equation"])

    st.markdown(f"""
    <div class="campus-card" style="margin-top: 10px; font-size: 0.86rem; color: #475569;">
        <b>Technical Comparison:</b><br>
        Multiple Linear Regression captures variance across {len(mlr_features)} simultaneous signals, whereas Simple Linear Regression is constrained to the bivariate linear relationship with <code>{slr_feature}</code>.
    </div>
    """, unsafe_allow_html=True)

# ----------------- VISUAL DIAGNOSTICS -----------------
st.markdown("---")
st.markdown("### 📈 Visual Diagnostics: Actual vs Predicted & Residuals")

tab_slr, tab_mlr = st.tabs(["Simple Linear Regression (SLR)", "Multiple Linear Regression (MLR)"])

for tab, m_name in zip([tab_slr, tab_mlr], ["Simple Linear Regression", "Multiple Linear Regression"]):
    with tab:
        art = artifacts[m_name]
        c1, c2 = st.columns(2)
        with c1:
            fig_act = px.scatter(
                x=art["actual"], y=art["pred"],
                labels={"x": f"Actual {label(target_col)}", "y": f"Predicted {label(target_col)}"},
                title=f"Actual vs. Predicted — {m_name}",
                opacity=0.65,
                color_discrete_sequence=["#2563EB"]
            )
            min_v = min(min(art["actual"]), min(art["pred"]))
            max_v = max(max(art["actual"]), max(art["pred"]))
            fig_act.add_shape(type="line", x0=min_v, y0=min_v, x1=max_v, y1=max_v, line=dict(color="#DC2626", dash="dash"))
            fig_act = base(fig_act, f"Actual vs. Predicted — {m_name}")
            st.plotly_chart(fig_act, use_container_width=True)

        with c2:
            fig_res = px.histogram(
                x=art["residuals"], nbins=30,
                title=f"Residual Error Distribution (Actual - Predicted) — {m_name}",
                color_discrete_sequence=["#60A5FA"]
            )
            fig_res.add_vline(x=0, line_dash="dash", line_color="#16A34A")
            fig_res = base(fig_res, f"Residual Error Distribution — {m_name}")
            st.plotly_chart(fig_res, use_container_width=True)

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Continuous Placement Competency & Skill Estimation",
    algorithm_name="Simple Linear Regression (SLR) & Multiple Linear Regression (MLR)",
    why_used=[
        ("Univariate Baseline with SLR", "Simple Linear Regression isolates the direct, single-variable predictive power of foundational academic metrics (like CGPA) against quantitative skill targets (like Aptitude Score). By computing the slope and R², it demonstrates the empirical ceiling of relying solely on classroom marks for hiring competency."),
        ("Multivariate Weight Decomposition with MLR", "Multiple Linear Regression models the composite interaction of academic, coding, and experiential attributes simultaneously. The learned regression coefficients (β) quantify the exact marginal return for each unit increase in a feature (e.g., how much each additional project or 10 DSA questions lifts expected aptitude/coding competency), holding all other variables constant."),
        ("Residual Analysis & Error Diagnostics", "Visualizing residual error distributions verifies the fundamental Gauss-Markov assumptions (homoscedasticity, normality of error terms, zero mean). Centered, bell-shaped residual distributions validate that our linear formulations capture the true continuous trend without systematic bias.")
    ],
    institutional_impact="Equips placement advisors with quantifiable, parametric equations to set realistic semester-by-semester skill improvement milestones for students, moving beyond qualitative advice to precise numerical guidance.",
    dwm_concept="Continuous Numerical Prediction, Ordinary Least Squares (OLS) Optimization, Multivariate Coefficient Interpretation, Residual Diagnostics."
)
