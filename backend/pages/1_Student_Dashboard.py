import streamlit as st
import pandas as pd
from src.auth import require_student
from src.preprocessing import load_data
from src.database import get_student_profile, get_student_prediction_history, get_student_feedback, is_student_profile_completed
from src.prediction import predict_placement
from src.recommendations import generate_recommendations
from src.visualizations import radar_comparison
from src.ui import css, hero, render_top_navbar, completion_gauge

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    f"Welcome back, {name}",
    "Here's an overview of your placement readiness, competency radar benchmarks, and customized improvement plan.",
    tag="Student Placement Platform"
)

# Check if the student has actively filled and submitted their profile data
profile_completed = is_student_profile_completed(email)

if not profile_completed:
    # ----------------- EMPTY ONBOARDING STATE FOR NEW USERS -----------------
    st.markdown("""
    <div class="campus-card" style="text-align: center; padding: 40px 24px; margin: 18px 0 24px 0; border: 1.5px dashed #93C5FD; border-radius: 14px; background: #FFFFFF;">
        <div style="font-size: 2.8rem; margin-bottom: 10px;">📋</div>
        <h2 style="color: #0F172A; font-size: 1.45rem; font-weight: 800; margin: 0 0 8px 0;">
            Candidate Placement Profile Not Completed Yet
        </h2>
        <p style="color: #64748B; font-size: 0.94rem; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.6;">
            Welcome to <b>Placement IQ</b>! To unlock your real-time <b>AI Placement Prediction</b>, 
            <b>Competency Radar Benchmark</b>, and <b>Personalized Improvement Plan</b>, please complete your academic and coding profile.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_b1, c_b2, c_b3 = st.columns([1, 2, 1])
    with c_b2:
        if st.button("📝 Complete My Candidate Profile Now", type="primary", use_container_width=True):
            st.switch_page("pages/2_Student_Profile.py")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🌟 What You Will Unlock After Submitting Your Details:")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="campus-card" style="padding: 22px; height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🎯</div>
            <h4 style="color: #2563EB; margin: 0 0 8px 0;">AI Placement Prediction</h4>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0; line-height: 1.6;">
                Get an instant probabilistic likelihood of placement calculated by machine learning models trained on 15,000 university placement records.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        col_f2.markdown("""
        <div class="campus-card" style="padding: 22px; height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🕸️</div>
            <h4 style="color: #2563EB; margin: 0 0 8px 0;">Competency Benchmark Radar</h4>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0; line-height: 1.6;">
                Visually benchmark your CGPA, attendance, DSA problem count, and coding scores directly against the median of placed alumni cohorts.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class="campus-card" style="padding: 22px; height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">📈</div>
            <h4 style="color: #16A34A; margin: 0 0 8px 0;">Targeted Action Roadmap</h4>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0; line-height: 1.6;">
                Receive specific, data-backed recommendations identifying your exact performance gaps and high-priority areas to improve recruitment readiness.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ----------------- FILLED PROFILE: LOAD ACTUAL STUDENT DATA -----------------
profile = get_student_profile(email)

# Fetch student prediction history & feedback
history_df = get_student_prediction_history(email)
feedback_df = get_student_feedback(email)

# Determine latest prediction outcome
if len(history_df) > 0:
    latest_hist = history_df.iloc[0]
    pred_status = latest_hist["predicted_status"]
    pred_prob = float(latest_hist["probability"])
    pred_model = latest_hist.get("model_name", "Random Forest")
    pred_evaluator = latest_hist.get("evaluated_by", "Model Inference")
else:
    # Run dynamic prediction on actual filled profile
    pred_res = predict_placement(profile)
    pred_status = pred_res["status"]
    pred_prob = pred_res["probability"]
    pred_model = pred_res.get("model_name", "Random Forest")
    pred_evaluator = "Initial Model Inference"

# Profile completeness calculation
key_fields = ["cgpa", "attendance_percentage", "dsa_questions_solved", "internships_count", "projects_count", "aptitude_score", "coding_skill_score"]
filled = sum(1 for k in key_fields if profile.get(k) is not None)
comp_pct = min(100, int((filled / len(key_fields)) * 100))

# ----------------- TOP METRIC KPI CARDS -----------------
is_placed = pred_status == "Placed"
status_icon = "✓" if is_placed else "⚠️"
status_badge = f"{pred_prob*100:.1f}% Likelihood"
coding_score_pct = int((float(profile.get('coding_skill_score', 7)) / 10.0) * 100)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Placement Prediction", f"{pred_status.upper()}", f"{status_badge}")
with k2:
    st.metric("Profile Completion", f"{comp_pct}%", "Candidate Profile")
with k3:
    st.metric("Academic CGPA", f"{float(profile.get('cgpa', 8.0)):.2f}", f"Branch: {profile.get('branch', 'CSE')}")
with k4:
    st.metric("Skill Score", f"{coding_score_pct}%", f"DSA: {profile.get('dsa_questions_solved', 200)} Solved")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Profile completeness bar
completion_gauge(comp_pct, ["External Profile URLs", "Mock Interview Score"] if comp_pct < 100 else None)

# ----------------- ADMIN FEEDBACK BANNER (IF PRESENT) -----------------
if len(feedback_df) > 0:
    latest_fb = feedback_df.iloc[0]
    p_badge = "badge-danger" if latest_fb["priority"] == "High" else "badge-warning"
    st.markdown(f"""
    <div class="campus-card" style="border-left: 4px solid #2563EB; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-weight: 700; font-size: 1rem; color: #0F172A;">
                🛡️ Placement Assessment & Faculty Feedback
            </div>
            <span class="badge-pill {p_badge}">Priority: {latest_fb['priority']}</span>
        </div>
        <p style="color: #334155; font-size: 0.92rem; margin: 0 0 8px 0; line-height: 1.6;">
            <b>Faculty Assessment:</b> "{latest_fb['recommendation']}"
        </p>
        <div style="font-size: 0.78rem; color: #64748B;">
            Reviewed by <b>{latest_fb['admin_name']}</b> on <code>{latest_fb['created_at']}</code> &bull; Placement Outlook: <b>{latest_fb['prediction']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN DASHBOARD SECTIONS -----------------
col_bench, col_action = st.columns([1.5, 1.2], gap="large")

with col_bench:
    st.markdown("""
    <div style="font-weight: 700; font-size: 1.1rem; color: #0F172A; margin-bottom: 4px;">
        Placement Readiness Overview
    </div>
    <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 12px;">
        Visualizing your competencies compared to the median of placed students:
    </div>
    """, unsafe_allow_html=True)

    df_ref = load_data()
    placed_ref = df_ref[df_ref["placement_prediction"] == 1]

    cgpa_val = float(profile.get("cgpa", 7.5))
    att_val = float(profile.get("attendance_percentage", 80))
    apt_val = float(profile.get("aptitude_score", 70))
    code_val = float(profile.get("coding_skill_score", 7))
    dsa_val = float(profile.get("dsa_questions_solved", 150))

    student_scores = {
        "CGPA (×10)": min(100, cgpa_val * 10),
        "Attendance %": att_val,
        "Aptitude Score": apt_val,
        "Coding Skill (×10)": min(100, code_val * 10),
        "DSA Practice": min(100, (dsa_val / 400.0) * 100)
    }

    cohort_scores = {
        "CGPA (×10)": min(100, placed_ref["cgpa"].median() * 10),
        "Attendance %": placed_ref["attendance_percentage"].median(),
        "Aptitude Score": placed_ref["aptitude_score"].median(),
        "Coding Skill (×10)": min(100, placed_ref["coding_skill_score"].median() * 10),
        "DSA Practice": min(100, (placed_ref["dsa_questions_solved"].median() / 400.0) * 100)
    }

    fig_rad = radar_comparison(student_scores, cohort_scores)
    st.plotly_chart(fig_rad, use_container_width=True)

with col_action:
    st.markdown("""
    <div style="font-weight: 700; font-size: 1.1rem; color: #0F172A; margin-bottom: 4px;">
        Recent Prediction / Placement Status
    </div>
    <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 12px;">
        Current standing from the active production model:
    </div>
    """, unsafe_allow_html=True)

    card_class = "prediction-placed" if is_placed else "prediction-unplaced"
    status_color = "#16A34A" if is_placed else "#DC2626"
    
    st.markdown(f"""
    <div class="prediction-card {card_class}" style="margin-top: 0; padding: 22px;">
        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
            PLACEMENT STATUS
        </div>
        <div style="font-size: 2.2rem; font-weight: 900; color: {status_color}; margin: 4px 0;">
            {status_icon} {pred_status.upper()}
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
            Estimated Likelihood: <span style="color: {status_color}; font-weight: 800;">{pred_prob*100:.1f}%</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B; line-height: 1.5;">
            Evaluated by <b>{pred_model}</b> &bull; {pred_evaluator}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Priority Areas to Improve
    st.markdown("""
    <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin: 16px 0 8px 0;">
        Areas to Improve
    </div>
    """, unsafe_allow_html=True)

    rec_data = generate_recommendations(profile, df_ref)
    top_gaps = rec_data["top_improvements"]

    if top_gaps:
        for g in top_gaps[:2]:
            p_badge = "badge-danger" if g["priority"] in ["Critical", "High"] else "badge-warning"
            st.markdown(f"""
            <div class="campus-card" style="margin-bottom: 10px; padding: 14px 16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #2563EB; font-size: 0.9rem;">{g['title']}</span>
                    <span class="badge-pill {p_badge}">{g['priority']} Priority</span>
                </div>
                <div style="font-size: 0.82rem; color: #475569; margin-bottom: 4px;">
                    Your value: <b>{g['student_val']}</b> &bull; Dataset median: <b>{g['benchmark_val']}</b>
                </div>
                <div style="font-size: 0.8rem; color: #64748B; line-height: 1.4;">
                    {g['advice']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🌟 Outstanding profile! All major placement metrics exceed the campus benchmark median.")

    if st.button("📋 View Complete Improvement Plan", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Improvement_Plan.py")

# ----------------- QUICK NAVIGATION TILES -----------------
st.markdown("---")
st.markdown("### 🚀 Quick Navigation")

q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("👤 My Profile", use_container_width=True):
        st.switch_page("pages/2_Student_Profile.py")
with q2:
    if st.button("🎯 Placement Prediction", use_container_width=True):
        st.switch_page("pages/3_Placement_Prediction.py")
with q3:
    if st.button("🕸️ Skill Analysis", use_container_width=True):
        st.switch_page("pages/4_Skill_Analysis.py")
with q4:
    if st.button("📜 Prediction History", use_container_width=True):
        st.switch_page("pages/6_Prediction_History.py")
