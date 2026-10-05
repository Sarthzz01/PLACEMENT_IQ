import streamlit as st
import pandas as pd
from src.auth import require_student
from src.preprocessing import load_data
from src.database import get_student_profile, log_prediction_to_db, get_system_setting, is_student_profile_completed
from src.prediction import predict_placement, get_production_model_name
from src.ui import css, hero, render_top_navbar

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Placement Prediction",
    "See how your current profile performs against the trained placement model.",
    tag="Placement Intelligence"
)

# Check if student profile is completed
if not is_student_profile_completed(email):
    st.markdown("""
    <div class="campus-card" style="text-align: center; padding: 40px 24px; margin: 20px 0; border: 1.5px dashed #93C5FD;">
        <div style="font-size: 3rem; margin-bottom: 12px;">🎯</div>
        <h2 style="color: #0F172A; font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">
            Candidate Profile Incomplete
        </h2>
        <p style="color: #64748B; font-size: 0.96rem; max-width: 580px; margin: 0 auto 24px auto; line-height: 1.6;">
            The AI Placement Prediction engine evaluates your actual CGPA, attendance, solved coding challenges, and competencies to forecast recruitment readiness. Please submit your profile parameters first.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📝 Complete My Profile to Unlock Prediction", type="primary", use_container_width=True):
            st.switch_page("pages/2_Student_Profile.py")
    st.stop()

# Fetch current verified student profile from SQLite database
student_dict = get_student_profile(email)
prod_model_name = get_production_model_name()

# Current Profile Summary Pill Card
st.markdown("### 📋 Student Profile Under Evaluation")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Branch / Age", f"{student_dict.get('branch', 'CSE')}", f"Age: {student_dict.get('age', 21)}")
with c2:
    st.metric("CGPA / Backlogs", f"{float(student_dict.get('cgpa', 8.0)):.2f}", f"{student_dict.get('backlogs', 0)} Active Backlogs")
with c3:
    st.metric("Attendance", f"{float(student_dict.get('attendance_percentage', 85)):.1f}%", "Classroom Discipline")
with c4:
    st.metric("Experience", f"{student_dict.get('internships_count', 1)} Internships", f"{student_dict.get('projects_count', 3)} Projects")
with c5:
    st.metric("Coding & Aptitude", f"DSA: {student_dict.get('dsa_questions_solved', 200)}", f"Aptitude: {float(student_dict.get('aptitude_score', 75)):.0f}")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Prediction Button
col_btn, col_info = st.columns([1.2, 2])
with col_btn:
    run_pred = st.button("🎯 Predict My Placement", type="primary", use_container_width=True)
with col_info:
    st.caption(f"Active Production Model: **{prod_model_name}** &bull; Trained on certified campus placement dataset.")

if run_pred or "last_student_prediction" in st.session_state:
    if run_pred:
        with st.spinner(f"Evaluating candidate vector through trained {prod_model_name}..."):
            df_ref = load_data()
            res = predict_placement(student_dict, reference_df=df_ref, model_name=prod_model_name)
            st.session_state.last_student_prediction = res
            
            # Log to persistent SQLite database
            log_prediction_to_db(
                student_id=user_id,
                email=email,
                status=res["status"],
                prob=res["probability"],
                model_name=res.get("model_name", prod_model_name),
                features=student_dict,
                evaluated_by="Student Self-Assessment"
            )
    else:
        res = st.session_state.last_student_prediction

    # Render Prediction Result Card
    is_placed = res["status"] == "Placed"
    status_text = "PLACED" if is_placed else "NOT PLACED"
    status_color = "#16A34A" if is_placed else "#DC2626"
    card_bg = "#F0FDF4" if is_placed else "#FEF2F2"
    card_border = "#86EFAC" if is_placed else "#FECACA"
    icon = "✓" if is_placed else "⚠️"

    st.markdown(f"""
    <div style="background: {card_bg}; border: 1.5px solid {card_border}; border-radius: 14px; padding: 28px 24px; text-align: center; margin: 18px 0; box-shadow: 0 2px 8px rgba(15,23,42,0.04);">
        <div style="font-size: 0.82rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">
            PLACEMENT PREDICTION
        </div>
        <div style="font-size: 2.8rem; font-weight: 900; color: {status_color}; margin: 6px 0;">
            {icon} {status_text}
        </div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
            Estimated Probability: <span style="color: {status_color}; font-size: 1.5rem; font-weight: 800;">{res['probability_percent']}%</span>
        </div>
        <div style="font-size: 0.88rem; color: #475569; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            <b>Readiness Tier:</b> <span style="color:#2563EB; font-weight:700;">{res['readiness_level']}</span> &bull; 
            Inference generated by <b>{res['model_name']}</b> based on your saved profile parameters.<br>
            <span style="font-size:0.78rem; color:#64748B;">Note: This prediction is a data-driven estimate based on historical placement trends.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Drivers & Areas to Improve
    st.markdown("### 💡 What can I improve?")
    col_str, col_imp = st.columns(2, gap="medium")
    
    with col_str:
        st.markdown("""
        <div class="campus-card" style="border-left: 4px solid #16A34A; height: 100%;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #16A34A; margin-bottom: 8px;">
                🌟 Profile Strengths & Competitive Drivers
            </div>
        """, unsafe_allow_html=True)
        if res.get("strengths"):
            for s in res["strengths"]:
                st.markdown(f"• **{s['title']}**: {s['detail']}")
        else:
            st.write("Profile is currently developing towards placed benchmark levels.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_imp:
        st.markdown("""
        <div class="campus-card" style="border-left: 4px solid #F59E0B; height: 100%;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #D97706; margin-bottom: 8px;">
                📈 Recommended Improvement Areas
            </div>
        """, unsafe_allow_html=True)
        if res.get("top_improvements"):
            for imp in res["top_improvements"][:4]:
                st.markdown(f"• **{imp['title']}** (Gap: `{imp['gap']} {imp['unit']}`): {imp['advice']}")
        else:
            st.write("Your profile meets or exceeds the placed candidate median across all evaluated parameters!")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("📈 Open Tailored Improvement Plan", use_container_width=True, type="primary"):
            st.switch_page("pages/5_Improvement_Plan.py")
    with c_btn2:
        if st.button("📜 View Historical Predictions Timeline", use_container_width=True):
            st.switch_page("pages/6_Prediction_History.py")
