import streamlit as st
from src.auth import init_auth_state, login_user, register_student_account, DEMO_ACCOUNTS, ADMIN_EMAILS
from src.config import BRANCH_OPTIONS
from src.ui import css, hero

css()
init_auth_state()

# If already authenticated, redirect immediately
if st.session_state.authenticated:
    if st.session_state.user_role == "Admin":
        st.switch_page("pages/10_Admin_Dashboard.py")
    else:
        st.switch_page("pages/1_Student_Dashboard.py")

hero(
    "Authentication & Registration Portal",
    "Single institutional access point for students and administrators. Roles and privileges are automatically resolved by the database.",
    tag="Secure Access"
)

col_center = st.columns([1, 2.2, 1])[1]

with col_center:
    # Determine default tab if directed from CTA button
    active_tab = getattr(st.session_state, "active_auth_tab", "login")
    
    tab_login, tab_signup = st.tabs([
        "🔐 Sign In to Placement IQ",
        "✨ Create New Student Account"
    ])

    # ----------------- TAB 1: SIGN IN -----------------
    with tab_login:
        st.markdown("""
        <div class="campus-card" style="border-top: 3px solid #2563EB; margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="margin:0; color:#0F172A; font-size:1.1rem;">🔐 Unified Account Login</h4>
                <span class="badge-pill badge-info">Role Auto-Detection</span>
            </div>
            <p style="color:#64748B; font-size:0.85rem; margin:0;">
                Enter your credentials to load your <b>Student Workspace</b> or <b>Administrator Center</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("common_login_form"):
            login_email = st.text_input("Institutional Email Address", placeholder="e.g. student@college.com or admin@college.com", key="auth_email_in")
            login_pass = st.text_input("Password", type="password", placeholder="Enter your account password", key="auth_pass_in")
            submitted = st.form_submit_button("🚀 Sign In to Placement IQ", use_container_width=True, type="primary")

            if submitted:
                if not login_email or "@" not in login_email:
                    st.error("Please enter a valid institutional email address.")
                elif not login_pass:
                    st.error("Please enter your account password.")
                else:
                    success, msg = login_user(login_email, login_pass)
                    if success:
                        st.success(f"{msg} Redirecting to your {st.session_state.user_role} portal...")
                        st.rerun()
                    else:
                        st.error(msg)

    # ----------------- TAB 2: SIGN UP / REGISTRATION -----------------
    with tab_signup:
        st.markdown("""
        <div class="campus-card" style="border-top: 3px solid #16A34A; margin-bottom: 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="margin:0; color:#0F172A; font-size:1.1rem;">🎓 New Student Registration</h4>
                <span class="badge-pill badge-success">Student Account</span>
            </div>
            <p style="color:#64748B; font-size:0.85rem; margin:0;">
                Create a candidate profile to evaluate placement readiness and receive personalized recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("student_signup_form"):
            reg_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            reg_email = st.text_input("Institutional Email Address", placeholder="e.g. rahul.sharma@college.com")
            
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                reg_branch = st.selectbox("Engineering Branch", BRANCH_OPTIONS, index=0)
            with c_s2:
                reg_stu_id = st.text_input("Student ID / Roll No. (Optional)", placeholder="e.g. STU-2026-451")

            c_p1, c_p2 = st.columns(2)
            with c_p1:
                reg_pass = st.text_input("Password", type="password", placeholder="At least 4 characters")
            with c_p2:
                reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

            st.caption("🔒 Public registration automatically provisions a **Student Account**. Administrator accounts require authorized institutional provisioning.")

            reg_submit = st.form_submit_button("✨ Register & Enter Student Workspace", use_container_width=True, type="primary")

            if reg_submit:
                if not reg_name or len(reg_name.strip()) < 2:
                    st.error("Please enter your full name.")
                elif not reg_email or "@" not in reg_email:
                    st.error("Please enter a valid email address.")
                elif not reg_pass or len(reg_pass) < 4:
                    st.error("Password must be at least 4 characters.")
                elif reg_pass != reg_confirm:
                    st.error("Passwords do not match. Please re-enter carefully.")
                else:
                    success, msg = register_student_account(
                        name=reg_name,
                        email=reg_email,
                        password=reg_pass,
                        confirm_password=reg_confirm,
                        branch=reg_branch,
                        student_id=reg_stu_id.strip() if reg_stu_id else None
                    )
                    if success:
                        st.success("Account created successfully! Redirecting to your Student Dashboard...")
                        st.rerun()
                    else:
                        st.error(msg)
