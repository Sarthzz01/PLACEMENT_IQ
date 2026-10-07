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
home_page = st.Page("pages/0_Home.py", title="Home", icon=":material/home:", default=True)
login_page = st.Page("pages/0_Login.py", title="Sign In & Register", icon=":material/login:")

# Student Workspace Pages
student_dashboard = st.Page("pages/1_Student_Dashboard.py", title="Dashboard", icon=":material/dashboard:")
student_profile = st.Page("pages/2_Student_Profile.py", title="Profile", icon=":material/person:")
student_prediction = st.Page("pages/3_Placement_Prediction.py", title="Placement Prediction", icon=":material/track_changes:")
student_skills = st.Page("pages/4_Skill_Analysis.py", title="Skill Analysis", icon=":material/radar:")
student_plan = st.Page("pages/5_Improvement_Plan.py", title="Improvement Plan", icon=":material/trending_up:")
student_history = st.Page("pages/6_Prediction_History.py", title="Prediction History", icon=":material/history:")

# Admin Workspace Pages
admin_overview = st.Page("pages/10_Admin_Dashboard.py", title="Dashboard", icon=":material/dashboard:")
admin_student_data = st.Page("pages/11_Student_Data.py", title="Students", icon=":material/group:")
admin_warehouse = st.Page("pages/12_Data_Warehouse.py", title="Data Warehouse", icon=":material/database:")
admin_olap = st.Page("pages/13_OLAP.py", title="OLAP Analytics", icon=":material/layers:")
admin_mining = st.Page("pages/14_Data_Mining.py", title="Data Mining", icon=":material/analytics:")
admin_classification = st.Page("pages/15_Classification.py", title="Classification", icon=":material/account_tree:")
admin_regression = st.Page("pages/16_Regression.py", title="Regression", icon=":material/trending_up:")
admin_kmeans = st.Page("pages/17_KMeans.py", title="K-Means", icon=":material/scatter_plot:")
admin_agglomerative = st.Page("pages/18_Agglomerative.py", title="Agglomerative", icon=":material/hub:")
admin_cluster_compare = st.Page("pages/19_Cluster_Comparison.py", title="Cluster Comparison", icon=":material/compare_arrows:")
admin_predictor = st.Page("pages/20_Admin_Predictor.py", title="Prediction Center", icon=":material/psychology:")
admin_reports = st.Page("pages/21_Reports.py", title="Reports", icon=":material/description:")
admin_settings = st.Page("pages/22_Settings.py", title="Settings", icon=":material/settings:")

# Common Logout Page
logout_page = st.Page("pages/99_Logout.py", title="Logout", icon=":material/logout:")

# Sidebar Branding
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 10px 4px 14px 4px;">
        <div style="width: 36px; height: 36px; border-radius: 8px; background: #2563EB; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-weight: 900; font-size: 1.05rem; box-shadow: 0 4px 12px rgba(37,99,235,0.4);">
            IQ
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.12rem; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.2;">PLACEMENT IQ</div>
            <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 500; letter-spacing: 0.02em;">CAMPUS PLATFORM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.authenticated:
        role = st.session_state.user_role
        name = st.session_state.user_name
        email = st.session_state.user_email
        role_tag = "Student Account" if role == "Student" else "Administrator"
        
        st.markdown(f"""
        <div style="padding: 12px 14px; border-radius: 10px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 12px;">
            <div style="font-size: 0.7rem; color: #60A5FA; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">{role_tag}</div>
            <div style="font-size: 0.9rem; margin-top: 2px; font-weight: 700; color: #FFFFFF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{name}</div>
            <div style="font-size: 0.74rem; color: #94A3B8; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{email}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 12px 14px; border-radius: 10px; background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.2); margin-bottom: 12px; font-size: 0.8rem; color: #CBD5E1; line-height: 1.5;">
            <b style="color: #60A5FA;">Campus Portal:</b> Sign in to access your placement intelligence and analytics suite.
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
