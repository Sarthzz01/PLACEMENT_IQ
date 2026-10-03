import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.auth import require_student
from src.preprocessing import load_data
from src.database import get_student_profile, is_student_profile_completed
from src.visualizations import radar_comparison
from src.ui import css, hero, render_top_navbar, label

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Student Skill & Competency Analysis",
    "Benchmark your academic standing, coding depth, problem-solving volume, and project portfolio against 15,000 students and placed alumni medians.",
    tag="Competency Intelligence"
)

# Check if student profile is completed
if not is_student_profile_completed(email):
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 44px 30px; margin: 24px 0; border: 1.5px dashed rgba(129, 140, 248, 0.45); border-radius: 20px;">
        <div style="font-size: 3.5rem; margin-bottom: 14px;">🕸️</div>
        <h2 style="color: #f8fafc; font-size: 1.6rem; font-weight: 800; margin-bottom: 10px;">
            Competency Radar Locked
        </h2>
        <p style="color: #94a3b8; font-size: 1.02rem; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.6;">
            Your competency radar compares your CGPA, attendance, DSA problem count, and coding skills against 15,000 university records. Please enter your profile details first.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📝 Complete My Profile for Skill Analysis", type="primary", use_container_width=True):
            st.switch_page("pages/2_Student_Profile.py")
    st.stop()

profile = get_student_profile(email) or {}
df = load_data()
placed_df = df[df["placement_prediction"] == 1]

# ----------------- SECTION 1: RADAR BENCHMARK -----------------
st.markdown("### 🕸️ Multi-Dimensional Competency Radar")
st.caption("Side-by-side radar comparison against campus placed median:")

c_radar, c_summary = st.columns([1.7, 1.3], gap="large")

cgpa_val = float(profile.get("cgpa", 7.5))
att_val = float(profile.get("attendance_percentage", 80))
apt_val = float(profile.get("aptitude_score", 70))
code_val = float(profile.get("coding_skill_score", 7))
dsa_val = float(profile.get("dsa_questions_solved", 150))
proj_val = float(profile.get("projects_count", 2))

student_scores = {
    "CGPA (×10)": min(100, cgpa_val * 10),
    "Attendance %": att_val,
    "Aptitude Score": apt_val,
    "Coding Skill (×10)": min(100, code_val * 10),
    "DSA Practice": min(100, (dsa_val / 400.0) * 100),
    "Projects (×10)": min(100, proj_val * 20)
}

cohort_scores = {
    "CGPA (×10)": min(100, placed_df["cgpa"].median() * 10),
    "Attendance %": placed_df["attendance_percentage"].median(),
    "Aptitude Score": placed_df["aptitude_score"].median(),
    "Coding Skill (×10)": min(100, placed_df["coding_skill_score"].median() * 10),
    "DSA Practice": min(100, (placed_df["dsa_questions_solved"].median() / 400.0) * 100),
    "Projects (×10)": min(100, placed_df["projects_count"].median() * 20)
}

with c_radar:
    fig_radar = radar_comparison(student_scores, cohort_scores)
    st.plotly_chart(fig_radar, use_container_width=True)

with c_summary:
    st.markdown("#### 📊 Key Feature Comparisons")
    
    comparisons = [
        ("CGPA", cgpa_val, placed_df["cgpa"].median(), "CGPA"),
        ("DSA Solved", dsa_val, placed_df["dsa_questions_solved"].median(), "problems"),
        ("Coding Score", code_val, placed_df["coding_skill_score"].median(), "/ 10"),
        ("Aptitude Score", apt_val, placed_df["aptitude_score"].median(), "/ 100"),
        ("Internships", float(profile.get("internships_count", 0)), placed_df["internships_count"].median(), "completed"),
        ("Projects", proj_val, placed_df["projects_count"].median(), "completed")
    ]
    
    for f_name, s_v, p_v, u in comparisons:
        diff = s_v - p_v
        d_color = "#34d399" if diff >= 0 else "#fb7185"
        d_sign = "+" if diff >= 0 else ""
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 10px 14px; background: rgba(15, 23, 42, 0.6); border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.06);">
            <div>
                <b style="color:#f8fafc; font-size:0.9rem;">{f_name}</b><br>
                <span style="font-size:0.75rem; color:#94a3b8;">Placed Median: {p_v:.1f} {u}</span>
            </div>
            <div style="text-align:right;">
                <b style="color:#f8fafc; font-size:0.95rem;">{s_v:.1f} {u}</b><br>
                <span style="font-size:0.75rem; color:{d_color}; font-weight:700;">{d_sign}{diff:.1f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ----------------- SECTION 2: CATEGORY DEEP DIVES -----------------
st.markdown("### 🔬 Category-by-Category Feature Distribution")

tab_acad, tab_code, tab_apt, tab_proj = st.tabs([
    "🎓 1. Academics",
    "💻 2. Coding & DSA",
    "🧠 3. Aptitude & Interviews",
    "💼 4. Experience & Projects"
])

with tab_acad:
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("#### CGPA Position on Campus Curve")
        fig_cgpa = px.histogram(
            df, x="cgpa", color="placement_status", nbins=30,
            title="CGPA Frequency Distribution",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
        )
        fig_cgpa.add_vline(x=cgpa_val, line_dash="dash", line_color="#38bdf8", annotation_text=f"You: {cgpa_val:.2f}")
        fig_cgpa.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cgpa, use_container_width=True)
    with col_a2:
        st.markdown("#### Attendance % vs Placement Status")
        fig_att = px.box(
            df, x="placement_status", y="attendance_percentage",
            title="Attendance Spread by Placement Outcome",
            color="placement_status",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#f43f5e"}
        )
        fig_att.add_hline(y=att_val, line_dash="dash", line_color="#38bdf8", annotation_text=f"Your Attendance: {att_val:.1f}%")
        fig_att.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_att, use_container_width=True)

with tab_code:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### DSA Problems Solved vs Campus Distribution")
        fig_dsa = px.histogram(
            df, x="dsa_questions_solved", color="placement_status", nbins=25,
            title="DSA Practice Distribution",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
        )
        fig_dsa.add_vline(x=dsa_val, line_dash="dash", line_color="#c084fc", annotation_text=f"You: {int(dsa_val)}")
        fig_dsa.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_dsa, use_container_width=True)
    with col_c2:
        st.markdown("#### Coding Skill Score vs CGPA Scatter")
        sample_df = df.sample(min(2000, len(df)), random_state=42)
        fig_scat = px.scatter(
            sample_df, x="cgpa", y="coding_skill_score", color="placement_status",
            title="CGPA vs. Technical Coding Skill",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#f43f5e"},
            opacity=0.6
        )
        fig_scat.add_trace(go.Scatter(
            x=[cgpa_val], y=[code_val], mode="markers",
            marker=dict(size=14, color="#38bdf8", symbol="star", line=dict(color="#ffffff", width=2)),
            name="Your Position"
        ))
        fig_scat.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scat, use_container_width=True)

with tab_apt:
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        st.markdown("#### Aptitude Score Distribution")
        fig_apt = px.histogram(
            df, x="aptitude_score", color="placement_status", nbins=25,
            title="Campus Aptitude Scores",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
        )
        fig_apt.add_vline(x=apt_val, line_dash="dash", line_color="#fbbf24", annotation_text=f"You: {apt_val:.1f}")
        fig_apt.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_apt, use_container_width=True)
    with col_ap2:
        st.markdown("#### Communication vs Mock Interview Score")
        comm_val = float(profile.get("communication_score", 7.0))
        mock_v = float(profile.get("mock_interview_score", 7.0))
        fig_comm = px.box(
            df, x="placement_status", y="communication_score",
            title="Communication Scores by Outcome",
            color="placement_status",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#f43f5e"}
        )
        fig_comm.add_hline(y=comm_val, line_dash="dash", line_color="#38bdf8", annotation_text=f"You: {comm_val:.1f}")
        fig_comm.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_comm, use_container_width=True)

with tab_proj:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Completed Internships Impact")
        intern_dist = df.groupby(["internships_count", "placement_status"]).size().reset_index(name="Count")
        fig_int = px.bar(
            intern_dist, x="internships_count", y="Count", color="placement_status", barmode="group",
            title="Internships vs Placement Outcomes",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
        )
        fig_int.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_int, use_container_width=True)
    with col_p2:
        st.markdown("#### Completed Projects Spread")
        proj_dist = df.groupby(["projects_count", "placement_status"]).size().reset_index(name="Count")
        fig_prj = px.bar(
            proj_dist, x="projects_count", y="Count", color="placement_status", barmode="group",
            title="Completed Projects vs Placement Outcomes",
            color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
        )
        fig_prj.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_prj, use_container_width=True)
