import sqlite3
import pandas as pd
from pathlib import Path
from .config import DB_PATH

STAR_SCHEMA_DEF = {
    "FactPlacement": [
        "fact_id (PK)", "student_key (FK)", "cgpa", "attendance_percentage",
        "aptitude_score", "coding_skill_score", "internships_count", "projects_count", "placement_prediction"
    ],
    "DimStudent": [
        "student_key (PK)", "age", "gender", "branch", "data_source"
    ],
    "DimAcademic": [
        "student_key (PK)", "cgpa", "backlogs", "attendance_percentage", "cgpa_band"
    ],
    "DimSkills": [
        "student_key (PK)", "dsa_questions_solved", "leetcode_questions_solved",
        "hackerrank_questions_solved", "aptitude_score", "communication_score",
        "coding_skill_score", "certifications_count", "coding_band"
    ],
    "DimEngagement": [
        "student_key (PK)", "internships_count", "projects_count",
        "hackathons_count", "github_repos", "mock_interview_score", "placement_training"
    ],
    "DimPlacement": [
        "student_key (PK)", "placement_prediction", "placement_status"
    ]
}

RELATIONSHIPS = [
    {"from": "FactPlacement.student_key", "to": "DimStudent.student_key", "cardinality": "N:1", "type": "Identifying"},
    {"from": "FactPlacement.student_key", "to": "DimAcademic.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimSkills.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimEngagement.student_key", "cardinality": "1:1", "type": "Dimensional"},
    {"from": "FactPlacement.student_key", "to": "DimPlacement.student_key", "cardinality": "1:1", "type": "Target Dimension"}
]

def build_warehouse(df, db_path=DB_PATH):
    """Construct or refresh the SQLite Star-Schema Data Warehouse."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    
    # Drop existing warehouse tables
    con.execute("DROP TABLE IF EXISTS FactPlacement")
    for t in ["DimStudent", "DimAcademic", "DimSkills", "DimEngagement", "DimPlacement"]:
        con.execute(f"DROP TABLE IF EXISTS {t}")
        
    base = df.reset_index(drop=True).copy()
    base["student_key"] = range(1, len(base) + 1)
    if "data_source" not in base.columns:
        base["data_source"] = "Original Dataset"
    
    # Populate Dimension Tables
    pd.DataFrame({
        "student_key": base.student_key,
        "age": base.age,
        "gender": base.gender,
        "branch": base.branch,
        "data_source": base.data_source
    }).to_sql("DimStudent", con, index=False)
    
    acad_cols = ["student_key", "cgpa", "backlogs", "attendance_percentage"]
    if "cgpa_band" in base.columns:
        acad_cols.append("cgpa_band")
    base[acad_cols].to_sql("DimAcademic", con, index=False)
    
    skills_cols = [
        "student_key", "dsa_questions_solved", "leetcode_questions_solved",
        "hackerrank_questions_solved", "aptitude_score", "communication_score",
        "coding_skill_score", "certifications_count"
    ]
    if "coding_band" in base.columns:
        skills_cols.append("coding_band")
    base[skills_cols].to_sql("DimSkills", con, index=False)
    
    base[[
        "student_key", "internships_count", "projects_count", "hackathons_count",
        "github_repos", "mock_interview_score", "placement_training"
    ]].to_sql("DimEngagement", con, index=False)
    
    base[["student_key", "placement_prediction", "placement_status"]].to_sql("DimPlacement", con, index=False)
    
    # Populate Central Fact Table
    fact = base[[
        "student_key", "cgpa", "attendance_percentage", "aptitude_score",
        "coding_skill_score", "internships_count", "projects_count", "placement_prediction"
    ]].copy()
    fact["fact_id"] = range(1, len(fact) + 1)
    fact.to_sql("FactPlacement", con, index=False)
    
    # Create surrogate key indexes for high-throughput OLAP joins
    con.execute("CREATE INDEX IF NOT EXISTS idx_fact_student ON FactPlacement(student_key)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_dim_student ON DimStudent(student_key)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_dim_academic ON DimAcademic(student_key)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_dim_skills ON DimSkills(student_key)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_dim_engagement ON DimEngagement(student_key)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_dim_placement ON DimPlacement(student_key)")
    
    con.commit()
    con.close()
    return db_path

def query(sql, db_path=DB_PATH):
    """Execute arbitrary SQL queries against the warehouse database."""
    con = sqlite3.connect(db_path)
    try:
        out = pd.read_sql_query(sql, con)
    finally:
        con.close()
    return out

PRESET_QUERIES = [
    {
        "id": "branch_performance",
        "title": "Branch-wise Placement Rate & Performance",
        "description": "Multi-table join (FactPlacement + DimStudent + DimPlacement) computing cohort placement conversion rates, average CGPA, and average coding scores across engineering branches.",
        "sql": """SELECT 
    d.branch,
    COUNT(f.student_key) AS total_students,
    SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_students,
    ROUND(100.0 * SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) / COUNT(f.student_key), 2) AS placement_rate_pct,
    ROUND(AVG(f.cgpa), 2) AS avg_cgpa,
    ROUND(AVG(f.coding_skill_score), 2) AS avg_coding_score
FROM FactPlacement f
JOIN DimStudent d ON f.student_key = d.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
GROUP BY d.branch
ORDER BY placement_rate_pct DESC;"""
    },
    {
        "id": "coding_dsa_impact",
        "title": "Coding Proficiency & Problem Solving Impact",
        "description": "Evaluates the direct correlation between competitive programming questions (DSA, LeetCode) and placement outcomes categorized by coding band.",
        "sql": """SELECT 
    s.coding_band,
    COUNT(f.student_key) AS student_count,
    ROUND(AVG(s.dsa_questions_solved), 1) AS avg_dsa_solved,
    ROUND(AVG(s.leetcode_questions_solved), 1) AS avg_leetcode_solved,
    ROUND(AVG(f.coding_skill_score), 2) AS avg_coding_score,
    ROUND(100.0 * SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) / COUNT(f.student_key), 2) AS placement_rate_pct
FROM FactPlacement f
JOIN DimSkills s ON f.student_key = s.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
WHERE s.coding_band IS NOT NULL AND s.coding_band != 'nan'
GROUP BY s.coding_band
ORDER BY avg_coding_score DESC;"""
    },
    {
        "id": "internship_project_matrix",
        "title": "Experiential Learning: Internships & Projects Matrix",
        "description": "Cross-dimensional analysis of practical portfolio strength (internships, completed projects, mock interviews) against candidate placement success.",
        "sql": """SELECT 
    e.internships_count,
    e.projects_count,
    COUNT(f.student_key) AS cohort_size,
    ROUND(AVG(f.cgpa), 2) AS avg_cgpa,
    ROUND(AVG(e.mock_interview_score), 1) AS avg_interview_score,
    ROUND(100.0 * SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) / COUNT(f.student_key), 2) AS placement_rate_pct
FROM FactPlacement f
JOIN DimEngagement e ON f.student_key = e.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
GROUP BY e.internships_count, e.projects_count
HAVING cohort_size >= 15
ORDER BY placement_rate_pct DESC
LIMIT 12;"""
    },
    {
        "id": "high_risk_academics",
        "title": "Academic Risk Stratification (CGPA & Backlogs)",
        "description": "Identifies vulnerable student cohorts based on academic standing, backlog count, and attendance for targeted institutional remediation.",
        "sql": """SELECT 
    a.cgpa_band,
    a.backlogs,
    COUNT(f.student_key) AS student_count,
    ROUND(AVG(a.attendance_percentage), 1) AS avg_attendance,
    ROUND(AVG(f.aptitude_score), 1) AS avg_aptitude,
    ROUND(100.0 * SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) / COUNT(f.student_key), 2) AS placement_rate_pct
FROM FactPlacement f
JOIN DimAcademic a ON f.student_key = a.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
WHERE a.cgpa_band IS NOT NULL
GROUP BY a.cgpa_band, a.backlogs
ORDER BY a.cgpa_band DESC, a.backlogs ASC;"""
    },
    {
        "id": "gender_training_equity",
        "title": "Gender Equity & Training Intervention Efficacy",
        "description": "Measures placement distribution parity across genders and assesses the lift delivered by the institutional placement training program.",
        "sql": """SELECT 
    d.gender,
    e.placement_training,
    COUNT(f.student_key) AS total_enrolled,
    ROUND(AVG(f.cgpa), 2) AS avg_cgpa,
    ROUND(AVG(f.coding_skill_score), 2) AS avg_coding,
    ROUND(AVG(f.aptitude_score), 2) AS avg_aptitude,
    ROUND(100.0 * SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) / COUNT(f.student_key), 2) AS placement_rate_pct
FROM FactPlacement f
JOIN DimStudent d ON f.student_key = d.student_key
JOIN DimEngagement e ON f.student_key = e.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
GROUP BY d.gender, e.placement_training
ORDER BY d.gender, placement_rate_pct DESC;"""
    }
]

def get_warehouse_summary(db_path=DB_PATH):
    """Retrieve metadata, table row counts, and schema definitions."""
    if not db_path.exists():
        return {}
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    tables = [
        "FactPlacement", "DimStudent", "DimAcademic", "DimSkills", "DimEngagement", "DimPlacement"
    ]
    summary = {}
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]
            summary[t] = {
                "rows": cnt,
                "columns": STAR_SCHEMA_DEF.get(t, [])
            }
        except Exception:
            summary[t] = {"rows": 0, "columns": []}
    con.close()
    return summary

def get_warehouse_health(db_path=DB_PATH):
    """Evaluate warehouse physical storage and referential integrity."""
    if not db_path.exists():
        return {
            "exists": False,
            "storage_size_bytes": 0,
            "storage_size_mb": 0.0,
            "referential_integrity_pct": 0.0,
            "orphaned_records": 0,
            "table_count": 0,
            "total_facts": 0
        }
    
    file_bytes = db_path.stat().st_size
    size_mb = round(file_bytes / (1024 * 1024), 2)
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    total_facts = 0
    orphans = 0
    try:
        cur.execute("SELECT COUNT(*) FROM FactPlacement")
        total_facts = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM FactPlacement WHERE student_key NOT IN (SELECT student_key FROM DimStudent)")
        orphans = cur.fetchone()[0]
    except Exception:
        pass
    finally:
        con.close()
        
    ref_integrity = 100.0 if total_facts > 0 and orphans == 0 else (
        round(100.0 * (total_facts - orphans) / total_facts, 2) if total_facts > 0 else 0.0
    )
    
    return {
        "exists": True,
        "storage_size_bytes": file_bytes,
        "storage_size_mb": size_mb,
        "referential_integrity_pct": ref_integrity,
        "orphaned_records": orphans,
        "table_count": len(STAR_SCHEMA_DEF),
        "total_facts": total_facts
    }

def get_sample_records(table_name, limit=50, db_path=DB_PATH):
    """Fetch sample rows from any warehouse table with validation."""
    if table_name not in STAR_SCHEMA_DEF:
        raise ValueError(f"Table '{table_name}' is not in the Star Schema definition.")
    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", con)
    finally:
        con.close()
    return df

