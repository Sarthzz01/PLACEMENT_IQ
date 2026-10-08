import sqlite3
import hashlib
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from .config import DB_PATH, OUTPUT_DIR, ADMIN_EMAILS

# Salt for password hashing
SALT = b"dwm_placement_iq_secure_salt_2026"

def hash_password(password: str) -> str:
    """Hash password using PBKDF2 HMAC SHA-256 with fixed project salt."""
    if not password:
        return ""
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000)
    return key.hex()

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify provided password against stored PBKDF2 hash."""
    if not stored_hash or not provided_password:
        return False
    return stored_hash == hash_password(provided_password)

def get_db_connection():
    """Get a SQLite connection to the persistent database."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables and seed baseline accounts and student profiles."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_db_connection()
    c = conn.cursor()

    # 1. Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        branch TEXT,
        created_at TEXT,
        last_login TEXT
    )
    """)

    # 2. Student profiles table
    c.execute("""
    CREATE TABLE IF NOT EXISTS student_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        student_id TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        age INTEGER,
        gender TEXT DEFAULT 'Male',
        branch TEXT DEFAULT 'CSE',
        cgpa REAL,
        backlogs INTEGER,
        attendance_percentage REAL,
        dsa_questions_solved INTEGER,
        leetcode_questions_solved INTEGER,
        hackerrank_questions_solved INTEGER,
        internships_count INTEGER,
        projects_count INTEGER,
        hackathons_count INTEGER,
        certifications_count INTEGER,
        aptitude_score REAL,
        communication_score REAL,
        coding_skill_score REAL,
        mock_interview_score REAL,
        github_repos INTEGER,
        placement_training TEXT DEFAULT 'Yes',
        github_url TEXT DEFAULT '',
        leetcode_url TEXT DEFAULT '',
        hackerrank_url TEXT DEFAULT '',
        portfolio_url TEXT DEFAULT '',
        certifications_url TEXT DEFAULT '',
        verification_status TEXT DEFAULT 'Pending Review',
        admin_notes TEXT DEFAULT '',
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Ensure is_completed column exists if migrating an existing DB
    try:
        c.execute("ALTER TABLE student_profiles ADD COLUMN is_completed INTEGER DEFAULT 0")
    except Exception:
        pass

    # 3. Student predictions table
    c.execute("""
    CREATE TABLE IF NOT EXISTS student_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        student_id TEXT,
        email TEXT,
        predicted_status TEXT,
        probability REAL,
        model_name TEXT,
        features_snapshot TEXT,
        evaluated_by TEXT DEFAULT 'Student Self-Assessment',
        predicted_at TEXT
    )
    """)

    # 4. Admin feedback table
    c.execute("""
    CREATE TABLE IF NOT EXISTS admin_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        email TEXT,
        prediction TEXT,
        recommendation TEXT,
        priority TEXT DEFAULT 'Medium',
        admin_name TEXT,
        created_at TEXT
    )
    """)

    # 5. OLAP Query History table
    c.execute("""
    CREATE TABLE IF NOT EXISTS olap_query_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        operation TEXT,
        row_dims TEXT,
        col_dims TEXT,
        measure TEXT,
        agg_func TEXT,
        filters_json TEXT,
        result_rows INTEGER,
        executed_at TEXT
    )
    """)

    # 6. System settings table
    c.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # Default system settings
    c.execute("INSERT OR IGNORE INTO system_settings (key, value) VALUES ('production_model', 'Random Forest')")
    c.execute("INSERT OR IGNORE INTO system_settings (key, value) VALUES ('training_data_mode', 'Original Dataset')")

    # Seed Admin Users
    admin_seed = [
        ("ADM-001", "Prof. Shruti Agrawal", "admin@college.com", "admin123", "admin", "CSE"),
        ("ADM-002", "Dean D. Joshi (TPO)", "placement@college.com", "placement123", "admin", "IT"),
        ("ADM-003", "System Administrator", "admin@campus.edu", "admin123", "admin", "CSE"),
    ]
    for sid, sname, semail, spass, srole, sbranch in admin_seed:
        c.execute("SELECT id FROM users WHERE email = ?", (semail,))
        if not c.fetchone():
            c.execute("""
            INSERT INTO users (student_id, name, email, password_hash, role, branch, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sid, sname, semail, hash_password(spass), srole, sbranch, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Seed Student Users & Profiles
    students_seed = [
        {
            "student_id": "STU-10492", "name": "Rohan Verma", "email": "student@college.com", "password": "student123",
            "branch": "CSE", "gender": "Male", "age": 21, "cgpa": 8.74, "backlogs": 0, "attendance_percentage": 91.5,
            "dsa_questions_solved": 380, "leetcode_questions_solved": 260, "hackerrank_questions_solved": 120,
            "github_repos": 14, "internships_count": 2, "projects_count": 4, "hackathons_count": 2, "certifications_count": 3,
            "aptitude_score": 84.0, "communication_score": 8.5, "coding_skill_score": 8.8, "mock_interview_score": 8.5,
            "placement_training": "Yes", "github_url": "https://github.com/rohan-codes",
            "leetcode_url": "https://leetcode.com/u/rohan_dev", "hackerrank_url": "https://hackerrank.com/rohan_v",
            "portfolio_url": "https://rohan-portfolio.dev", "certifications_url": "https://credly.com/users/rohan-verma",
            "verification_status": "Verified", "admin_notes": "Strong GitHub project portfolio and high DSA count."
        },
        {
            "student_id": "STU-10493", "name": "Ananya Sen", "email": "ananya.sen@campus.edu", "password": "student123",
            "branch": "IT", "gender": "Female", "age": 21, "cgpa": 7.92, "backlogs": 0, "attendance_percentage": 84.0,
            "dsa_questions_solved": 190, "leetcode_questions_solved": 130, "hackerrank_questions_solved": 60,
            "github_repos": 9, "internships_count": 1, "projects_count": 3, "hackathons_count": 1, "certifications_count": 2,
            "aptitude_score": 72.5, "communication_score": 7.5, "coding_skill_score": 7.0, "mock_interview_score": 7.5,
            "placement_training": "Yes", "github_url": "https://github.com/ananya-sen",
            "leetcode_url": "https://leetcode.com/u/ananya_it", "hackerrank_url": "https://hackerrank.com/ananya_s",
            "portfolio_url": "https://ananya-sen.me", "certifications_url": "https://coursera.org/verify/specialization/ananya",
            "verification_status": "Verified", "admin_notes": "Solid coursework profile and active hackathon participation."
        },
        {
            "student_id": "STU-10494", "name": "Vikram Malhotra", "email": "vikram.m@campus.edu", "password": "student123",
            "branch": "Mechanical", "gender": "Male", "age": 22, "cgpa": 6.45, "backlogs": 1, "attendance_percentage": 68.0,
            "dsa_questions_solved": 45, "leetcode_questions_solved": 30, "hackerrank_questions_solved": 15,
            "github_repos": 3, "internships_count": 0, "projects_count": 1, "hackathons_count": 0, "certifications_count": 1,
            "aptitude_score": 52.0, "communication_score": 5.0, "coding_skill_score": 4.2, "mock_interview_score": 5.0,
            "placement_training": "No", "github_url": "https://github.com/vikram-mech",
            "leetcode_url": "https://leetcode.com/u/vikram_30", "hackerrank_url": "https://hackerrank.com/vikram_m",
            "portfolio_url": "", "certifications_url": "https://udemy.com/certificate/UC-10294",
            "verification_status": "Action Required", "admin_notes": "Needs attendance improvement and placement training registration."
        }
    ]

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for s in students_seed:
        c.execute("SELECT id FROM users WHERE email = ?", (s["email"],))
        user_row = c.fetchone()
        if not user_row:
            c.execute("""
            INSERT INTO users (student_id, name, email, password_hash, role, branch, created_at)
            VALUES (?, ?, ?, ?, 'student', ?, ?)
            """, (s["student_id"], s["name"], s["email"], hash_password(s["password"]), s["branch"], now_str))
            uid = c.lastrowid
        else:
            uid = user_row["id"]

        c.execute("SELECT id FROM student_profiles WHERE email = ?", (s["email"],))
        if not c.fetchone():
            c.execute("""
            INSERT INTO student_profiles (
                user_id, student_id, email, name, age, gender, branch, cgpa, backlogs, attendance_percentage,
                dsa_questions_solved, leetcode_questions_solved, hackerrank_questions_solved,
                internships_count, projects_count, hackathons_count, certifications_count,
                aptitude_score, communication_score, coding_skill_score, mock_interview_score,
                github_repos, placement_training, github_url, leetcode_url, hackerrank_url,
                portfolio_url, certifications_url, verification_status, admin_notes, is_completed, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (
                uid, s["student_id"], s["email"], s["name"], s["age"], s["gender"], s["branch"],
                s["cgpa"], s["backlogs"], s["attendance_percentage"], s["dsa_questions_solved"],
                s["leetcode_questions_solved"], s["hackerrank_questions_solved"], s["internships_count"],
                s["projects_count"], s["hackathons_count"], s["certifications_count"], s["aptitude_score"],
                s["communication_score"], s["coding_skill_score"], s["mock_interview_score"], s["github_repos"],
                s["placement_training"], s["github_url"], s["leetcode_url"], s["hackerrank_url"],
                s["portfolio_url"], s["certifications_url"], s["verification_status"], s["admin_notes"],
                now_str, now_str
            ))

    # Mark only seeded demo students as completed
    try:
        seed_emails = [s["email"] for s in students_seed]
        placeholders = ",".join(["?"] * len(seed_emails))
        c.execute(f"UPDATE student_profiles SET is_completed = 1 WHERE email IN ({placeholders})", seed_emails)
    except Exception:
        pass

    # Seed Initial Admin Feedback
    c.execute("SELECT COUNT(*) FROM admin_feedback")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO admin_feedback (student_id, email, prediction, recommendation, priority, admin_name, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "STU-10492", "student@college.com", "Placed",
            "Excellent technical aptitude and problem-solving readiness. Recommended for Day-1 High Package Product Drives.",
            "High", "Prof. Shruti Agrawal", now_str
        ))
        c.execute("""
        INSERT INTO admin_feedback (student_id, email, prediction, recommendation, priority, admin_name, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "STU-10494", "vikram.m@campus.edu", "Not Placed",
            "Urgent focus needed on clearing backlogs, raising class attendance above 75%, and attending the mandatory placement preparation bootcamps.",
            "High", "Dean D. Joshi (TPO)", now_str
        ))

    # Seed initial prediction history if empty
    c.execute("SELECT COUNT(*) FROM student_predictions")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO student_predictions (student_id, email, predicted_status, probability, model_name, features_snapshot, evaluated_by, predicted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "STU-10492", "student@college.com", "Placed", 0.942, "Random Forest", "{}", "Student Self-Assessment", "2026-09-28 14:30:00"
        ))
        c.execute("""
        INSERT INTO student_predictions (student_id, email, predicted_status, probability, model_name, features_snapshot, evaluated_by, predicted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "STU-10493", "ananya.sen@campus.edu", "Placed", 0.785, "Random Forest", "{}", "Student Self-Assessment", "2026-09-28 17:15:00"
        ))
        c.execute("""
        INSERT INTO student_predictions (student_id, email, predicted_status, probability, model_name, features_snapshot, evaluated_by, predicted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "STU-10494", "vikram.m@campus.edu", "Not Placed", 0.235, "Random Forest", "{}", "Admin Evaluation", "2026-09-29 10:45:00"
        ))

    conn.commit()
    conn.close()

# ---------------- USER AUTHENTICATION & MANAGEMENT ----------------

def authenticate_user(email: str, password: str = None, bypass_password: bool = False):
    """
    Authenticate user by email and password.
    Returns user dict or None.
    """
    init_database()
    clean_email = email.strip().lower()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE LOWER(email) = ?", (clean_email,))
    user = c.fetchone()
    
    if not user:
        # Check if email is in ADMIN_EMAILS
        admin_set = {e.strip().lower() for e in ADMIN_EMAILS}
        if clean_email in admin_set:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
            INSERT INTO users (student_id, name, email, password_hash, role, branch, created_at, last_login)
            VALUES (?, ?, ?, ?, 'admin', 'CSE', ?, ?)
            """, (f"ADM-{abs(hash(clean_email))%900+100}", "Administrator", clean_email, hash_password("admin123"), now_str, now_str))
            conn.commit()
            c.execute("SELECT * FROM users WHERE LOWER(email) = ?", (clean_email,))
            user = c.fetchone()
        else:
            conn.close()
            return None

    user_dict = dict(user)
    
    # Password verification
    if not bypass_password:
        if not verify_password(user_dict["password_hash"], password):
            conn.close()
            return None

    # Update last login
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("UPDATE users SET last_login = ? WHERE id = ?", (now_str, user_dict["id"]))
    conn.commit()
    conn.close()
    return user_dict

def register_user(name: str, email: str, password: str, branch: str = "CSE", student_id: str = None):
    """
    Register a new student account.
    Enforces role='student' (never allows self-registration as admin).
    Returns (success: bool, message: str, user_dict: dict).
    """
    init_database()
    clean_email = email.strip().lower()
    if not clean_email or "@" not in clean_email:
        return False, "Please provide a valid email address.", None
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters.", None
    if not name or len(name.strip()) < 2:
        return False, "Please enter your full name.", None

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE LOWER(email) = ?", (clean_email,))
    if c.fetchone():
        conn.close()
        return False, "An account with this email address already exists. Please log in.", None

    if not student_id:
        student_id = f"STU-{abs(hash(clean_email)) % 90000 + 10000}"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p_hash = hash_password(password)

    # Public registration is strictly student role
    role = "student"
    c.execute("""
    INSERT INTO users (student_id, name, email, password_hash, role, branch, created_at, last_login)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_id, name.strip(), clean_email, p_hash, role, branch, now_str, now_str))
    uid = c.lastrowid

    # Create empty baseline profile with is_completed = 0 and NULL features
    c.execute("""
    INSERT INTO student_profiles (
        user_id, student_id, email, name, branch, is_completed,
        cgpa, backlogs, attendance_percentage, dsa_questions_solved, leetcode_questions_solved,
        hackerrank_questions_solved, internships_count, projects_count, hackathons_count,
        certifications_count, aptitude_score, communication_score, coding_skill_score,
        mock_interview_score, github_repos, created_at, updated_at
    ) VALUES (
        ?, ?, ?, ?, ?, 0,
        NULL, NULL, NULL, NULL, NULL,
        NULL, NULL, NULL, NULL,
        NULL, NULL, NULL, NULL,
        NULL, NULL, ?, ?
    )
    """, (uid, student_id, clean_email, name.strip(), branch, now_str, now_str))

    conn.commit()
    c.execute("SELECT * FROM users WHERE id = ?", (uid,))
    new_user = dict(c.fetchone())
    conn.close()
    return True, "Account registered successfully!", new_user

# ---------------- STUDENT PROFILES ----------------

def get_student_profile(email_or_id: str):
    """Retrieve full student profile dict by email or student_id."""
    init_database()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    SELECT * FROM student_profiles 
    WHERE LOWER(email) = ? OR LOWER(student_id) = ?
    ORDER BY id DESC LIMIT 1
    """, (email_or_id.strip().lower(), email_or_id.strip().lower()))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def is_student_profile_completed(email_or_id: str) -> bool:
    """
    Check if a student has actively filled and submitted their profile details.
    Returns False for newly registered users who have not yet entered their details.
    """
    p = get_student_profile(email_or_id)
    if not p:
        return False
    is_comp = p.get("is_completed", 0)
    return bool(is_comp) and (p.get("cgpa") is not None)

def save_student_profile(p: dict):
    """Insert or update student profile in SQLite database."""
    init_database()
    conn = get_db_connection()
    c = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email = p.get("email", "").strip().lower()
    student_id = p.get("student_id", f"STU-{abs(hash(email))%90000+10000}")
    name = p.get("name", "Student")

    # When saving profile, mark is_completed = 1 if academic data is present
    p.setdefault("is_completed", 1)

    c.execute("SELECT id FROM student_profiles WHERE LOWER(email) = ?", (email,))
    existing = c.fetchone()

    fields = [
        "name", "age", "gender", "branch", "cgpa", "backlogs", "attendance_percentage",
        "dsa_questions_solved", "leetcode_questions_solved", "hackerrank_questions_solved",
        "internships_count", "projects_count", "hackathons_count", "certifications_count",
        "aptitude_score", "communication_score", "coding_skill_score", "mock_interview_score",
        "github_repos", "placement_training", "github_url", "leetcode_url", "hackerrank_url",
        "portfolio_url", "certifications_url", "verification_status", "admin_notes", "is_completed"
    ]

    values = [p.get(f) for f in fields]

    if existing:
        set_clause = ", ".join([f"{f} = ?" for f in fields]) + ", updated_at = ?"
        c.execute(f"UPDATE student_profiles SET {set_clause} WHERE id = ?", values + [now_str, existing["id"]])
    else:
        cols = ["student_id", "email", "created_at", "updated_at"] + fields
        placeholders = ", ".join(["?"] * len(cols))
        c.execute(f"INSERT INTO student_profiles ({', '.join(cols)}) VALUES ({placeholders})", [student_id, email, now_str, now_str] + values)

    conn.commit()
    conn.close()
    return student_id

def get_all_student_profiles_df():
    """Retrieve all student profiles from SQLite database as a pandas DataFrame."""
    init_database()
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM student_profiles ORDER BY id DESC", conn)
    finally:
        conn.close()
    return df

# ---------------- PREDICTIONS & AUDIT LOGS ----------------

def log_prediction_to_db(student_id: str, email: str, status: str, prob: float, model_name: str, features: dict = None, evaluated_by: str = "Student Self-Assessment"):
    """Record a prediction run in SQLite."""
    init_database()
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feat_json = json.dumps(features) if features else "{}"
    conn.execute("""
    INSERT INTO student_predictions (student_id, email, predicted_status, probability, model_name, features_snapshot, evaluated_by, predicted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_id, email, status, prob, model_name, feat_json, evaluated_by, now_str))
    conn.commit()
    conn.close()

def get_student_prediction_history(email: str = None):
    """Fetch prediction history for a given student or all students."""
    init_database()
    conn = get_db_connection()
    try:
        if email:
            df = pd.read_sql_query("""
            SELECT * FROM student_predictions 
            WHERE LOWER(email) = ? 
            ORDER BY id DESC
            """, conn, params=(email.strip().lower(),))
        else:
            df = pd.read_sql_query("SELECT * FROM student_predictions ORDER BY id DESC", conn)
    finally:
        conn.close()
    return df

# ---------------- ADMIN FEEDBACK ----------------

def save_admin_feedback(student_id: str, email: str, prediction: str, recommendation: str, priority: str = "Medium", admin_name: str = "Admin"):
    """Record admin assessment & actionable recommendations for a student."""
    init_database()
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
    INSERT INTO admin_feedback (student_id, email, prediction, recommendation, priority, admin_name, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_id, email, prediction, recommendation, priority, admin_name, now_str))
    conn.commit()
    conn.close()

def get_student_feedback(email: str):
    """Retrieve all admin feedback records for a specific student."""
    init_database()
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("""
        SELECT * FROM admin_feedback 
        WHERE LOWER(email) = ? 
        ORDER BY id DESC
        """, conn, params=(email.strip().lower(),))
    finally:
        conn.close()
    return df

# ---------------- OLAP QUERY LOGGING ----------------

def log_olap_query(user_email: str, operation: str, row_dims: list, col_dims: list, measure: str, agg_func: str, filters: dict, result_rows: int):
    """Record an OLAP execution for query audit and quick rerun."""
    init_database()
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
    INSERT INTO olap_query_history (user_email, operation, row_dims, col_dims, measure, agg_func, filters_json, result_rows, executed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_email,
        operation,
        ", ".join(row_dims) if row_dims else "None",
        ", ".join(col_dims) if col_dims else "None",
        measure,
        agg_func,
        json.dumps(filters),
        result_rows,
        now_str
    ))
    conn.commit()
    conn.close()

def get_olap_history(limit: int = 25):
    """Retrieve recent OLAP queries."""
    init_database()
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(f"SELECT * FROM olap_query_history ORDER BY id DESC LIMIT {limit}", conn)
    finally:
        conn.close()
    return df

# ---------------- SYSTEM SETTINGS ----------------

def get_system_setting(key: str, default: str = ""):
    """Retrieve a persistent system configuration setting."""
    init_database()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM system_settings WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    return row["value"] if row else default

def set_system_setting(key: str, value: str):
    """Save a persistent system configuration setting."""
    init_database()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()
