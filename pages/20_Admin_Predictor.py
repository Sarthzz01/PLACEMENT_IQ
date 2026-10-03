import streamlit as st
import pandas as pd
from src.auth import require_admin
from src.preprocessing import load_data, EXPECTED, BASE_NUMERIC
from src.database import (
    get_all_student_profiles_df, log_prediction_to_db, save_admin_feedback
)
from src.prediction import predict_placement, batch_predict, get_production_model_name
from src.config import BRANCH_OPTIONS, GENDER_OPTIONS, TRAINING_OPTIONS
from src.ui import css, hero, render_top_navbar, label

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Placement Prediction Center & Batch Assessment",
    "Evaluate candidate likelihoods across registered student records or upload external CSV rosters for automated batch placement scoring.",
    tag="Predictive Inference Center"
)

df_ref = load_data()
profiles_df = get_all_student_profiles_df()

tab_db, tab_single, tab_batch = st.tabs([
    "👥 1. Assess Registered Student",
    "👤 2. Ad-Hoc Candidate Profile",
    "📁 3. High-Throughput Batch CSV Scoring"
])

# ----------------- TAB 1: ASSESS REGISTERED STUDENT -----------------
with tab_db:
    st.markdown("### 👥 Evaluate Registered Student from Database")
    st.caption("Select a candidate to inspect features, execute model inference, and record feedback directly to their portal:")

    if len(profiles_df) > 0:
        sel_sid = st.selectbox(
            "Select Candidate to Evaluate",
            profiles_df["student_id"].tolist(),
            format_func=lambda s: f"{s} — {profiles_df[profiles_df['student_id']==s].iloc[0]['name']} ({profiles_df[profiles_df['student_id']==s].iloc[0]['email']})",
            key="db_eval_sid"
        )
        cand = profiles_df[profiles_df["student_id"] == sel_sid].iloc[0].to_dict()

        col_cand_info, col_cand_run = st.columns([1.5, 1.5], gap="large")
        with col_cand_info:
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#38bdf8;">Candidate: {cand.get('name')}</h4>
                <div style="font-size:0.88rem; color:#cbd5e1; line-height: 1.7;">
                    <b>Branch:</b> {cand.get('branch')} &bull; <b>CGPA:</b> {float(cand.get('cgpa', 0)):.2f} &bull; <b>Attendance:</b> {float(cand.get('attendance_percentage', 0)):.1f}%<br>
                    <b>DSA Solved:</b> {cand.get('dsa_questions_solved', 0)} &bull; <b>LeetCode:</b> {cand.get('leetcode_questions_solved', 0)}<br>
                    <b>Internships:</b> {cand.get('internships_count', 0)} &bull; <b>Projects:</b> {cand.get('projects_count', 0)} &bull; <b>Backlogs:</b> {cand.get('backlogs', 0)}<br>
                    <b>Aptitude:</b> {float(cand.get('aptitude_score', 0)):.1f} &bull; <b>Coding:</b> {float(cand.get('coding_skill_score', 0)):.1f} / 10
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_cand_run:
            m_choice = st.selectbox("Select Model for Evaluation", ["Random Forest", "Decision Tree", "Naive Bayes"], key="db_eval_m")
            if st.button("🔮 Run Prediction for Candidate", type="primary", use_container_width=True, key="btn_run_db_pred"):
                db_pred_res = predict_placement(cand, reference_df=df_ref, model_name=m_choice)
                st.session_state.db_eval_res = db_pred_res
                
                log_prediction_to_db(
                    student_id=cand.get("student_id"),
                    email=cand.get("email"),
                    status=db_pred_res["status"],
                    prob=db_pred_res["probability"],
                    model_name=db_pred_res["model_name"],
                    features=cand,
                    evaluated_by=f"Admin: {name}"
                )

        if "db_eval_res" in st.session_state:
            d_res = st.session_state.db_eval_res
            st_color = "#34d399" if d_res["status"] == "Placed" else "#fb7185"
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid {st_color}; border-radius: 14px; padding: 18px; margin: 16px 0; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: 900; color: {st_color};">
                    {'✓' if d_res['status']=='Placed' else '⚠️'} {d_res['status'].upper()} ({d_res['probability_percent']}%)
                </div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px;">
                    Evaluated via <b>{d_res['model_name']}</b> &bull; Readiness: <b>{d_res['readiness_level']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### ✍️ Save Feedback to Student Dashboard")
            with st.form("cand_feedback_form"):
                fb_verdict = st.selectbox("Faculty Verdict", ["Placed", "Not Placed", "High Potential", "At Risk"], key="fb_v_sel")
                fb_prio = st.selectbox("Priority", ["High", "Medium", "Low"], index=1, key="fb_p_sel")
                fb_text = st.text_area("Official Feedback & Advice", value=f"Placement Likelihood: {d_res['probability_percent']}%. Focus on {d_res['top_improvements'][0]['title'] if d_res['top_improvements'] else 'maintaining momentum'}.")
                submit_cand_fb = st.form_submit_button("💾 Dispatch to Student Portal", type="primary", use_container_width=True)

                if submit_cand_fb:
                    save_admin_feedback(
                        student_id=cand.get("student_id"),
                        email=cand.get("email"),
                        prediction=fb_verdict,
                        recommendation=fb_text.strip(),
                        priority=fb_prio,
                        admin_name=name
                    )
                    st.success("✅ Feedback successfully dispatched to candidate's Student Dashboard!")
    else:
        st.info("No student accounts currently registered in database.")

# ----------------- TAB 2: AD-HOC CANDIDATE FORM -----------------
with tab_single:
    st.markdown("### 👤 Ad-Hoc Candidate Profile Evaluation")
    st.caption("Input custom test vector to evaluate classification inference without saving to student database:")

    with st.form("admin_single_predict_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            branch = st.selectbox("Engineering Branch", BRANCH_OPTIONS, index=0, key="ah_branch")
            gender = st.selectbox("Gender", GENDER_OPTIONS, index=0, key="ah_gender")
            age = st.slider("Age", 18, 30, 21, key="ah_age")
            cgpa = st.slider("CGPA", 5.0, 10.0, 8.2, 0.01, key="ah_cgpa")
            backlogs = st.number_input("Active Backlogs", 0, 8, 0, key="ah_back")
            attendance = st.slider("Attendance %", 50.0, 100.0, 85.0, 0.5, key="ah_att")

        with col2:
            dsa = st.number_input("DSA Problems Solved", 0, 1000, 250, key="ah_dsa")
            leetcode = st.number_input("LeetCode Solved", 0, 700, 150, key="ah_lc")
            hackerrank = st.number_input("HackerRank Solved", 0, 500, 80, key="ah_hr")
            github = st.number_input("GitHub Repositories", 0, 50, 10, key="ah_gh")
            internships = st.number_input("Completed Internships", 0, 6, 1, key="ah_int")
            projects = st.number_input("Completed Projects", 0, 12, 3, key="ah_prj")

        with col3:
            hackathons = st.number_input("Hackathons Count", 0, 10, 1, key="ah_hk")
            certs = st.number_input("Certifications Count", 0, 10, 2, key="ah_cert")
            aptitude = st.slider("Aptitude Score", 30.0, 100.0, 75.0, 0.5, key="ah_apt")
            communication = st.slider("Communication Score", 1.0, 10.0, 7.0, 0.1, key="ah_comm")
            coding_skill = st.slider("Coding Skill Score", 1.0, 10.0, 7.5, 0.1, key="ah_code")
            mock_score = st.slider("Mock Interview Score", 1.0, 10.0, 7.5, 0.1, key="ah_mock")
            training = st.selectbox("Placement Training", TRAINING_OPTIONS, index=0, key="ah_train")

        ah_model = st.selectbox("Classifier", ["Random Forest", "Decision Tree", "Naive Bayes"], key="ah_model_sel")
        predict_btn = st.form_submit_button("🔮 Predict Placement Outcome", type="primary", use_container_width=True)

    if predict_btn:
        row_dict = {
            "branch": branch, "gender": gender, "age": age, "cgpa": cgpa,
            "backlogs": backlogs, "attendance_percentage": attendance,
            "dsa_questions_solved": dsa, "leetcode_questions_solved": leetcode,
            "hackerrank_questions_solved": hackerrank, "github_repos": github,
            "internships_count": internships, "projects_count": projects,
            "hackathons_count": hackathons, "certifications_count": certs,
            "aptitude_score": aptitude, "communication_score": communication,
            "coding_skill_score": coding_skill, "mock_interview_score": mock_score,
            "placement_training": training
        }

        res = predict_placement(row_dict, reference_df=df_ref, model_name=ah_model)
        is_placed = res["status"] == "Placed"
        card_class = "prediction-placed" if is_placed else "prediction-unplaced"
        status_color = "#34d399" if is_placed else "#fb7185"

        st.markdown(f"""
        <div class="prediction-card {card_class}">
            <div style="font-size: 1.1rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                EVALUATION RESULT
            </div>
            <div style="font-size: 3rem; font-weight: 900; color: {status_color}; margin: 6px 0;">
                {'✓' if is_placed else '⚠️'} {res['status'].upper()}
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #f8fafc;">
                Placement Confidence: <span style="color: {status_color};">{res['probability_percent']}%</span> ({res['model_name']})
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: BATCH CSV SCORING -----------------
with tab_batch:
    st.markdown("### 📁 High-Throughput Batch CSV Placement Scoring")
    st.caption("Upload candidate CSV file matching placement dataset columns to run bulk inference:")

    uploaded_file = st.file_uploader("Upload Student Candidates CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.markdown(f"**Loaded CSV:** {len(batch_df)} records.")
            
            # Validation
            missing_cols = [c for c in ["cgpa", "branch", "dsa_questions_solved"] if c not in batch_df.columns]
            if missing_cols:
                st.error(f"Validation Error: Uploaded CSV is missing critical columns: {missing_cols}")
            else:
                batch_model = st.selectbox("Model for Batch Inference", ["Random Forest", "Decision Tree", "Naive Bayes"], key="batch_m_sel")
                if st.button("🚀 Run Batch Prediction", type="primary"):
                    with st.spinner(f"Scoring {len(batch_df)} candidates through {batch_model}..."):
                        scored_df = batch_predict(batch_df, reference_df=df_ref, model_name=batch_model)
                        
                        st.markdown("#### Scored Batch Candidate Records")
                        st.dataframe(scored_df.head(50), use_container_width=True)

                        out_csv = scored_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📥 Download Scored Candidate Roster (CSV)",
                            data=out_csv,
                            file_name="scored_placement_candidates.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        except Exception as e:
            st.error(f"Error parsing uploaded CSV: {str(e)}")
