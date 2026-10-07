import streamlit as st
import pandas as pd
from src.auth import require_student
from src.config import BASE_NUMERIC, BRANCH_OPTIONS, GENDER_OPTIONS, TRAINING_OPTIONS, NUMERIC_RANGES
from src.database import get_student_profile, save_student_profile, is_student_profile_completed
from src.submissions import smart_parse_links
from src.ui import css, hero, render_top_navbar, completion_gauge

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "My Profile",
    "Keep your placement profile up to date. These parameters map directly into our institutional Data Warehouse and power the AI placement prediction models.",
    tag="Candidate Profile Center"
)

# Load existing profile from SQLite database
p_data = get_student_profile(email) or {}
is_completed = is_student_profile_completed(email)

# Helper function to get values: if profile is completed, use saved data; otherwise use clean baseline defaults
def get_field_val(key, default_unfilled, val_type=float):
    if is_completed and p_data.get(key) is not None:
        try:
            return val_type(p_data[key])
        except (ValueError, TypeError):
            return default_unfilled
    return default_unfilled

# Profile Completeness Calculation
required_keys = [
    "cgpa", "attendance_percentage", "dsa_questions_solved", "leetcode_questions_solved",
    "internships_count", "projects_count", "aptitude_score", "coding_skill_score",
    "communication_score", "mock_interview_score"
]

if is_completed:
    filled = sum(1 for k in required_keys if p_data.get(k) is not None)
    comp_pct = int((filled / len(required_keys)) * 100)
    missing_fields = [k.replace('_', ' ').title() for k in required_keys if p_data.get(k) is None]
    completion_gauge(comp_pct, missing_fields if comp_pct < 100 else None)
else:
    comp_pct = 0
    completion_gauge(0, ["Academic CGPA & Attendance", "DSA & Coding Problems", "Internships & Projects", "Aptitude & Skills"])

tab_form, tab_links, tab_preview = st.tabs([
    "📋 1. Dataset Parameters Form",
    "🔗 2. Online Profile & Portfolio Links",
    "👁️ 3. Profile Summary & JSON Inspection"
])

# ----------------- TAB 1: DATASET PARAMETERS FORM -----------------
with tab_form:
    if not is_completed:
        st.info("👋 **Welcome to Profile Setup!** Please fill in your academic record, coding practice, and project experience below. Once saved, your actual data will power your placement analytics, AI predictions, and peer comparisons.")
    else:
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px; padding: 16px 20px;">
            <div style="font-weight: 700; color: #2563EB; font-size: 0.95rem; margin-bottom: 4px;">Verified Dataset Features</div>
            <div style="color: #64748B; font-size: 0.85rem;">
                All inputs are validated against verified bounds from <code>placement_prediction_cleaned.csv</code>. Your saved record persists automatically in SQLite.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.form("student_profile_form"):
        
        # 1. Personal Information Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>👤</span> Personal Information
            </div>
        """, unsafe_allow_html=True)
        c_a1, c_a2, c_a3 = st.columns(3)
        with c_a1:
            gender_idx = GENDER_OPTIONS.index(p_data.get("gender", "Male")) if (is_completed and p_data.get("gender") in GENDER_OPTIONS) else 0
            gender = st.selectbox("Gender", GENDER_OPTIONS, index=gender_idx)
        with c_a2:
            age = st.number_input(
                "Age (Years)",
                min_value=NUMERIC_RANGES["age"][0],
                max_value=NUMERIC_RANGES["age"][1],
                value=int(get_field_val("age", 21, int)),
                help="Standard undergraduate candidate age bracket: 18-32"
            )
        with c_a3:
            branch_idx = BRANCH_OPTIONS.index(p_data.get("branch", "CSE")) if (p_data.get("branch") in BRANCH_OPTIONS) else 0
            branch = st.selectbox("Engineering Department / Branch", BRANCH_OPTIONS, index=branch_idx)
        st.markdown("</div>", unsafe_allow_html=True)

        # 2. Academic Information Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🎓</span> Academic Information
            </div>
        """, unsafe_allow_html=True)
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            cgpa = st.slider(
                "Cumulative GPA (CGPA)",
                min_value=NUMERIC_RANGES["cgpa"][0],
                max_value=NUMERIC_RANGES["cgpa"][1],
                value=float(get_field_val("cgpa", 0.0, float)),
                step=0.01,
                help="University scale from 0.00 to 10.00"
            )
        with c_b2:
            backlogs = st.number_input(
                "Active Backlogs",
                min_value=NUMERIC_RANGES["backlogs"][0],
                max_value=NUMERIC_RANGES["backlogs"][1],
                value=int(get_field_val("backlogs", 0, int)),
                help="Pending active course backlogs"
            )
        with c_b3:
            attendance = st.slider(
                "Class Attendance Percentage (%)",
                min_value=NUMERIC_RANGES["attendance_percentage"][0],
                max_value=NUMERIC_RANGES["attendance_percentage"][1],
                value=float(get_field_val("attendance_percentage", 0.0, float)),
                step=0.5,
                help="Minimum 75% required by most campus placement policies"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Coding & Problem Solving Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>💻</span> Coding & Problem Solving
            </div>
        """, unsafe_allow_html=True)
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            dsa = st.number_input(
                "DSA Questions Solved",
                min_value=NUMERIC_RANGES["dsa_questions_solved"][0],
                max_value=NUMERIC_RANGES["dsa_questions_solved"][1],
                value=int(get_field_val("dsa_questions_solved", 0, int)),
                help="Total algorithmic challenges completed across all platforms"
            )
            hackerrank = st.number_input(
                "HackerRank Solved",
                min_value=NUMERIC_RANGES["hackerrank_questions_solved"][0],
                max_value=NUMERIC_RANGES["hackerrank_questions_solved"][1],
                value=int(get_field_val("hackerrank_questions_solved", 0, int)),
                help="HackerRank challenges and skill badges"
            )
        with c_c2:
            leetcode = st.number_input(
                "LeetCode Solved",
                min_value=NUMERIC_RANGES["leetcode_questions_solved"][0],
                max_value=NUMERIC_RANGES["leetcode_questions_solved"][1],
                value=int(get_field_val("leetcode_questions_solved", 0, int)),
                help="LeetCode problems completed"
            )
            github_repos = st.number_input(
                "GitHub Repositories",
                min_value=NUMERIC_RANGES["github_repos"][0],
                max_value=NUMERIC_RANGES["github_repos"][1],
                value=int(get_field_val("github_repos", 0, int)),
                help="Public open-source and course project repositories"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # 4. Projects & Experience Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>💼</span> Projects & Experience
            </div>
        """, unsafe_allow_html=True)
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            internships = st.number_input(
                "Completed Internships",
                min_value=NUMERIC_RANGES["internships_count"][0],
                max_value=NUMERIC_RANGES["internships_count"][1],
                value=int(get_field_val("internships_count", 0, int)),
                help="Verified software engineering or research internships"
            )
            hackathons = st.number_input(
                "Hackathons Participated",
                min_value=NUMERIC_RANGES["hackathons_count"][0],
                max_value=NUMERIC_RANGES["hackathons_count"][1],
                value=int(get_field_val("hackathons_count", 0, int)),
                help="Collegiate or national level 24-48h hackathons"
            )
        with c_d2:
            projects = st.number_input(
                "Completed Projects",
                min_value=NUMERIC_RANGES["projects_count"][0],
                max_value=NUMERIC_RANGES["projects_count"][1],
                value=int(get_field_val("projects_count", 0, int)),
                help="Full-stack, ML, or capstone hardware/software projects"
            )
            certs = st.number_input(
                "Certifications Count",
                min_value=NUMERIC_RANGES["certifications_count"][0],
                max_value=NUMERIC_RANGES["certifications_count"][1],
                value=int(get_field_val("certifications_count", 0, int)),
                help="Verified technical certifications (AWS, Coursera, Oracle, etc.)"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # 5. Skills & Competencies Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🎯</span> Skills, Aptitude & Communication
            </div>
        """, unsafe_allow_html=True)
        c_e1, c_e2 = st.columns(2)
        with c_e1:
            aptitude = st.slider(
                "Aptitude Score",
                min_value=NUMERIC_RANGES["aptitude_score"][0],
                max_value=NUMERIC_RANGES["aptitude_score"][1],
                value=float(get_field_val("aptitude_score", 0.0, float)),
                step=0.5,
                help="Standardized campus quantitative & logical test score"
            )
            coding_skill = st.slider(
                "Coding Skill (0-10)",
                min_value=NUMERIC_RANGES["coding_skill_score"][0],
                max_value=NUMERIC_RANGES["coding_skill_score"][1],
                value=float(get_field_val("coding_skill_score", 0.0, float)),
                step=0.1,
                help="Assessed technical coding fluency (0-10 scale)"
            )
        with c_e2:
            communication = st.slider(
                "Communication Score (0-10)",
                min_value=NUMERIC_RANGES["communication_score"][0],
                max_value=NUMERIC_RANGES["communication_score"][1],
                value=float(get_field_val("communication_score", 0.0, float)),
                step=0.1,
                help="Oral fluency and behavioral articulation (0-10 scale)"
            )
            mock_score = st.slider(
                "Mock Interview Score (0-10)",
                min_value=NUMERIC_RANGES["mock_interview_score"][0],
                max_value=NUMERIC_RANGES["mock_interview_score"][1],
                value=float(get_field_val("mock_interview_score", 0.0, float)),
                step=0.1,
                help="Faculty mentor interview score (0-10 scale)"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # 6. Placement Preparation Card
        st.markdown("""
        <div class="campus-card" style="margin-bottom: 16px;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>📚</span> Placement Preparation
            </div>
        """, unsafe_allow_html=True)
        training_idx = TRAINING_OPTIONS.index(p_data.get("placement_training", "No")) if (is_completed and p_data.get("placement_training") in TRAINING_OPTIONS) else 1
        training = st.selectbox(
            "Enrolled in Campus Placement Training",
            TRAINING_OPTIONS,
            index=training_idx,
            help="Registered in campus pre-placement preparation training"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        col_save_btn, col_pred_btn = st.columns([1, 1])
        with col_save_btn:
            save_clicked = st.form_submit_button("💾 Save Profile to Database", type="primary", use_container_width=True)
        with col_pred_btn:
            pred_clicked = st.form_submit_button("🔮 Save & Proceed to Prediction", use_container_width=True)

        if save_clicked or pred_clicked:
            updated_profile = {
                "name": name,
                "student_id": user_id,
                "email": email,
                "gender": gender,
                "age": int(age),
                "branch": branch,
                "cgpa": float(cgpa),
                "backlogs": int(backlogs),
                "attendance_percentage": float(attendance),
                "dsa_questions_solved": int(dsa),
                "leetcode_questions_solved": int(leetcode),
                "hackerrank_questions_solved": int(hackerrank),
                "github_repos": int(github_repos),
                "internships_count": int(internships),
                "projects_count": int(projects),
                "hackathons_count": int(hackathons),
                "certifications_count": int(certs),
                "aptitude_score": float(aptitude),
                "communication_score": float(communication),
                "coding_skill_score": float(coding_skill),
                "mock_interview_score": float(mock_score),
                "placement_training": training,
                "github_url": p_data.get("github_url", ""),
                "leetcode_url": p_data.get("leetcode_url", ""),
                "hackerrank_url": p_data.get("hackerrank_url", ""),
                "portfolio_url": p_data.get("portfolio_url", ""),
                "certifications_url": p_data.get("certifications_url", ""),
                "verification_status": p_data.get("verification_status", "Verified"),
                "admin_notes": p_data.get("admin_notes", ""),
                "is_completed": 1
            }

            save_student_profile(updated_profile)

            # Generate real-time prediction and log to student_predictions
            try:
                from src.prediction import predict_placement
                from src.database import log_prediction_to_db
                pred_res = predict_placement(updated_profile)
                log_prediction_to_db(
                    student_id=user_id,
                    email=email,
                    status=pred_res["status"],
                    prob=pred_res["probability"],
                    model_name=pred_res.get("model_name", "Random Forest"),
                    features=updated_profile,
                    evaluated_by="Student Profile Submission"
                )
            except Exception:
                pass

            st.success("✅ Profile parameters successfully saved to SQLite database!")
            
            if pred_clicked:
                st.switch_page("pages/3_Placement_Prediction.py")
            else:
                st.rerun()

# ----------------- TAB 2: OPTIONAL PORTFOLIO LINKS -----------------
with tab_links:
    st.markdown("""
    <div class="campus-card">
        <div style="font-weight: 700; font-size: 1.05rem; color: #2563EB; margin-bottom: 6px;">🔗 Connect External Coding Profiles & Portfolio</div>
        <p style="color: #64748B; font-size: 0.88rem; margin: 0;">
            Provide links to your public platforms. Our parser can estimate problem solve counts and public repository metrics to auto-fill your parameters.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_links_form"):
        l_col1, l_col2 = st.columns(2)
        with l_col1:
            in_gh = st.text_input("GitHub Profile URL", value=p_data.get("github_url", ""), placeholder="https://github.com/username")
            in_lc = st.text_input("LeetCode Profile URL", value=p_data.get("leetcode_url", ""), placeholder="https://leetcode.com/u/username")
            in_hr = st.text_input("HackerRank Profile URL", value=p_data.get("hackerrank_url", ""), placeholder="https://hackerrank.com/username")
        with l_col2:
            in_pf = st.text_input("Personal Portfolio / Website URL", value=p_data.get("portfolio_url", ""), placeholder="https://yourportfolio.dev")
            in_cert = st.text_input("Credly / Certification Credential URL", value=p_data.get("certifications_url", ""), placeholder="https://credly.com/users/username")

        save_links_btn = st.form_submit_button("🔗 Save & Auto-Parse Profile Links", type="primary", use_container_width=True)

        if save_links_btn:
            extracted = smart_parse_links(in_gh, in_lc, in_hr, in_pf, in_cert)
            
            # Merge with existing
            current = get_student_profile(email) or {}
            current["github_url"] = in_gh
            current["leetcode_url"] = in_lc
            current["hackerrank_url"] = in_hr
            current["portfolio_url"] = in_pf
            current["certifications_url"] = in_cert

            # Auto-suggest if extracted
            if extracted["leetcode_questions_solved"] > 0:
                current["leetcode_questions_solved"] = max(current.get("leetcode_questions_solved", 0), extracted["leetcode_questions_solved"])
            if extracted["github_repos"] > 0:
                current["github_repos"] = max(current.get("github_repos", 0), extracted["github_repos"])
            if extracted["dsa_questions_solved"] > 0:
                current["dsa_questions_solved"] = max(current.get("dsa_questions_solved", 0), extracted["dsa_questions_solved"])

            save_student_profile(current)
            st.success("✅ Profile URLs saved successfully!")
            if extracted["detected_profiles"]:
                st.info(f"⚡ Parsed Signals: {', '.join(extracted['detected_profiles'])}")
            st.rerun()

# ----------------- TAB 3: PROFILE SUMMARY & INSPECTION -----------------
with tab_preview:
    st.markdown("### 📋 Stored Candidate Profile Record")
    if is_completed and p_data and p_data.get("cgpa") is not None:
        disp_df = pd.DataFrame([{k: v for k, v in p_data.items() if k not in ["user_id"]}])
        st.dataframe(disp_df.T.rename(columns={0: "Value"}), use_container_width=True)
    else:
        st.info("ℹ️ No candidate profile stored yet. Please fill in the parameters in Tab 1 and click 'Save Profile to Database'.")
