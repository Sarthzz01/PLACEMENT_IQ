import streamlit as st
import pandas as pd
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.warehouse import (
    build_warehouse, get_warehouse_summary, get_sample_records,
    query, STAR_SCHEMA_DEF, RELATIONSHIPS
)
from src.config import DB_PATH
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Star-Schema Data Warehouse Architecture",
    "Inspect relational dimension tables, query the central FactPlacement table, and refresh warehouse data cubes across baseline and newly registered student cohorts.",
    tag="Data Warehousing Core"
)

# Warehouse Metadata & Status
wh_summary = get_warehouse_summary()
db_exists = DB_PATH.exists() and len(wh_summary) > 0

col_status1, col_status2 = st.columns([2, 1])
with col_status1:
    st.markdown("### 🏛️ Relational Data Warehouse Status")
with col_status2:
    wh_scope = st.radio(
        "Warehouse Cohort Source",
        ["Unified Dataset (Original + DB Students)", "Original Dataset Only"],
        horizontal=True
    )

include_new = (wh_scope == "Unified Dataset (Original + DB Students)")

# Action to refresh warehouse
c_act1, c_act2 = st.columns([1, 2])
with c_act1:
    if st.button("🔄 Refresh / Rebuild Data Warehouse", type="primary", use_container_width=True):
        with st.spinner("Extracting, transforming, and loading records into Star Schema SQLite database..."):
            df = load_data(include_new_students=include_new)
            build_warehouse(df)
            st.success("Data Warehouse rebuilt successfully!")
            st.rerun()

wh_summary = get_warehouse_summary()
fact_rows = wh_summary.get("FactPlacement", {}).get("rows", 0)

# KPI Cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Fact Records (`FactPlacement`)", f"{fact_rows:,}", "Primary Fact Table")
with k2:
    st.metric("Dimension Tables", "5 Relational Tables", "Normalized Star Schema")
with k3:
    st.metric("Storage Engine", "SQLite RDBMS", "outputs/placement_dw.sqlite")
with k4:
    st.metric("Relational Integrity", "100% Foreign Keys", "Surrogate `student_key`")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

tab_schema, tab_tables, tab_relationships, tab_sql = st.tabs([
    "📐 1. Star Schema Architecture",
    "🔍 2. Warehouse Tables Browser",
    "🔗 3. Relationships & Keys",
    "⚡ 4. SQL Query Workbench"
])

# ----------------- TAB 1: STAR SCHEMA ARCHITECTURE -----------------
with tab_schema:
    st.markdown("### 📐 Star Schema Dimensional Model")
    st.caption("Central fact table with surrogate keys linking to 5 dedicated dimension tables:")

    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 22px; margin-bottom: 20px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
            <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 14px;">
                <b style="color: #818cf8;">DimStudent (Dimension)</b><br>
                <span style="font-size: 0.8rem; color: #cbd5e1;">student_key (PK), age, gender, branch, data_source</span>
            </div>
            <div style="background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 12px; padding: 14px;">
                <b style="color: #38bdf8;">DimAcademic (Dimension)</b><br>
                <span style="font-size: 0.8rem; color: #cbd5e1;">student_key (PK), cgpa, backlogs, attendance, cgpa_band</span>
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 14px;">
                <b style="color: #34d399;">DimSkills (Dimension)</b><br>
                <span style="font-size: 0.8rem; color: #cbd5e1;">student_key (PK), dsa, leetcode, aptitude, coding_score</span>
            </div>
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 14px;">
                <b style="color: #fbbf24;">DimEngagement (Dimension)</b><br>
                <span style="font-size: 0.8rem; color: #cbd5e1;">student_key (PK), internships, projects, hackathons, repos</span>
            </div>
            <div style="background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 12px; padding: 14px;">
                <b style="color: #fb7185;">DimPlacement (Dimension)</b><br>
                <span style="font-size: 0.8rem; color: #cbd5e1;">student_key (PK), placement_prediction, placement_status</span>
            </div>
        </div>
        
        <div style="text-align: center; margin: 18px 0 10px 0;">
            <div style="display: inline-block; background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(124, 58, 237, 0.3)); border: 2px solid #818cf8; border-radius: 16px; padding: 18px 36px; box-shadow: 0 0 24px rgba(99, 102, 241, 0.25);">
                <span style="font-size: 0.8rem; text-transform: uppercase; color: #38bdf8; font-weight: 800; letter-spacing: 0.05em;">CENTRAL FACT TABLE</span>
                <h3 style="margin: 4px 0; color: #f8fafc; font-size: 1.4rem;">FactPlacement</h3>
                <span style="font-size: 0.85rem; color: #cbd5e1;">
                    fact_id (PK) &bull; student_key (FK) &bull; cgpa &bull; attendance &bull; aptitude &bull; coding &bull; internships &bull; projects &bull; placement_prediction
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 2: WAREHOUSE TABLES BROWSER -----------------
with tab_tables:
    st.markdown("### 🔍 Interactive Table Browser")
    table_names = list(STAR_SCHEMA_DEF.keys())
    
    sel_tbl = st.selectbox("Select Warehouse Table to Inspect", table_names, index=0)
    limit_cnt = st.slider("Sample Row Limit", 5, 100, 15, 5)

    if db_exists:
        sample_df = get_sample_records(sel_tbl, limit=limit_cnt)
        st.markdown(f"**Showing first {len(sample_df)} rows from `{sel_tbl}`:**")
        st.dataframe(sample_df, use_container_width=True)

        st.caption(f"Schema Definition for `{sel_tbl}`: {', '.join(STAR_SCHEMA_DEF[sel_tbl])}")
    else:
        st.info("Warehouse database is initializing. Click 'Refresh / Rebuild' above.")

# ----------------- TAB 3: RELATIONSHIPS & KEYS -----------------
with tab_relationships:
    st.markdown("### 🔗 Star Schema Relational Integrity")
    rel_df = pd.DataFrame(RELATIONSHIPS)
    st.dataframe(rel_df, use_container_width=True)

# ----------------- TAB 4: SQL QUERY WORKBENCH -----------------
with tab_sql:
    st.markdown("### ⚡ Live SQL Query Workbench")
    st.caption("Execute custom SQL queries against the active SQLite Star-Schema Data Warehouse:")

    default_sql = """SELECT d.branch, p.placement_status, 
       ROUND(AVG(f.cgpa), 2) AS avg_cgpa, 
       ROUND(AVG(f.coding_skill_score), 2) AS avg_coding,
       COUNT(*) AS total_students
FROM FactPlacement f
JOIN DimStudent d ON f.student_key = d.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
GROUP BY d.branch, p.placement_status
ORDER BY d.branch, p.placement_status;"""

    user_sql = st.text_area("SQL Statement", value=default_sql, height=140)
    
    if st.button("🚀 Run SQL Query", type="primary"):
        try:
            sql_res = query(user_sql)
            st.markdown(f"**Query returned {len(sql_res)} rows:**")
            st.dataframe(sql_res, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {str(e)}")
