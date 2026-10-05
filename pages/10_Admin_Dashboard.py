import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_admin
from src.preprocessing import load_data, get_dataset_counts
from src.database import get_all_student_profiles_df, get_student_prediction_history
from src.config import DB_PATH
from src.visualizations import base
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    f"Welcome back, {name}",
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

# ----------------- TOP KPI ROW (REFERENCE STYLE) -----------------
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="campus-card" style="padding: 18px 20px; margin-bottom: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Total Students</span>
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #EFF6FF; color: #2563EB; display: flex; align-items: center; justify-content: center; font-size: 1rem;">👥</div>
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">{total_students:,}</div>
        <div style="font-size: 0.75rem; color: #2563EB; font-weight: 600; margin-top: 4px;">{counts['new_students']} newly enrolled</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="campus-card" style="padding: 18px 20px; margin-bottom: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Placed Students</span>
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #F0FDF4; color: #16A34A; display: flex; align-items: center; justify-content: center; font-size: 1rem;">✓</div>
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #16A34A; letter-spacing: -0.02em;">{placed_students:,}</div>
        <div style="font-size: 0.75rem; color: #16A34A; font-weight: 600; margin-top: 4px;">Recruitment Cleared</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="campus-card" style="padding: 18px 20px; margin-bottom: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Not Placed</span>
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #FEF2F2; color: #DC2626; display: flex; align-items: center; justify-content: center; font-size: 1rem;">⚠️</div>
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #DC2626; letter-spacing: -0.02em;">{not_placed:,}</div>
        <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; margin-top: 4px;">Training in Progress</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="campus-card" style="padding: 18px 20px; margin-bottom: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Placement Rate</span>
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #EFF6FF; color: #2563EB; display: flex; align-items: center; justify-content: center; font-size: 1rem;">📈</div>
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">{placement_rate:.1f}%</div>
        <div style="font-size: 0.75rem; color: #16A34A; font-weight: 600; margin-top: 4px;">Campus Benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="campus-card" style="padding: 18px 20px; margin-bottom: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Average CGPA</span>
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #F5F3FF; color: #7C3AED; display: flex; align-items: center; justify-content: center; font-size: 1rem;">🎓</div>
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">{avg_cgpa:.2f}</div>
        <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; margin-top: 4px;">Aptitude: {avg_aptitude:.1f}/100</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ----------------- VISUAL ANALYTICS GRID: LARGE CHART (LEFT) + RECENT ACTIVITY (RIGHT) -----------------
c_main_chart, c_activity = st.columns([1.6, 1.1], gap="large")

with c_main_chart:
    st.markdown("### 🏛️ Placement Distribution by Department")
    branch_df = df.groupby(["branch", "placement_status"]).size().reset_index(name="Students")
    fig_bar = px.bar(
        branch_df, x="branch", y="Students", color="placement_status", barmode="group",
        title="Placed vs. Not Placed by Engineering Department",
        color_discrete_map={"Placed": "#2563EB", "Not Placed": "#94A3B8"}
    )
    fig_bar = base(fig_bar, "Placed vs. Not Placed by Engineering Department")
    st.plotly_chart(fig_bar, use_container_width=True)

with c_activity:
    st.markdown("### ⚡ Recent Placement Activity")
    
    # Query actual predictions from SQLite
    recent_history = get_student_prediction_history(None)
    
    if len(recent_history) > 0:
        st.markdown("""
        <div class="campus-card" style="padding: 16px; margin-bottom: 14px;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
                Latest Evaluated Candidates
            </div>
        """, unsafe_allow_html=True)
        for _, r in recent_history.head(4).iterrows():
            st_color = "#16A34A" if r["predicted_status"] == "Placed" else "#DC2626"
            st_badge = "badge-success" if r["predicted_status"] == "Placed" else "badge-danger"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 8px 10px; border-bottom: 1px solid #F1F5F9;">
                <div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: #0F172A;">{r['student_id']}</div>
                    <div style="font-size: 0.74rem; color: #64748B;">{r['email']}</div>
                </div>
                <div style="text-align: right;">
                    <span class="badge-pill {st_badge}">{r['predicted_status']}</span>
                    <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">{float(r['probability'])*100:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No prediction executions recorded yet.")

    # Breakdown donut chart
    status_df = df["placement_status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    fig_pie = px.pie(
        status_df, names="Status", values="Count", hole=0.6,
        color="Status",
        color_discrete_map={"Placed": "#16A34A", "Not Placed": "#94A3B8"}
    )
    fig_pie = base(fig_pie, "Campus Placement Ratio")
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ----------------- SECONDARY CHARTS ROW -----------------
c_sec1, c_sec2 = st.columns([1, 1], gap="medium")

with c_sec1:
    st.markdown("### 📊 Academic CGPA Distribution")
    fig_hist = px.histogram(
        df, x="cgpa", color="placement_status", nbins=30,
        title="CGPA Frequency Breakdown across Campus",
        color_discrete_map={"Placed": "#2563EB", "Not Placed": "#94A3B8"},
        opacity=0.85
    )
    fig_hist = base(fig_hist, "CGPA Frequency Breakdown across Campus")
    st.plotly_chart(fig_hist, use_container_width=True)

with c_sec2:
    st.markdown("### 💼 Practical Internships vs Placement Rate")
    intern_group = df.groupby("internships_count")["placement_prediction"].agg(["count", "mean"]).reset_index()
    intern_group["Placement Rate %"] = intern_group["mean"] * 100
    fig_line = px.line(
        intern_group, x="internships_count", y="Placement Rate %",
        markers=True,
        title="Placement Probability by Number of Completed Internships",
        labels={"internships_count": "Internships Completed"}
    )
    fig_line = base(fig_line, "Placement Probability by Number of Completed Internships")
    st.plotly_chart(fig_line, use_container_width=True)

# ----------------- SYSTEM STATUS FOOTER -----------------
st.markdown(f"""
<div class="campus-card" style="margin-top: 14px; padding: 18px 22px;">
    <div style="font-weight: 700; color: #2563EB; font-size: 0.95rem; margin-bottom: 4px;">Data Warehouse Infrastructure Status</div>
    <div style="color: #64748B; font-size: 0.85rem;">
        SQLite Star-Schema Database: <code>outputs/placement_dw.sqlite</code> &bull; Central Fact Table: <code>FactPlacement</code> ({total_students:,} rows) &bull; Relational Dimension Tables: <code>DimStudent</code>, <code>DimAcademic</code>, <code>DimSkills</code>, <code>DimEngagement</code>, <code>DimPlacement</code>.
    </div>
</div>
""", unsafe_allow_html=True)
