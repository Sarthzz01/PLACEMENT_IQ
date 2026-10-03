import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.database import get_all_student_profiles_df, get_student_prediction_history
from src.config import DB_PATH
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Institutional Placement Intelligence Dashboard",
    "Executive institutional analytics across university student records stored in our SQLite Star-Schema Data Warehouse and active candidate databases.",
    tag="Executive Command Center"
)

# Unified dataset control
counts = get_dataset_counts()

top_c1, top_c2 = st.columns([2, 1])
with top_c1:
    st.markdown("### 📊 Cohort Scope & Dataset Selection")
with top_c2:
    dataset_scope = st.radio(
        "Analytics Dataset Scope",
        ["Unified Dataset (Original + New Students)", "Original Dataset Only"],
        horizontal=True
    )

include_new = (dataset_scope == "Unified Dataset (Original + New Students)")
df = load_data(include_new_students=include_new)

total_students = len(df)
placed_students = int(df["placement_prediction"].sum())
not_placed = total_students - placed_students
placement_rate = (placed_students / total_students) * 100
avg_cgpa = df["cgpa"].mean()
avg_aptitude = df["aptitude_score"].mean()
avg_coding = df["coding_skill_score"].mean()

# ----------------- DATASET LINEAGE & STATS -----------------
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; font-size: 0.88rem; color: #cbd5e1;">
    <b>Dataset Lineage:</b> 
    Original CSV Students: <b style="color:#38bdf8;">""" + f"{counts['original_students']:,}" + """</b> &bull; 
    Newly Registered Students in SQLite: <b style="color:#c084fc;">""" + f"{counts['new_students']:,}" + """</b> &bull; 
    Active Analytics Cohort: <b style="color:#34d399;">""" + f"{total_students:,}" + """</b> students
</div>
""", unsafe_allow_html=True)

# ----------------- TOP KPI CARDS -----------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("Total Students", f"{total_students:,}", f"{counts['new_students']} newly added")
with k2:
    st.metric("Placed Students", f"{placed_students:,}", f"{placement_rate:.1f}% Placement Rate")
with k3:
    st.metric("Not Placed", f"{not_placed:,}", f"{100-placement_rate:.1f}% Cohort")
with k4:
    st.metric("Average CGPA", f"{avg_cgpa:.2f}", "Across Cohorts")
with k5:
    st.metric("Avg Aptitude", f"{avg_aptitude:.1f} / 100", "Screening Metric")
with k6:
    st.metric("Avg Coding Index", f"{avg_coding:.1f} / 10", "Technical Fluency")

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ----------------- VISUAL ANALYTICS GRID -----------------
c_chart1, c_chart2 = st.columns([1, 1], gap="medium")

with c_chart1:
    st.markdown("### 🍩 Overall Campus Placement Split")
    status_df = df["placement_status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    fig_pie = px.pie(
        status_df, names="Status", values="Count", hole=0.55,
        title="Placement Outcomes Ratio",
        color="Status",
        color_discrete_map={"Placed": "#10b981", "Not Placed": "#f43f5e"}
    )
    fig_pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c_chart2:
    st.markdown("### 🏛️ Placement Distribution by Branch")
    branch_df = df.groupby(["branch", "placement_status"]).size().reset_index(name="Students")
    fig_bar = px.bar(
        branch_df, x="branch", y="Students", color="placement_status", barmode="group",
        title="Placed vs. Not Placed by Engineering Department",
        color_discrete_map={"Placed": "#6366f1", "Not Placed": "#64748b"}
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

c_chart3, c_chart4 = st.columns([1, 1], gap="medium")

with c_chart3:
    st.markdown("### 📊 Academic CGPA Distribution")
    fig_hist = px.histogram(
        df, x="cgpa", color="placement_status", nbins=30,
        title="CGPA Frequency Breakdown across Campus",
        color_discrete_map={"Placed": "#10b981", "Not Placed": "#f43f5e"},
        opacity=0.75
    )
    fig_hist.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_hist, use_container_width=True)

with c_chart4:
    st.markdown("### 💼 Practical Internships vs Placement Rate")
    intern_group = df.groupby("internships_count")["placement_prediction"].agg(["count", "mean"]).reset_index()
    intern_group["Placement Rate %"] = intern_group["mean"] * 100
    fig_line = px.line(
        intern_group, x="internships_count", y="Placement Rate %",
        markers=True,
        title="Placement Probability by Number of Completed Internships",
        labels={"internships_count": "Internships Completed"}
    )
    fig_line.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_line, use_container_width=True)

# ----------------- SYSTEM STATUS FOOTER -----------------
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; margin-top: 14px;">
    <h4 style="margin-top:0; color:#38bdf8;">Data Warehouse Infrastructure Status</h4>
    <p style="color:#94a3b8; font-size:0.88rem; margin-bottom: 0;">
        SQLite Star-Schema Database: <code>outputs/placement_dw.sqlite</code> &bull; Central Fact Table: <code>FactPlacement</code> &bull; Relational Dimension Tables: <code>DimStudent</code>, <code>DimAcademic</code>, <code>DimSkills</code>, <code>DimEngagement</code>, <code>DimPlacement</code>.
    </p>
</div>
""", unsafe_allow_html=True)
