import streamlit as st
import pandas as pd
from src.auth import require_admin
from src.database import (
    get_all_student_profiles_df, get_student_prediction_history,
    save_student_profile, save_admin_feedback, log_prediction_to_db
)
from src.prediction import predict_placement, get_production_model_name
from src.preprocessing import load_data
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Student Directory & Candidate Management",
    "Inspect registered student profiles from SQLite database, evaluate candidate feature vectors, record official faculty feedback, and export candidate rosters.",
    tag="Candidate Management"
)

# Fetch all student profiles from SQLite database
profiles_df = get_all_student_profiles_df()
history_df = get_student_prediction_history()

total_students = len(profiles_df)
verified_count = len(profiles_df[profiles_df["verification_status"] == "Verified"]) if "verification_status" in profiles_df.columns else 0
pending_count = len(profiles_df[profiles_df["verification_status"] == "Pending Review"]) if "verification_status" in profiles_df.columns else 0
action_count = total_students - verified_count - pending_count

# KPI Strip
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Candidates", f"{total_students}", "Stored in SQLite")
with m2:
    st.metric("Verified Profiles", f"{verified_count}", "Audit Approved")
with m3:
    st.metric("Pending Review", f"{pending_count}", "Awaiting Verification")
with m4:
    st.metric("Action Required", f"{action_count}", "Follow-up Needed")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ----------------- SEARCH, FILTER & SORT CONTROLS -----------------
col_search, col_branch, col_status = st.columns([2, 1, 1])
with col_search:
    search_q = st.text_input("🔍 Search Candidates", placeholder="Search by name, student ID, or email...")
with col_branch:
    branch_filter = st.selectbox("Filter Branch", ["All Branches"] + sorted(profiles_df["branch"].dropna().unique().tolist()) if len(profiles_df) > 0 else ["All Branches"])
with col_status:
    status_filter = st.selectbox("Verification Status", ["All Statuses", "Verified", "Pending Review", "Action Required"])

filtered_df = profiles_df.copy()

if search_q:
    q = search_q.lower()
    filtered_df = filtered_df[
        filtered_df["name"].astype(str).str.lower().str.contains(q, na=False) |
        filtered_df["email"].astype(str).str.lower().str.contains(q, na=False) |
        filtered_df["student_id"].astype(str).str.lower().str.contains(q, na=False)
    ]

if branch_filter != "All Branches":
    filtered_df = filtered_df[filtered_df["branch"] == branch_filter]

if status_filter != "All Statuses" and "verification_status" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["verification_status"] == status_filter]

# Add latest prediction info to roster table
enhanced_rows = []
for _, r in filtered_df.iterrows():
    stu_email = r["email"]
    stu_hist = history_df[history_df["email"].str.lower() == stu_email.lower()] if len(history_df) > 0 else pd.DataFrame()
    if len(stu_hist) > 0:
        latest_pred = stu_hist.iloc[0]["predicted_status"]
        latest_prob = f"{float(stu_hist.iloc[0]['probability']) * 100:.1f}%"
    else:
        latest_pred = "Unassessed"
        latest_prob = "N/A"
        
    enhanced_rows.append({
        "Student ID": r["student_id"],
        "Name": r["name"],
        "Email": r["email"],
        "Branch": r["branch"],
        "CGPA": f"{float(r.get('cgpa', 0)):.2f}",
        "Prediction": latest_pred,
        "Probability": latest_prob,
        "Profile Status": r.get("verification_status", "Verified"),
        "Last Updated": r.get("updated_at", r.get("created_at", "N/A"))
    })

roster_df = pd.DataFrame(enhanced_rows)

st.markdown(f"### 📋 Candidate Directory Roster ({len(roster_df)} students)")
st.dataframe(roster_df, use_container_width=True)

# Export CSV
csv_bytes = roster_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Export Student Directory (CSV)",
    data=csv_bytes,
    file_name="student_directory_roster.csv",
    mime="text/csv"
)

st.markdown("---")

# ----------------- CANDIDATE INSPECTION, PREDICTION & FEEDBACK DRAWER -----------------
st.markdown("### 🔬 Candidate Detail, Live Prediction & Feedback")

if len(filtered_df) > 0:
    sel_student_id = st.selectbox(
        "Select Student Candidate",
        filtered_df["student_id"].tolist(),
        format_func=lambda s: f"{s} — {filtered_df[filtered_df['student_id']==s].iloc[0]['name']} ({filtered_df[filtered_df['student_id']==s].iloc[0]['email']})"
    )

    sel_student = filtered_df[filtered_df["student_id"] == sel_student_id].iloc[0].to_dict()

    col_prof_view, col_action_view = st.columns([1.5, 1.5], gap="large")

    with col_prof_view:
        st.markdown(f"""
        <div class="campus-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <h4 style="margin:0; color:#2563EB;">Candidate Profile: {sel_student.get('name')}</h4>
                <span class="badge-pill badge-info">{sel_student.get('student_id')}</span>
            </div>
            <div style="font-size:0.9rem; color:#475569; line-height: 1.8;">
                <b>Email:</b> <code>{sel_student.get('email')}</code> &bull; <b>Branch:</b> {sel_student.get('branch')}<br>
                <b>CGPA:</b> {float(sel_student.get('cgpa', 0)):.2f} &bull; <b>Backlogs:</b> {sel_student.get('backlogs', 0)} &bull; <b>Attendance:</b> {float(sel_student.get('attendance_percentage', 0)):.1f}%<br>
                <b>DSA Problems:</b> {sel_student.get('dsa_questions_solved', 0)} &bull; <b>LeetCode:</b> {sel_student.get('leetcode_questions_solved', 0)}<br>
                <b>Internships:</b> {sel_student.get('internships_count', 0)} &bull; <b>Projects:</b> {sel_student.get('projects_count', 0)}<br>
                <b>Aptitude:</b> {float(sel_student.get('aptitude_score', 0)):.1f} &bull; <b>Coding Score:</b> {float(sel_student.get('coding_skill_score', 0)):.1f} / 10<br>
                <b>Placement Training:</b> {sel_student.get('placement_training', 'Yes')}<br>
                <b>External Links:</b> 
                <a href="{sel_student.get('github_url', '#')}" target="_blank" style="color:#2563EB;">GitHub</a> &bull; 
                <a href="{sel_student.get('leetcode_url', '#')}" target="_blank" style="color:#2563EB;">LeetCode</a> &bull;
                <a href="{sel_student.get('portfolio_url', '#')}" target="_blank" style="color:#16A34A;">Portfolio</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_action_view:
        st.markdown("#### 🎯 Run Live Prediction for this Candidate")
        model_choice = st.selectbox("Choose Classification Model", ["Random Forest", "Decision Tree", "Naive Bayes"], index=0)
        
        if st.button("🚀 Evaluate Candidate Likelihood", type="primary", use_container_width=True):
            df_ref = load_data()
            eval_res = predict_placement(sel_student, reference_df=df_ref, model_name=model_choice)
            st.session_state.admin_selected_eval = eval_res
            
            # Log evaluation
            log_prediction_to_db(
                student_id=sel_student.get("student_id"),
                email=sel_student.get("email"),
                status=eval_res["status"],
                prob=eval_res["probability"],
                model_name=eval_res["model_name"],
                features=sel_student,
                evaluated_by=f"Admin: {name}"
            )

        if "admin_selected_eval" in st.session_state:
            res = st.session_state.admin_selected_eval
            status_color = "#16A34A" if res["status"] == "Placed" else "#DC2626"
            card_bg = "#F0FDF4" if res["status"] == "Placed" else "#FEF2F2"
            card_border = "#86EFAC" if res["status"] == "Placed" else "#FECACA"
            st.markdown(f"""
            <div style="background: {card_bg}; border: 1.5px solid {card_border}; border-radius: 12px; padding: 14px; margin: 10px 0; text-align: center;">
                <div style="font-size: 1.3rem; font-weight: 800; color: {status_color};">
                    {'✓' if res['status']=='Placed' else '⚠️'} {res['status'].upper()} ({res['probability_percent']}%)
                </div>
                <div style="font-size: 0.8rem; color: #64748B;">Evaluated with {res['model_name']} &bull; Stored in SQLite</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### ✍️ Add Official Feedback & Recommendations")
        with st.form("admin_feedback_form"):
            fb_prediction = st.selectbox("Assessment Verdict", ["Placed", "Not Placed", "High Potential", "At Risk"], index=0)
            fb_priority = st.selectbox("Priority Level", ["High", "Medium", "Low"], index=1)
            fb_recommendation = st.text_area(
                "Actionable Faculty Recommendation",
                placeholder="e.g. Focus on clearing active backlogs and attend DSA algorithmic workshops..."
            )
            submit_fb = st.form_submit_button("💾 Save Feedback to Student Dashboard", type="primary", use_container_width=True)

            if submit_fb:
                if not fb_recommendation:
                    st.error("Please enter a recommendation message.")
                else:
                    save_admin_feedback(
                        student_id=sel_student.get("student_id"),
                        email=sel_student.get("email"),
                        prediction=fb_prediction,
                        recommendation=fb_recommendation.strip(),
                        priority=fb_priority,
                        admin_name=name
                    )
                    st.success("✅ Feedback saved! It will immediately appear on the student's dashboard.")
                    st.rerun()
