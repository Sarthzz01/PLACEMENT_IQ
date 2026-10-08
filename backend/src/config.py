from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "placement_prediction_cleaned.csv"
MODEL_DIR = ROOT / "models"
OUTPUT_DIR = ROOT / "outputs"
DB_PATH = OUTPUT_DIR / "placement_dw.sqlite"
SUBMISSIONS_FILE = OUTPUT_DIR / "student_submissions.csv"

# Target & Primary Keys
TARGET = "placement_prediction"
ID_COL = "student_id"

# Configurable Administrator Accounts
# Users logging in with these emails automatically receive the Admin role
ADMIN_EMAILS = [
    "admin@college.com",
    "placement@college.com",
    "admin@campus.edu",
    "shruti.agrawal@college.com",
    "tpo@college.edu",
    "dean.placement@college.edu"
]

# Feature labels for rich UI rendering
DISPLAY_NAMES = {
    "cgpa": "CGPA",
    "backlogs": "Active Backlogs",
    "attendance_percentage": "Attendance %",
    "dsa_questions_solved": "DSA Questions",
    "leetcode_questions_solved": "LeetCode Questions",
    "hackerrank_questions_solved": "HackerRank Questions",
    "internships_count": "Internships Completed",
    "projects_count": "Projects Completed",
    "hackathons_count": "Hackathons Participated",
    "certifications_count": "Certifications Earned",
    "aptitude_score": "Aptitude Score",
    "communication_score": "Communication Score",
    "coding_skill_score": "Coding Skill Score",
    "github_repos": "GitHub Repositories",
    "mock_interview_score": "Mock Interview Score",
    "placement_prediction": "Placement Prediction",
    "age": "Age",
    "gender": "Gender",
    "branch": "Branch",
    "placement_training": "Placement Training",
    "placement_status": "Placement Status"
}

# Base numeric features from placement_prediction_cleaned.csv
BASE_NUMERIC = [
    "age",
    "cgpa",
    "backlogs",
    "attendance_percentage",
    "dsa_questions_solved",
    "leetcode_questions_solved",
    "hackerrank_questions_solved",
    "internships_count",
    "projects_count",
    "hackathons_count",
    "certifications_count",
    "aptitude_score",
    "communication_score",
    "coding_skill_score",
    "github_repos",
    "mock_interview_score"
]

# Numerical candidate targets for Regression analysis
REGRESSION_TARGETS = [
    "aptitude_score",
    "coding_skill_score",
    "cgpa",
    "mock_interview_score"
]

# Default feature selection for clustering algorithms
CLUSTER_DEFAULTS = [
    "cgpa",
    "backlogs",
    "attendance_percentage",
    "dsa_questions_solved",
    "leetcode_questions_solved",
    "hackerrank_questions_solved",
    "internships_count",
    "projects_count",
    "hackathons_count",
    "certifications_count",
    "aptitude_score",
    "communication_score",
    "coding_skill_score",
    "github_repos",
    "mock_interview_score"
]

# Valid options for categorical inputs
BRANCH_OPTIONS = ["CSE", "IT", "ECE", "ENTC", "Civil", "Mechanical"]
GENDER_OPTIONS = ["Male", "Female", "Other"]
TRAINING_OPTIONS = ["Yes", "No"]

# Value range validation rules for student inputs & CSV uploads
NUMERIC_RANGES = {
    "age": (18, 32),
    "cgpa": (0.0, 10.0),
    "backlogs": (0, 12),
    "attendance_percentage": (0.0, 100.0),
    "dsa_questions_solved": (0, 1500),
    "leetcode_questions_solved": (0, 1000),
    "hackerrank_questions_solved": (0, 800),
    "github_repos": (0, 100),
    "internships_count": (0, 10),
    "projects_count": (0, 20),
    "hackathons_count": (0, 15),
    "certifications_count": (0, 15),
    "aptitude_score": (0.0, 100.0),
    "communication_score": (0.0, 10.0),
    "coding_skill_score": (0.0, 10.0),
    "mock_interview_score": (0.0, 10.0)
}
