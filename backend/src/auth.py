from .database import authenticate_user, register_user, init_database
from .config import ADMIN_EMAILS

DEMO_ACCOUNTS = {
    "admin": {
        "email": "admin@college.com",
        "name": "Prof. Shruti Agrawal (DWM Prof)",
        "role": "Admin",
        "id": "ADM-001"
    },
    "placement_officer": {
        "email": "placement@college.com",
        "name": "Dr. Sanchita Banerjee (TPO)",
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

# In-memory session state for Python runtime / scripts
_SESSION = {
    "authenticated": False,
    "user_email": "",
    "user_role": None,
    "user_name": "",
    "user_id": ""
}

def init_auth_state():
    """Initialize session state variables for authentication."""
    return dict(_SESSION)

def login_user(email: str, password: str = None, bypass_password: bool = False) -> tuple[bool, str]:
    """
    Log in the user, verifying password against SQLite database and determining role.
    Returns (success, message).
    """
    clean_email = email.strip().lower()
    if not clean_email or "@" not in clean_email:
        return False, "Please enter a valid email address."

    user = authenticate_user(clean_email, password, bypass_password=bypass_password)
    if not user:
        return False, "Invalid email or password. Please verify your credentials."

    role = "Admin" if user["role"].lower() == "admin" else "Student"
    name = user["name"] or clean_email.split("@")[0].title()
    student_id = user.get("student_id") or f"STU-{abs(hash(clean_email)) % 90000 + 10000}"

    _SESSION["authenticated"] = True
    _SESSION["user_email"] = clean_email
    _SESSION["user_role"] = role
    _SESSION["user_name"] = name
    _SESSION["user_id"] = student_id
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
    _SESSION["authenticated"] = False
    _SESSION["user_email"] = ""
    _SESSION["user_role"] = None
    _SESSION["user_name"] = ""
    _SESSION["user_id"] = ""

def get_current_user():
    """Return currently active session."""
    return dict(_SESSION)
