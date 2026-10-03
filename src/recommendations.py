import pandas as pd
import numpy as np
from .preprocessing import load_data
from .config import TARGET, BASE_NUMERIC

# Actionable domain advice mapped to actual dataset features
FEATURE_GUIDANCE = {
    "dsa_questions_solved": {
        "title": "DSA & Algorithmic Problem Solving",
        "category": "Coding & Algorithms",
        "unit": "problems",
        "direction": "higher",
        "advice": "Increase your DSA practice on LeetCode/HackerRank. Focus on arrays, strings, binary search, trees, graphs, and dynamic programming patterns to clear technical coding rounds."
    },
    "coding_skill_score": {
        "title": "Technical Coding Skill Score",
        "category": "Programming Fundamentals",
        "unit": "/ 10",
        "direction": "higher",
        "advice": "Strengthen core programming language fundamentals (OOP, memory management, clean code architecture). Build mini-modules and practice rapid implementation under timed conditions."
    },
    "aptitude_score": {
        "title": "Quantitative & Logical Aptitude",
        "category": "Aptitude Screening",
        "unit": "/ 100",
        "direction": "higher",
        "advice": "Practice quantitative aptitude, data interpretation, and logical puzzles. Recruiters use online aptitude tests as the primary screening filter before technical interviews."
    },
    "communication_score": {
        "title": "Communication & Articulation",
        "category": "Soft Skills & HR",
        "unit": "/ 10",
        "direction": "higher",
        "advice": "Participate in group discussions, behavioral mock interviews, and practice explaining your technical project decisions clearly using the STAR framework."
    },
    "mock_interview_score": {
        "title": "Mock Interview Performance",
        "category": "Interview Preparedness",
        "unit": "/ 10",
        "direction": "higher",
        "advice": "Schedule simulated peer and mentor mock interviews. Focus on live problem solving, thinking aloud, and handling follow-up technical questions with confidence."
    },
    "internships_count": {
        "title": "Practical Industry Internships",
        "category": "Work Experience",
        "unit": "internships",
        "direction": "higher",
        "advice": "Gain practical industry exposure through software internships, open-source contributions, or university research projects to demonstrate production experience."
    },
    "projects_count": {
        "title": "Portfolio Technical Projects",
        "category": "Practical Development",
        "unit": "projects",
        "direction": "higher",
        "advice": "Build 2-3 end-to-end full-stack or machine learning projects with working live demos and clean GitHub README documentation. Be prepared to defend your architecture choices."
    },
    "github_repos": {
        "title": "Public GitHub Repositories",
        "category": "Open Source & Code Proof",
        "unit": "repositories",
        "direction": "higher",
        "advice": "Maintain an active GitHub profile with organized public repositories, informative commit histories, and meaningful documentation for all capstone projects."
    },
    "attendance_percentage": {
        "title": "Classroom Attendance Record",
        "category": "Academic Discipline",
        "unit": "%",
        "direction": "higher",
        "advice": "Maintain your classroom attendance strictly above 75%. Most Tier-1 campus placement guidelines enforce a 75%+ attendance eligibility threshold."
    },
    "backlogs": {
        "title": "Active Backlogs Count",
        "category": "Academic Standing",
        "unit": "backlogs",
        "direction": "lower",
        "advice": "Clear all pending backlogs as top priority. Most visiting tech companies enforce a strict zero-active-backlog eligibility criterion for day-one drives."
    },
    "cgpa": {
        "title": "Academic Cumulative GPA",
        "category": "Academic Performance",
        "unit": "CGPA",
        "direction": "higher",
        "advice": "Improve semester exam performance to maintain CGPA above university and recruiter cutoffs (typically 7.0+ for IT/Product drives)."
    },
    "placement_training": {
        "title": "Campus Placement Training",
        "category": "Training Participation",
        "unit": "",
        "direction": "higher",
        "advice": "Enroll in the structured campus pre-placement training modules covering aptitude shortcuts, coding workshops, and resume writing."
    }
}

def generate_recommendations(student_dict, reference_df=None):
    """
    Generate data-driven, actionable recommendations by comparing student features
    against placed candidate medians and distributions from the dataset.
    Returns:
        dict containing:
        - strengths: list of strong areas
        - weaknesses: list of detailed gap analysis objects
        - overall_readiness_level: High / Moderate / Developing
    """
    if reference_df is None:
        reference_df = load_data()

    placed_cohort = reference_df[reference_df[TARGET] == 1]
    all_cohort = reference_df

    gaps = []
    strengths = []

    for feature, meta in FEATURE_GUIDANCE.items():
        if feature == "placement_training":
            val = str(student_dict.get(feature, "Yes")).lower()
            if val in ["no", "false", "0"]:
                gaps.append({
                    "feature": feature,
                    "title": meta["title"],
                    "category": meta["category"],
                    "student_val": "No",
                    "benchmark_val": "Yes",
                    "unit": "",
                    "gap": 1.0,
                    "priority": "High",
                    "advice": meta["advice"]
                })
            else:
                strengths.append({
                    "feature": feature,
                    "title": meta["title"],
                    "detail": "Enrolled in campus placement training programs"
                })
            continue

        if feature not in reference_df.columns:
            continue

        try:
            s_val = float(student_dict.get(feature, 0.0))
        except (ValueError, TypeError):
            continue

        placed_median = float(placed_cohort[feature].median())
        all_median = float(all_cohort[feature].median())

        if meta["direction"] == "lower":
            # For backlogs: lower is better
            if s_val > 0:
                gaps.append({
                    "feature": feature,
                    "title": meta["title"],
                    "category": meta["category"],
                    "student_val": f"{int(s_val)}",
                    "benchmark_val": "0",
                    "unit": meta["unit"],
                    "gap": float(s_val),
                    "priority": "Critical" if s_val >= 2 else "High",
                    "advice": meta["advice"]
                })
            else:
                strengths.append({
                    "feature": feature,
                    "title": meta["title"],
                    "detail": "Zero active backlogs — fully eligible for campus recruitment"
                })
        else:
            # For positive metrics: higher is better
            if s_val < placed_median:
                gap = round(placed_median - s_val, 2)
                percentile = (reference_df[feature] <= s_val).mean() * 100
                priority = "High" if s_val < all_median else "Medium"
                
                gaps.append({
                    "feature": feature,
                    "title": meta["title"],
                    "category": meta["category"],
                    "student_val": f"{s_val:.1f}" if s_val % 1 != 0 else f"{int(s_val)}",
                    "benchmark_val": f"{placed_median:.1f}" if placed_median % 1 != 0 else f"{int(placed_median)}",
                    "unit": meta["unit"],
                    "gap": gap,
                    "percentile": round(percentile, 1),
                    "priority": priority,
                    "advice": meta["advice"]
                })
            else:
                strengths.append({
                    "feature": feature,
                    "title": meta["title"],
                    "detail": f"Above placed median ({s_val:.1f} vs {placed_median:.1f} {meta['unit']})"
                })

    # Sort gaps by priority: Critical > High > Medium
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    gaps.sort(key=lambda x: (priority_order.get(x["priority"], 9), -x["gap"]))

    readiness = "High Readiness" if len(gaps) <= 2 else ("Moderate Readiness" if len(gaps) <= 5 else "Developing Readiness")

    return {
        "readiness_level": readiness,
        "top_improvements": gaps[:5],
        "all_improvements": gaps,
        "strengths": strengths[:5]
    }
