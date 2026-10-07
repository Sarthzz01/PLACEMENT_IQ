import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.olap import (
    aggregate, apply_filters, slice_op, dice_op, rollup_2d,
    drilldown_2d, pivot_op, drill_across
)
from src.database import log_olap_query, get_olap_history
from src.visualizations import base
from src.ui import css, hero, render_top_navbar, label, render_academic_justification

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Multi-Dimensional OLAP Cube Analytics",
    "Dynamic Slice, Dice, 2-Dimensional Simultaneous Roll-Up & Drill-Down, Cross-Tabular Pivot, and Multi-Fact Drill-Across over the placement data cube.",
    tag="OLAP Engine"
)

# Dataset Scope Selection (Original vs Unified)
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    st.markdown("### 🧊 OLAP Cube Engine")
with col_head2:
    cube_scope = st.radio(
        "Cube Data Source",
        ["Unified Dataset (Original + DB Students)", "Original Dataset Only"],
        horizontal=True,
        key="olap_cube_scope"
    )

include_new = (cube_scope == "Unified Dataset (Original + DB Students)")
df = load_data(include_new_students=include_new)

# Dynamic Dimensions & Measures from the active DataFrame
DIMENSIONS = [
    c for c in [
        "branch", "gender", "placement_training", "placement_status",
        "cgpa_band", "aptitude_band", "attendance_band", "coding_band",
        "internship_band", "projects_band", "backlog_band", "data_source"
    ] if c in df.columns
]

MEASURES = [
    c for c in [
        "cgpa", "attendance_percentage", "dsa_questions_solved",
        "leetcode_questions_solved", "hackerrank_questions_solved",
        "internships_count", "projects_count", "hackathons_count",
        "certifications_count", "aptitude_score", "communication_score",
        "coding_skill_score", "github_repos", "mock_interview_score",
        "placement_prediction"
    ] if c in df.columns
]

AGG_FUNCS = ["Average", "Sum", "Count", "Min", "Max", "Median"]

tab_builder, tab_slice, tab_dice, tab_rollup, tab_drilldown, tab_pivot, tab_across, tab_hist = st.tabs([
    "🛠️ 1. Universal Query Builder",
    "🔪 2. Slice",
    "🎲 3. Dice",
    "⬆️ 4. 2D Roll-Up",
    "⬇️ 5. 2D Drill-Down",
    "🔄 6. Pivot Table",
    "🌐 7. Drill-Across",
    "📜 8. Query History"
])

# ----------------- TAB 1: UNIVERSAL OLAP QUERY BUILDER -----------------
with tab_builder:
    st.markdown("### 🛠️ Universal OLAP Query Builder")
    st.caption("Freely compose row dimensions, column dimensions, numeric measures, and aggregation functions:")

    st.markdown("""<div class="campus-card" style="margin-bottom: 16px;">""", unsafe_allow_html=True)
    b_c1, b_c2, b_c3, b_c4 = st.columns(4)
    with b_c1:
        qb_rows = st.multiselect("Row Dimension(s)", DIMENSIONS, default=["branch"], format_func=label)
    with b_c2:
        qb_cols = st.multiselect("Column Dimension(s)", [d for d in DIMENSIONS if d not in qb_rows], default=["placement_status"], format_func=label)
    with b_c3:
        qb_measure = st.selectbox("Measure Column", MEASURES, index=MEASURES.index("cgpa"), format_func=label)
    with b_c4:
        qb_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0)

    # Dynamic Multi-Filters
    with st.expander("🔍 Optional Slice & Sub-Cube Filters", expanded=False):
        filt_dim_sel = st.multiselect("Select Dimensions to Filter", DIMENSIONS, default=[], format_func=label, key="qb_filt_dims")
        filters = {}
        if filt_dim_sel:
            f_cols = st.columns(min(3, len(filt_dim_sel)))
            for idx, c in enumerate(filt_dim_sel):
                with f_cols[idx % len(f_cols)]:
                    val_opts = sorted(df[c].dropna().astype(str).unique().tolist())
                    chosen_vals = st.multiselect(f"Values for {label(c)}", val_opts, key=f"qb_val_{c}")
                    if chosen_vals:
                        filters[c] = chosen_vals

    filtered_df = apply_filters(df, filters)
    st.caption(f"Active records matching filters: **{len(filtered_df):,}** of {len(df):,}")

    if st.button("🚀 Run OLAP Query", type="primary", key="btn_run_qb"):
        with st.spinner("Aggregating multi-dimensional data cube..."):
            qb_res = aggregate(filtered_df, qb_rows, qb_cols, qb_measure, qb_agg)
            st.session_state.qb_result = qb_res
            log_olap_query(email, "Universal Query Builder", qb_rows, qb_cols, qb_measure, qb_agg, filters, len(qb_res))

    st.markdown("</div>", unsafe_allow_html=True)

    if "qb_result" in st.session_state:
        res = st.session_state.qb_result
        st.markdown("#### Aggregated Cube Result")
        st.dataframe(res, use_container_width=True)

        if len(qb_rows) > 0 and len(res) > 0:
            val_cols = res.columns[len(qb_rows):]
            if len(val_cols) > 0:
                fig_qb = px.bar(
                    res, x=qb_rows[0], y=val_cols, barmode="group",
                    title=f"{qb_agg} of {label(qb_measure)} by {label(qb_rows[0])}"
                )
                fig_qb = base(fig_qb, f"{qb_agg} of {label(qb_measure)} by {label(qb_rows[0])}")
                st.plotly_chart(fig_qb, use_container_width=True)

        csv_qb = res.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download OLAP Query Results (CSV)", data=csv_qb, file_name="olap_query_result.csv", mime="text/csv")

# ----------------- TAB 2: SLICE -----------------
with tab_slice:
    st.markdown("### 🔪 OLAP Slice Operation")
    st.caption("Slice the cube across a specific dimensional plane by fixing one attribute value:")

    st.markdown("""<div class="campus-card" style="margin-bottom: 16px;">""", unsafe_allow_html=True)
    sl_c1, sl_c2, sl_c3, sl_c4 = st.columns(4)
    with sl_c1:
        slice_dim = st.selectbox("Select Slice Dimension", DIMENSIONS, index=0, format_func=label, key="sl_dim")
    with sl_c2:
        slice_vals = sorted(df[slice_dim].astype(str).unique().tolist())
        slice_val = st.selectbox("Select Slice Value", slice_vals, key="sl_val")
    with sl_c3:
        slice_measure = st.selectbox("Measure Column", MEASURES, index=MEASURES.index("cgpa"), format_func=label, key="sl_meas")
    with sl_c4:
        slice_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0, key="sl_agg")
    st.markdown("</div>", unsafe_allow_html=True)

    slice_df = df[df[slice_dim].astype(str) == str(slice_val)]

    # KPI Strip
    sk1, sk2, sk3, sk4 = st.columns(4)
    with sk1:
        st.metric("Cohort Students", f"{len(slice_df):,}", f"Filtered by {slice_dim}={slice_val}")
    with sk2:
        placed_pct = (slice_df['placement_prediction'].mean()) * 100 if len(slice_df) > 0 else 0
        st.metric("Placement Rate", f"{placed_pct:.1f}%", "Cohort Success")
    with sk3:
        m_val = getattr(slice_df[slice_measure], "mean")() if len(slice_df) > 0 else 0
        st.metric(f"{slice_agg} {label(slice_measure)}", f"{m_val:.2f}")
    with sk4:
        st.metric("Avg Attendance", f"{slice_df['attendance_percentage'].mean():.1f}%" if len(slice_df) > 0 else "0%")

    st.markdown("#### Filtered Records Table")
    st.dataframe(slice_df.head(25), use_container_width=True)

    if len(slice_df) > 0:
        fig_slice = px.histogram(
            slice_df, x="cgpa", color="placement_status",
            title=f"CGPA Distribution for {label(slice_dim)} = '{slice_val}'",
            color_discrete_map={"Placed": "#16A34A", "Not Placed": "#64748B"}
        )
        fig_slice = base(fig_slice, f"CGPA Distribution for {label(slice_dim)} = '{slice_val}'")
        st.plotly_chart(fig_slice, use_container_width=True)

    csv_sl = slice_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Sliced Records (CSV)", data=csv_sl, file_name=f"slice_{slice_dim}_{slice_val}.csv", mime="text/csv")

# ----------------- TAB 3: DICE -----------------
with tab_dice:
    st.markdown("### 🎲 OLAP Dice Operation")
    st.caption("Dice defines a sub-cube by specifying multi-condition filters simultaneously:")

    st.markdown("""<div class="campus-card" style="margin-bottom: 16px;">""", unsafe_allow_html=True)
    d_c1, d_c2, d_c3, d_c4 = st.columns(4)
    with d_c1:
        dice_branches = st.multiselect("Branch Condition", sorted(df["branch"].dropna().unique().tolist()), default=["CSE", "IT"])
    with d_c2:
        dice_cgpa_min = st.slider("Minimum CGPA", 0.0, 10.0, 7.5, 0.1)
    with d_c3:
        dice_att_min = st.slider("Minimum Attendance %", 0.0, 100.0, 75.0, 1.0)
    with d_c4:
        dice_intern = st.selectbox("Internship Experience", ["All", "With Internships (≥1)", "Without Internships (0)"])
    st.markdown("</div>", unsafe_allow_html=True)

    dice_data = df.copy()
    if dice_branches:
        dice_data = dice_data[dice_data["branch"].isin(dice_branches)]
    dice_data = dice_data[dice_data["cgpa"] >= dice_cgpa_min]
    dice_data = dice_data[dice_data["attendance_percentage"] >= dice_att_min]
    if dice_intern == "With Internships (≥1)":
        dice_data = dice_data[dice_data["internships_count"] >= 1]
    elif dice_intern == "Without Internships (0)":
        dice_data = dice_data[dice_data["internships_count"] == 0]

    dk1, dk2, dk3 = st.columns(3)
    with dk1:
        st.metric("Diced Sub-Cube Count", f"{len(dice_data):,}", f"Matching all conditions")
    with dk2:
        dice_pl = (dice_data['placement_prediction'].mean() * 100) if len(dice_data) > 0 else 0
        st.metric("Sub-Cube Placement Rate", f"{dice_pl:.1f}%")
    with dk3:
        st.metric("Avg Aptitude", f"{dice_data['aptitude_score'].mean():.1f}" if len(dice_data) > 0 else "0")

    if len(dice_data) > 0:
        fig_dice = px.scatter(
            dice_data.sample(min(3000, len(dice_data)), random_state=42),
            x="cgpa", y="aptitude_score", color="placement_status",
            size="dsa_questions_solved",
            title="Diced Sub-Cube: CGPA vs Aptitude Score (Size: DSA Solved)",
            color_discrete_map={"Placed": "#16A34A", "Not Placed": "#64748B"}
        )
        fig_dice = base(fig_dice, "Diced Sub-Cube: CGPA vs Aptitude Score (Size: DSA Solved)")
        st.plotly_chart(fig_dice, use_container_width=True)

        st.dataframe(dice_data.head(20), use_container_width=True)

        csv_dice = dice_data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Diced Sub-Cube (CSV)", data=csv_dice, file_name="diced_subcube.csv", mime="text/csv")

# ----------------- TAB 4: 2D ROLL-UP -----------------
with tab_rollup:
    st.markdown("### ⬆️ 2-Dimensional Dynamic Roll-Up Operation")
    st.caption("Select which row dimensions and which column dimensions to drill up at once:")

    st.markdown("""
    <div class="campus-card" style="margin-bottom: 16px;">
        <p style="color:#475569; font-size:0.88rem; margin:0;">
            <b>Simultaneous 2D Roll-Up:</b> Choose the current detailed levels on both axes, then specify the target summarized levels.
            The engine executes roll-up along both axes simultaneously and displays the side-by-side transition.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ru_c1, ru_c2 = st.columns(2)
    with ru_c1:
        st.markdown("#### Row Axis Roll-Up")
        ru_curr_rows = st.multiselect("Current Row Dimensions", DIMENSIONS, default=["branch", "gender"], key="ru_c_rows", format_func=label)
        ru_targ_rows = st.multiselect("Roll-Up Rows To (Fewer Dimensions or Empty for Overall)", [d for d in ru_curr_rows], default=["branch"], key="ru_t_rows", format_func=label)

    with ru_c2:
        st.markdown("#### Column Axis Roll-Up")
        ru_curr_cols = st.multiselect("Current Column Dimensions", [d for d in DIMENSIONS if d not in ru_curr_rows], default=["placement_status", "placement_training"], key="ru_c_cols", format_func=label)
        ru_targ_cols = st.multiselect("Roll-Up Columns To (Fewer Dimensions or Empty for Overall)", [d for d in ru_curr_cols], default=["placement_status"], key="ru_t_cols", format_func=label)

    ru_m_c1, ru_m_c2 = st.columns(2)
    with ru_m_c1:
        ru_measure = st.selectbox("Measure Column", MEASURES, index=MEASURES.index("cgpa"), format_func=label, key="ru_meas")
    with ru_m_c2:
        ru_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0, key="ru_agg")

    if st.button("🚀 Execute 2D Roll-Up", type="primary", key="btn_run_ru"):
        b_df, a_df = rollup_2d(df, ru_curr_rows, ru_targ_rows, ru_curr_cols, ru_targ_cols, ru_measure, ru_agg)
        
        st.markdown(f"#### 1. Before Roll-Up (Detailed: Rows={ru_curr_rows}, Cols={ru_curr_cols})")
        st.dataframe(b_df, use_container_width=True)

        st.markdown(f"#### 2. After Roll-Up (Summarized: Rows={ru_targ_rows if ru_targ_rows else 'Overall'}, Cols={ru_targ_cols if ru_targ_cols else 'Overall'})")
        st.dataframe(a_df, use_container_width=True)

        log_olap_query(email, "2D Roll-Up", ru_targ_rows, ru_targ_cols, ru_measure, ru_agg, {}, len(a_df))

# ----------------- TAB 5: 2D DRILL-DOWN -----------------
with tab_drilldown:
    st.markdown("### ⬇️ 2-Dimensional Dynamic Drill-Down Operation")
    st.caption("Navigate from summarized parent levels down to finer granular attributes across row and column axes:")

    dd_c1, dd_c2 = st.columns(2)
    with dd_c1:
        st.markdown("#### Row Axis Drill-Down")
        dd_curr_rows = st.multiselect("Current Row Dimensions", DIMENSIONS, default=["branch"], key="dd_c_rows", format_func=label)
        dd_targ_rows = st.multiselect("Drill-Down Rows To (Add Sub-Dimensions)", DIMENSIONS, default=["branch", "gender"], key="dd_t_rows", format_func=label)

    with dd_c2:
        st.markdown("#### Column Axis Drill-Down")
        dd_curr_cols = st.multiselect("Current Column Dimensions", [d for d in DIMENSIONS if d not in dd_curr_rows], default=["placement_status"], key="dd_c_cols", format_func=label)
        dd_targ_cols = st.multiselect("Drill-Down Columns To (Add Sub-Dimensions)", [d for d in DIMENSIONS if d not in dd_targ_rows], default=["placement_status", "cgpa_band"], key="dd_t_cols", format_func=label)

    dd_m_c1, dd_m_c2 = st.columns(2)
    with dd_m_c1:
        dd_measure = st.selectbox("Measure Column", MEASURES, index=MEASURES.index("cgpa"), format_func=label, key="dd_meas")
    with dd_m_c2:
        dd_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0, key="dd_agg")

    if st.button("🚀 Execute 2D Drill-Down", type="primary", key="btn_run_dd"):
        b_df, a_df = drilldown_2d(df, dd_curr_rows, dd_targ_rows, dd_curr_cols, dd_targ_cols, dd_measure, dd_agg)

        st.markdown(f"#### 1. Before Drill-Down (High Level: Rows={dd_curr_rows}, Cols={dd_curr_cols})")
        st.dataframe(b_df, use_container_width=True)

        st.markdown(f"#### 2. After Drill-Down (Granular: Rows={dd_targ_rows}, Cols={dd_targ_cols})")
        st.dataframe(a_df, use_container_width=True)

        log_olap_query(email, "2D Drill-Down", dd_targ_rows, dd_targ_cols, dd_measure, dd_agg, {}, len(a_df))

# ----------------- TAB 6: PIVOT TABLE -----------------
with tab_pivot:
    st.markdown("### 🔄 OLAP Pivot Table & Matrix View")
    st.caption("Rotate axes to view data from different analytical perspectives:")

    st.markdown("""<div class="campus-card" style="margin-bottom: 16px;">""", unsafe_allow_html=True)
    pv_c1, pv_c2, pv_c3, pv_c4 = st.columns(4)
    with pv_c1:
        pv_row = st.selectbox("Row Dimension", DIMENSIONS, index=DIMENSIONS.index("branch"), format_func=label, key="pv_row")
    with pv_c2:
        pv_col = st.selectbox("Column Dimension", [d for d in DIMENSIONS if d != pv_row], index=0, format_func=label, key="pv_col")
    with pv_c3:
        pv_measure = st.selectbox("Value Measure", MEASURES, index=MEASURES.index("cgpa"), format_func=label, key="pv_meas")
    with pv_c4:
        pv_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0, key="pv_agg")
    st.markdown("</div>", unsafe_allow_html=True)

    pv_result = pivot_op(df, [pv_row], [pv_col], pv_measure, pv_agg)
    st.markdown(f"#### Pivot Matrix: {label(pv_row)} × {label(pv_col)} ({pv_agg} of {label(pv_measure)})")
    st.dataframe(pv_result, use_container_width=True)

    if len(pv_result) > 0 and len(pv_result.columns) > 1:
        val_cols = pv_result.columns[1:]
        fig_pv = px.imshow(
            pv_result[val_cols].values,
            x=[str(c) for c in val_cols],
            y=pv_result[pv_row].astype(str).tolist(),
            text_auto=True,
            title=f"Cross-Tabulation Matrix: {label(pv_row)} vs {label(pv_col)}",
            color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]]
        )
        fig_pv = base(fig_pv, f"Cross-Tabulation Matrix: {label(pv_row)} vs {label(pv_col)}")
        st.plotly_chart(fig_pv, use_container_width=True)

    csv_pv = pv_result.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Pivot Table (CSV)", data=csv_pv, file_name="pivot_table.csv", mime="text/csv")

# ----------------- TAB 7: DRILL-ACROSS -----------------
with tab_across:
    st.markdown("### 🌐 OLAP Drill-Across Operation")
    st.caption("Combine multiple measures across different warehouse dimension areas in a single query:")

    st.markdown("""<div class="campus-card" style="margin-bottom: 16px;">""", unsafe_allow_html=True)
    ac_c1, ac_c2 = st.columns(2)
    with ac_c1:
        ac_row = st.selectbox("Row Dimension", DIMENSIONS, index=0, format_func=label, key="ac_row")
    with ac_c2:
        ac_col = st.selectbox("Column Dimension", [d for d in DIMENSIONS if d != ac_row], index=2, format_func=label, key="ac_col")

    ac_measures = st.multiselect(
        "Select Multiple Cross-Table Measures",
        MEASURES,
        default=["cgpa", "aptitude_score", "placement_prediction"],
        format_func=label
    )
    ac_agg = st.selectbox("Aggregation", AGG_FUNCS, index=0, key="ac_agg")
    st.markdown("</div>", unsafe_allow_html=True)

    if ac_measures:
        st.info("Lineage: Combining `FactPlacement` measures with `DimStudent` and `DimAcademic` dimensions.")
        ac_res = drill_across(df, ac_row, ac_col, ac_measures, ac_agg)
        st.dataframe(ac_res, use_container_width=True)

        csv_ac = ac_res.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Drill-Across Results (CSV)", data=csv_ac, file_name="drill_across_results.csv", mime="text/csv")

# ----------------- TAB 8: QUERY HISTORY -----------------
with tab_hist:
    st.markdown("### 📜 OLAP Query Audit History")
    st.caption("Review recently executed OLAP cube operations stored in SQLite database:")

    hist_olap = get_olap_history()
    if len(hist_olap) > 0:
        st.dataframe(hist_olap, use_container_width=True)
    else:
        st.info("No OLAP queries logged yet in this session.")

# ----------------- ACADEMIC & INSTITUTIONAL JUSTIFICATION -----------------
render_academic_justification(
    title="Multi-Dimensional OLAP Cube Operations & Strategic Navigation",
    algorithm_name="OLAP Operations: Slice • Dice • 2D Roll-Up • 2D Drill-Down • Pivot • Drill-Across",
    why_used=[
        ("Interactive Dimensional Slicing & Dicing", "Standard static tables only show flat, predefined views of student cohorts. The Slice operation isolates a specific sub-plane along a single dimension (e.g. Branch = Computer Science), while Dice extracts a localized sub-cube bounded by multiple simultaneous criteria (e.g. CGPA >= 8.0 and Internships >= 2). This allows placement officers to isolate niche talent pools instantly for incoming specialized recruiters."),
        ("Bidirectional Hierarchical Navigation (Roll-Up & Drill-Down)", "Academic leadership requires insights at different levels of abstraction. Simultaneous 2D Roll-Up summarizes granular data upward along conceptual hierarchies (Student → Branch → Campus Institution), revealing macro placement trends. Conversely, Drill-Down navigates downward from high-level statistics into granular candidate records, enabling immediate targeted academic counseling for high-risk students."),
        ("Axis Rotation (Pivot) & Multi-Fact Synthesis (Drill-Across)", "The Pivot operation reorients cube axes to present cross-tabulated contingency matrices (e.g. Academic Performance vs Placement Rate), surfacing hidden dimensional dependencies. Drill-Across spans multiple fact domains, consolidating student co-curricular milestones with final hiring conversion into a unified analytical matrix.")
    ],
    institutional_impact="Transforms placement intelligence from reactive post-semester reviews into proactive, real-time decision-making—allowing placement deans to continuously evaluate departmental conversion rates, optimize faculty training allocations, and track cohort progress.",
    dwm_concept="Multi-Dimensional Data Cube (MOLAP / ROLAP), Slice & Dice Projections, Concept Hierarchies & Dimension Generalization, Granular Decomposition, Cross-Tabular Rotation, Multi-Fact Federation."
)
