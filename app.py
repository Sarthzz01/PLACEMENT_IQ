import streamlit as st
from src.auth import init_auth_state, logout_user
from src.ui import css
from src.database import init_database

st.set_page_config(
    page_title="PLACEMENT IQ — Student Placement Analytics & Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global dark modern glassmorphism styling
css()
init_auth_state()
init_database()

# Define Public Landing & Authentication Pages
home_page = st.Page("pages/0_Home.py", title="Home", icon="🏠", default=True)
login_page = st.Page("pages/0_Login.py", title="Sign In & Register", icon="🔐")

# Student Workspace Pages
student_dashboard = st.Page("pages/1_Student_Dashboard.py", title="Placement Dashboard", icon="📊")
student_profile = st.Page("pages/2_Student_Profile.py", title="My Profile & Entry", icon="👤")
student_prediction = st.Page("pages/3_Placement_Prediction.py", title="Predict Placement", icon="🎯")
student_skills = st.Page("pages/4_Skill_Analysis.py", title="Skill Analysis", icon="🕸️")
student_plan = st.Page("pages/5_Improvement_Plan.py", title="Improvement Plan", icon="📈")
student_history = st.Page("pages/6_Prediction_History.py", title="Prediction History", icon="📜")

# Admin Workspace Pages
admin_overview = st.Page("pages/10_Admin_Dashboard.py", title="Executive Overview", icon="🛡️")
admin_student_data = st.Page("pages/11_Student_Data.py", title="Student Directory & Audit", icon="👥")
admin_warehouse = st.Page("pages/12_Data_Warehouse.py", title="Data Warehouse", icon="🏛️")
admin_olap = st.Page("pages/13_OLAP.py", title="OLAP Analytics", icon="🧊")
admin_mining = st.Page("pages/14_Data_Mining.py", title="Data Mining", icon="⛏️")
admin_classification = st.Page("pages/15_Classification.py", title="Classification Suite", icon="🎯")
admin_regression = st.Page("pages/16_Regression.py", title="Numerical Regression", icon="📈")
admin_kmeans = st.Page("pages/17_KMeans.py", title="K-Means Clustering", icon="🔮")
admin_agglomerative = st.Page("pages/18_Agglomerative.py", title="Agglomerative Clustering", icon="🌳")
admin_cluster_compare = st.Page("pages/19_Cluster_Comparison.py", title="Cluster Comparison", icon="⚖️")
admin_predictor = st.Page("pages/20_Admin_Predictor.py", title="Placement Predictor", icon="🚀")
admin_reports = st.Page("pages/21_Reports.py", title="Reports & Export", icon="📄")
admin_settings = st.Page("pages/22_Settings.py", title="System Settings", icon="⚙️")

# Common Logout Page
logout_page = st.Page("pages/99_Logout.py", title="Sign Out", icon="🚪")

# Sidebar Branding
with st.sidebar:
    st.markdown("### ✨ PLACEMENT IQ")
    st.caption("Student Placement Analytics & Intelligence • DWM Platform")
    st.markdown("---")
    
    if st.session_state.authenticated:
        role = st.session_state.user_role
        name = st.session_state.user_name
        email = st.session_state.user_email
        badge_style = "color:#38bdf8; background:rgba(6,182,212,0.15); border:1px solid rgba(56,189,248,0.3);" if role == "Student" else "color:#c084fc; background:rgba(139,92,246,0.18); border:1px solid rgba(192,132,252,0.35);"
        
        st.markdown(f"""
        <div style="padding: 14px; border-radius: 12px; {badge_style} margin-bottom: 12px;">
            <div style="font-weight: 700; font-size: 0.95rem;">{'🎓 Student Portal' if role == 'Student' else '🛡️ Admin Center'}</div>
            <div style="font-size: 0.88rem; margin-top: 4px; font-weight:600; color:#f8fafc;">{name}</div>
            <div style="font-size: 0.75rem; opacity: 0.85;">{email}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 12px; border-radius: 10px; background: rgba(37, 99, 235, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); margin-bottom: 12px; font-size: 0.82rem; color: #cbd5e1;">
            <b>Public Portal:</b> Explore platform capabilities or sign in with your student or administrative credentials.
        </div>
        """, unsafe_allow_html=True)

# Dynamic Role-Based Navigation Routing
if not st.session_state.authenticated:
    pg = st.navigation([home_page, login_page])
elif st.session_state.user_role == "Student":
    pg = st.navigation({
        "Student Workspace": [student_dashboard, student_profile, student_prediction, student_skills, student_plan, student_history],
        "Account": [logout_page]
    })
elif st.session_state.user_role == "Admin":
    pg = st.navigation({
        "Executive Analytics": [admin_overview, admin_student_data, admin_warehouse, admin_olap, admin_mining],
        "Machine Learning Suite": [admin_classification, admin_regression, admin_kmeans, admin_agglomerative, admin_cluster_compare],
        "Predictor & Exports": [admin_predictor, admin_reports, admin_settings],
        "Account": [logout_page]
    })
else:
    pg = st.navigation([home_page, login_page])

pg.run()
