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
    "AI Placement Prediction Engine",
    "Evaluate your real-time likelihood of campus placement using our trained institutional classification model. Results are estimated probabilities based on 15,000 university placement records.",
    tag="Predictive Inference"
)

# Check if student profile is completed
if not is_student_profile_completed(email):
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 44px 30px; margin: 24px 0; border: 1.5px dashed rgba(244, 63, 94, 0.45); border-radius: 20px;">
        <div style="font-size: 3.5rem; margin-bottom: 14px;">🔮</div>
        <h2 style="color: #f8fafc; font-size: 1.6rem; font-weight: 800; margin-bottom: 10px;">
            Candidate Profile Incomplete
        </h2>
        <p style="color: #94a3b8; font-size: 1.02rem; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.6;">
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
    run_pred = st.button("🔮 Predict My Placement", type="primary", use_container_width=True)
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
    card_class = "prediction-placed" if is_placed else "prediction-unplaced"
    icon = "✓" if is_placed else "⚠️"
    status_text = "PLACED" if is_placed else "NOT PLACED"
    status_color = "#34d399" if is_placed else "#fb7185"

    st.markdown(f"""
    <div class="prediction-card {card_class}">
        <div style="font-size: 0.95rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
            MODEL PLACEMENT PREDICTION OUTCOME
        </div>
        <div style="font-size: 3.2rem; font-weight: 900; color: {status_color}; margin: 8px 0;">
            {icon} {status_text}
        </div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 6px;">
            Estimated Probability: <span style="color: {status_color}; font-size: 1.6rem; font-weight: 800;">{res['probability_percent']}%</span>
        </div>
        <div style="font-size: 0.88rem; color: #cbd5e1; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            <b>Readiness Tier:</b> <span style="color:#38bdf8; font-weight:700;">{res['readiness_level']}</span> &bull; 
            Inference generated by <b>{res['model_name']}</b> based on your saved profile parameters.<br>
            <span style="font-size:0.78rem; opacity:0.8;">Note: This prediction is a data-driven estimate based on historical patterns, not an absolute guarantee.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Drivers & Areas to Improve
    st.markdown("### 💡 Why this prediction?")
    col_str, col_imp = st.columns(2, gap="medium")
    
    with col_str:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #10b981; height: 100%;">
            <h4 style="margin-top:0; color:#34d399;">🌟 Profile Strengths & Competitive Drivers</h4>
        """, unsafe_allow_html=True)
        if res.get("strengths"):
            for s in res["strengths"]:
                st.markdown(f"• **{s['title']}**: {s['detail']}")
        else:
            st.write("Profile is currently developing towards placed benchmark levels.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_imp:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #f43f5e; height: 100%;">
            <h4 style="margin-top:0; color:#fb7185;">📈 Top Recommended Improvement Areas</h4>
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
