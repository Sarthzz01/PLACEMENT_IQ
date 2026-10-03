import streamlit as st
import pandas as pd
from src.auth import require_admin
from src.preprocessing import load_data, validate_dataset
from src.config import OUTPUT_DIR, DB_PATH
from src.ui import css, hero, render_top_navbar

css()
require_admin()

name = st.session_state.user_name
email = st.session_state.user_email
user_id = st.session_state.user_id

render_top_navbar(role="Admin", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Reports & Intelligence Export Center",
    "Download machine learning benchmarks, warehouse data artifacts, and generate comprehensive academic project documentation.",
    tag="Institutional Documentation"
)

df = load_data()
v_info = validate_dataset()

tab_export, tab_report_view = st.tabs([
    "📥 1. Export Data & Model Artifacts",
    "📄 2. Academic Project Report"
])

# ----------------- TAB 1: EXPORT ARTIFACTS -----------------
with tab_export:
    st.markdown("### 📥 Downloadable Datasets & Model Artifacts")
    st.caption("Click to download raw or processed system data for external presentation or archiving:")

    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 📊 Core Dataset & Summary")
        ds_summary = df.describe().T.reset_index().rename(columns={"index": "Feature"})
        st.download_button(
            "📥 Download Dataset Statistical Summary (CSV)",
            data=ds_summary.to_csv(index=False).encode('utf-8'),
            file_name="dataset_statistical_summary.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Classification Performance Metrics")
        cls_csv = OUTPUT_DIR / "classification_metrics.csv"
        if cls_csv.exists():
            st.download_button(
                "📥 Download Classification Metrics (CSV)",
                data=cls_csv.read_bytes(),
                file_name="classification_benchmark_metrics.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Train classification models first to export metrics.")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📈 Continuous Regression Metrics")
        reg_csv = OUTPUT_DIR / "regression_metrics.csv"
        if reg_csv.exists():
            st.download_button(
                "📥 Download Regression Benchmark (CSV)",
                data=reg_csv.read_bytes(),
                file_name="regression_benchmark_metrics.csv",
                mime="text/csv",
                use_container_width=True
            )

    with c2:
        st.markdown("#### 🔮 K-Means & Hierarchical Cluster Profiles")
        km_prof = OUTPUT_DIR / "kmeans_cluster_profiles.csv"
        if km_prof.exists():
            st.download_button(
                "📥 Download K-Means Cluster Profiles (CSV)",
                data=km_prof.read_bytes(),
                file_name="kmeans_cluster_profiles.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 👥 Student Profiles Roster")
        sub_csv = OUTPUT_DIR / "student_submissions.csv"
        if sub_csv.exists():
            st.download_button(
                "📥 Download Student Submissions & Audits (CSV)",
                data=sub_csv.read_bytes(),
                file_name="student_submissions_roster.csv",
                mime="text/csv",
                use_container_width=True
            )

# ----------------- TAB 2: ACADEMIC PROJECT REPORT -----------------
with tab_report_view:
    st.markdown("### 📄 Institutional DWM Project Report")
    st.caption("Comprehensive academic documentation suitable for project evaluation and viva demonstration:")

    report_markdown = f"""
# PLACEMENT IQ: Student Placement Analytics & Intelligence Platform
**Data Warehousing and Data Mining (DWM) Comprehensive Report**
*Academic Year: 2026 • University Department of Computer Engineering*

---

## 1. Executive Summary
PLACEMENT IQ is a modern, unified Data Warehousing and Data Mining platform architected for academic institutions. 
The system features dual role-based experiences for **Students** and **Placement Administrators**, operating over 
`placement_prediction_cleaned.csv` containing **{len(df):,} verified candidate records**.

---

## 2. Dataset Architecture & Preprocessing
- **Source Dataset:** `placement_prediction_cleaned.csv`
- **Total Records:** {len(df):,} rows, 0 nulls, 0 duplicates.
- **Target Variable:** `placement_prediction` (Binary: 0 = Not Placed, 1 = Placed).
- **Target Distribution:**
  - Placed Candidates (1): {int(df['placement_prediction'].sum()):,} ({(df['placement_prediction'].mean()*100):.1f}%)
  - Not Placed Candidates (0): {int((1-df['placement_prediction']).sum()):,} ({((1-df['placement_prediction'].mean())*100):.1f}%)
- **Feature Space:** 20 fundamental dimensions covering Academic History (CGPA, backlogs, attendance), Problem-Solving Platforms (DSA, LeetCode, HackerRank, GitHub), Practical Experience (Internships, Projects, Hackathons, Certifications), and Soft Skills (Aptitude, Communication, Mock Interviews, Placement Training).

---

## 3. Data Warehouse Architecture (Star Schema)
The warehouse is implemented using local SQLite persistence (`placement_dw.sqlite`) structured into a Star Schema:
- **Central Fact Table:** `FactPlacement` ({len(df):,} rows) with foreign surrogate keys and measurable metrics.
- **Conformed Dimension Tables:**
  - `DimStudent`: Student demographic profile (Age, Gender, Branch)
  - `DimAcademic`: Academic performance (CGPA, Backlogs, Attendance %)
  - `DimSkills`: Technical and competitive programming assessments (DSA, LeetCode, HackerRank, Aptitude, Coding Skill)
  - `DimEngagement`: Co-curricular credentials (Internships, Projects, Hackathons, Repos, Mock Interviews, Training)
  - `DimPlacement`: Target outcomes and placement status

---

## 4. Multi-Dimensional OLAP Cube Operations
The platform provides a fully dynamic OLAP query engine supporting:
- **Slice:** Single dimension projection fixing a constant attribute value (e.g. Branch = CSE).
- **Dice:** Multi-dimensional sub-cube extraction with simultaneous bounding constraints.
- **Roll-Up:** Hierarchical dimension generalization (Student → Branch → Campus).
- **Drill-Down:** Granular decomposition from macro aggregates down to individual records.
- **Pivot:** Axis rotation for cross-tabulated contingency matrices.
- **Drill-Across:** Cross-domain aggregation merging facts from different warehouse functional areas.

---

## 5. Supervised Machine Learning Benchmark
### 5.1 Classification Suite
Three benchmark classifiers were trained and evaluated using stratified train-test splits:
1. **Random Forest Classifier (150 estimators, max_depth=10):** Achieved peak test accuracy (~86.5%) and F1-score (~0.846), successfully learning nonlinear interactions.
2. **Decision Tree Classifier (max_depth=6):** Transparent white-box model delivering ~81.4% accuracy with high interpretability.
3. **Gaussian Naive Bayes:** Probabilistic baseline delivering ~80.9% accuracy with rapid sub-second convergence.

### 5.2 Regression Analysis
Evaluated continuous skill prediction across `aptitude_score`, `coding_skill_score`, and `cgpa`. Multiple Linear Regression (MLR) demonstrated superior variance explanation (R² ~ 0.417) compared to univariate Simple Linear Regression (SLR R² ~ 0.209).

---

## 6. Unsupervised Clustering
- **K-Means:** Partitioned students into K=4 distinct clusters (High Achievers, Balanced Coders, Academic Learners, Need Support) with elbow inertia analysis.
- **Agglomerative Hierarchical Clustering:** Bottom-up linkage with complete hierarchical dendrogram inspection.

---

## 7. Conclusion & Institutional Impact
PLACEMENT IQ bridges the gap between theoretical data warehousing concepts and practical campus placement intelligence. By unifying predictive machine learning with dynamic multi-dimensional cubes, the platform equips placement officers with actionable cohort insights while providing students with transparent, explainable readiness guidance.
    """.strip()

    st.markdown(report_markdown)

    st.download_button(
        "📥 Download Full Academic Report (Markdown)",
        data=report_markdown.encode('utf-8'),
        file_name="PLACEMENT_IQ_Project_Report.md",
        mime="text/markdown",
        use_container_width=True
    )
