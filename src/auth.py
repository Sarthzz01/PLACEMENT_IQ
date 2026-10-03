import streamlit as st
from .database import authenticate_user, register_user, init_database
from .config import ADMIN_EMAILS

DEMO_ACCOUNTS = {
    "admin": {
        "email": "admin@college.com",
        "name": "Prof. K. Sharma (DWM Lead)",
        "role": "Admin",
        "id": "ADM-001"
    },
    "placement_officer": {
        "email": "placement@college.com",
        "name": "Dean D. Joshi (TPO)",
        "role": "Admin",
        "id": "ADM-002"
    },
    "student_1": {
        "email": "student@college.com",
        "name": "Rohan Verma",
        "role": "Student",
        "id": "STU-10492"
    },
    "student_2": {
        "email": "ananya.sen@campus.edu",
        "name": "Ananya Sen",
        "role": "Student",
        "id": "STU-10493"
    }
}

def init_auth_state():
    """Initialize session state variables for authentication."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = ""

def login_user(email: str, password: str = None, bypass_password: bool = False) -> tuple[bool, str]:
    """
    Log in the user, verifying password against SQLite database and determining role.
    Returns (success, message).
    """
    init_auth_state()
    clean_email = email.strip().lower()
    if not clean_email or "@" not in clean_email:
        return False, "Please enter a valid email address."

    user = authenticate_user(clean_email, password, bypass_password=bypass_password)
    if not user:
        return False, "Invalid email or password. Please verify your credentials."

    role = "Admin" if user["role"].lower() == "admin" else "Student"
    name = user["name"] or clean_email.split("@")[0].title()
    student_id = user["student_id"] or f"STU-{abs(hash(clean_email)) % 90000 + 10000}"

    st.session_state.authenticated = True
    st.session_state.user_email = clean_email
    st.session_state.user_role = role
    st.session_state.user_name = name
    st.session_state.user_id = student_id
    return True, f"Welcome back, {name}!"

def register_student_account(name: str, email: str, password: str, confirm_password: str, branch: str = "CSE", student_id: str = None) -> tuple[bool, str]:
    """
    Register a new student account securely.
    Public registration is strictly restricted to student role.
    """
    if password != confirm_password:
        return False, "Passwords do not match."
    success, msg, user = register_user(name, email, password, branch=branch, student_id=student_id)
    if success and user:
        login_user(email, password)
    return success, msg

def logout_user():
    """Clear user session state and sign out."""
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_role = None
    st.session_state.user_name = ""
    st.session_state.user_id = ""

def require_auth():
    """Ensure user is logged in before rendering a protected page."""
    init_auth_state()
    if not st.session_state.authenticated:
        st.warning("🔒 Authentication required. Please log in via the Login portal.")
        st.stop()

def require_admin():
    """Ensure user is logged in as an Administrator."""
    require_auth()
    if st.session_state.user_role != "Admin":
        st.error("⛔ Access Denied: Administrator privileges are required to view this page.")
        st.stop()

def require_student():
    """Ensure user is logged in as a Student."""
    require_auth()
    if st.session_state.user_role != "Student":
        st.error("⛔ Access Denied: This page is reserved for the Student portal.")
        st.stop()
