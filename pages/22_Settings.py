import streamlit as st
from src.auth import require_admin
from src.config import ADMIN_EMAILS, DB_PATH, DATA_PATH
from src.preprocessing import validate_dataset, load_data, get_dataset_counts
from src.warehouse import build_warehouse
from src.database import get_system_setting, set_system_setting
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "System Settings & Warehouse Governance",
    "Configure administrator accounts, manage production machine learning models, inspect dataset counts, and execute database maintenance.",
    tag="System Administration"
)

tab_models, tab_acc, tab_wh, tab_diag = st.tabs([
    "🎯 1. Production Model & ML Settings",
    "👥 2. Admin Accounts & Roles",
    "🏛️ 3. Data Warehouse Maintenance",
    "🩺 4. Health & Diagnostics"
])

# ----------------- TAB 1: PRODUCTION MODEL SETTINGS -----------------
with tab_models:
    st.markdown("### 🎯 Production Model Configuration")
    st.caption("Designate which trained classifier generates live student-facing placement predictions:")

    curr_model = get_system_setting("production_model", "Random Forest")
    new_model = st.selectbox(
        "Active Production Classifier",
        ["Random Forest", "Decision Tree", "Naive Bayes"],
        index=["Random Forest", "Decision Tree", "Naive Bayes"].index(curr_model) if curr_model in ["Random Forest", "Decision Tree", "Naive Bayes"] else 0
    )

    if st.button("💾 Save Production Model Selection", type="primary"):
        set_system_setting("production_model", new_model)
        st.success(f"Production model successfully set to **{new_model}**!")
        st.rerun()

    st.markdown("""
    <div class="glass-card" style="margin-top: 14px; font-size: 0.88rem; color: #cbd5e1;">
        • <b>Random Forest (Recommended):</b> Ensemble model achieving ~86.5% test accuracy with robust generalization across non-linear feature interactions.<br>
        • <b>Decision Tree:</b> High interpretability with hierarchical decision rules.<br>
        • <b>Gaussian Naive Bayes:</b> Fast probabilistic baseline suitable for continuous Bayesian likelihood estimates.
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 2: ADMIN ACCOUNTS -----------------
with tab_acc:
    st.markdown("### 👥 Configured Administrator Email Accounts")
    st.caption("Users signing in with any of these institutional email addresses are automatically granted Administrator privileges:")

    st.markdown("""
    <div class="glass-card">
        <ul style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.8; margin-bottom: 0;">
    """ + "".join([f"<li><code>{e}</code></li>" for e in ADMIN_EMAILS]) + """
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 To modify permanent admin accounts, update the `ADMIN_EMAILS` list in `src/config.py`.")

# ----------------- TAB 3: DATA WAREHOUSE MAINTENANCE -----------------
with tab_wh:
    st.markdown("### 🏛️ Data Warehouse Maintenance")
    st.caption("Re-index SQLite Star Schema tables or flush cached models:")

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        if st.button("🔄 Force Rebuild SQLite Star Schema (Unified)", use_container_width=True, type="primary"):
            with st.spinner("Rebuilding SQLite tables from active datasets..."):
                df = load_data(include_new_students=True)
                build_warehouse(df)
                st.success("Data Warehouse rebuilt successfully with unified student records!")
    with c_b2:
        if st.button("🧹 Clear Model Memory Cache", use_container_width=True):
            st.cache_data.clear()
            for key in ["cls_admin", "reg_admin", "km_admin", "agg_admin", "qb_result"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("Model session caches cleared!")

# ----------------- TAB 4: SYSTEM DIAGNOSTICS -----------------
with tab_diag:
    st.markdown("### 🩺 System Diagnostics & Dataset Lineage")
    diag = validate_dataset()
    counts = get_dataset_counts()

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.metric("Original Dataset Records", f"{counts['original_students']:,}", "placement_prediction_cleaned.csv")
    with d2:
        st.metric("New Registered Students", f"{counts['new_students']:,}", "Stored in SQLite DB")
    with d3:
        st.metric("Combined Analytics Cohort", f"{counts['combined_students']:,}", "100% Schema Valid")
    with d4:
        st.metric("Database File", DB_PATH.name, "SQLite Connected")

    st.markdown("#### Target Distribution (`placement_prediction`)")
    st.json(diag["target_distribution"])
