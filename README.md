# ✨ PLACEMENT IQ: Student Placement Intelligence & Data Warehousing Platform

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQLite Star Schema](https://img.shields.io/badge/SQLite-Star--Schema%20DWH-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Validation Status](https://img.shields.io/badge/Tests-13%2F13%20Passing-10B981?style=for-the-badge&logo=checkmarx&logoColor=white)](file:///TEST_REPORT.md)

---

## 📌 Executive Summary

**PLACEMENT IQ** is an enterprise-grade academic data intelligence platform designed for higher-education institutions, campus placement cells (TPO), and undergraduate students. It combines **Data Warehousing (DWH)**, **Multi-Dimensional On-Line Analytical Processing (OLAP)**, and **Supervised & Unsupervised Data Mining** into a unified, privacy-compliant institutional analytics hub.

* **For Students**: A proactive placement career copilot. Students assess real-time placement probability using trained machine learning classifiers, benchmark their skill profile against 15,000 alumni records via multi-dimensional radar visualizations, and receive targeted, mathematically computed action roadmaps.
* **For Administrators**: A comprehensive DWM command center. Faculty leads, Training & Placement Officers (TPOs), and Deans perform deep-dive multidimensional slice-and-dice queries, run simultaneous 2D roll-ups/drill-downs, retrain classification and continuous regression models, conduct K-Means & Agglomerative clustering, and dispatch personalized student guidance.

---

## 🏛️ System Architecture

```
                                    ┌───────────────────────────────────────┐
                                    │       PUBLIC ACCESS & ROUTING         │
                                    │    Landing Page & Common Login        │
                                    └───────────────────┬───────────────────┘
                                                        │
                                          Role Auto-Detection (PBKDF2)
                                                        │
                          ┌─────────────────────────────┴─────────────────────────────┐
                          ▼                                                           ▼
       ┌─────────────────────────────────────┐                     ┌─────────────────────────────────────┐
       │         STUDENT WORKSPACE           │                     │        ADMINISTRATOR CENTER         │
       ├─────────────────────────────────────┤                     ├─────────────────────────────────────┤
       │ 📊 Dynamic Placement Dashboard      │                     │ 🛡️ Executive Overview & DWM Lineage  │
       │ 👤 Candidate Profile & Portfolios   │                     │ 👥 Candidate Directory & Audit      │
       │ 🎯 Live ML Placement Inference      │                     │ 🏛️ Star-Schema Console & SQL Runner │
       │ 🕸️ Multi-Dimensional Radar Benchmark│                     │ 🧊 Universal Dynamic OLAP Engine    │
       │ 📈 Targeted Action Roadmap          │                     │ ⛏️ Data Mining & Association Rules │
       │ 📜 Historical Prediction Timeline   │                     │ 🎯 Classification Suite (DT, RF, NB)│
       │ 🚪 Secure Session Logout            │                     │ 📈 Continuous Regression (SLR, MLR) │
       │                                     │                     │ 🔮 K-Means & Elbow Cluster Analysis │
       │                                     │                     │ 🌳 Agglomerative Hierarchical & Dend│
       │                                     │                     │ ⚖️ Side-by-Side Cluster Benchmark   │
       │                                     │                     │ 🚀 Prediction Center & Batch CSV    │
       │                                     │                     │ 📄 Institutional Reports & PDF/CSV  │
       │                                     │                     │ ⚙️ System Governance & Model Switch │
       └──────────────────┬──────────────────┘                     └──────────────────┬──────────────────┘
                          │                                                           │
                          └─────────────────────────────┬─────────────────────────────┘
                                                        │
                                                        ▼
                                    ┌───────────────────────────────────────┐
                                    │          ANALYTICS BACKEND            │
                                    ├───────────────────────────────────────┤
                                    │ • Unified Dataset Engine (Base + DB)  │
                                    │ • Mathematical Gap Recommendation     │
                                    │ • Multi-Dimensional OLAP Cube Builder  │
                                    │ • Scikit-Learn Inference Pipeline     │
                                    │ • Star-Schema SQLite Warehouse (R/W)  │
                                    └───────────────────────────────────────┘
```

---

## ⚡ Core Platform Differentiators

| Capability | Implementation Architecture | Impact / Value |
| :--- | :--- | :--- |
| **Strict Dataset Grounding** | Certified `placement_prediction_cleaned.csv` (15,000 rows, 26 features) | Zero hallucinated or fabricated metrics; 100% verified empirical distributions. |
| **Clean Onboarding Gating** | Session and profile completion verifier (`is_completed = 1`) | Brand new accounts start completely empty; no fake mock data or placeholder numbers are shown until the student enters their details. |
| **Unified Dataset Architecture** | SQLite normalization + automated feature harmonization | Admins seamlessly switch analysis between original 15,000 baseline records and the live unified dataset ($15,000 + N$ records). |
| **2D Dynamic OLAP Operations** | Simultaneous multi-axis roll-up and drill-down across rows and columns | Interactive matrix de-aggregation and summarization with automatic audit query logging. |
| **Mathematical Gap Engine** | $Gap = \text{Placed Median} - \text{Student Score}$ | Produces quantitative, prioritized deficits with exact targets for student recruitment readiness. |
| **Dual ML Paradigm** | Supervised (Classification + Continuous Regression) & Unsupervised Clustering | Provides binary classification, continuous score forecasting, and unsupervised cohort segmentation. |

---

## 📊 Dataset Specifications & Data Governance

The foundation of PLACEMENT IQ is the certified university placement dataset:
* **Primary Path**: `data/placement_prediction_cleaned.csv`
* **Volume**: 15,000 verified candidate records
* **Dimensions**: 26 feature columns (16 continuous numeric, 9 one-hot encoded categories, 1 binary target)
* **Target Feature**: `placement_prediction` (`1` = Placed, `0` = Not Placed)
* **Class Balance**: 6,357 Placed (42.38%) vs. 8,643 Not Placed (57.62%)
* **Data Cleansing**: 0 missing values, 0 duplicate rows, zero synthetic noise

### Star-Schema Data Warehouse Design

The database (`outputs/placement_dw.sqlite`) implements a Kimball-style Star Schema refreshed directly from the Unified Dataset:

```
                            ┌────────────────────────┐
                            │      DimStudent        │
                            ├────────────────────────┤
                            │ PK  student_key        │
                            │     age                │
                            │     gender             │
                            │     branch             │
                            └───────────┬────────────┘
                                        │
                                        │ 1:N
                                        ▼
┌────────────────────────┐  N:1 ┌────────────────────────┐ 1:N  ┌────────────────────────┐
│      DimAcademic       ├─────►│     FactPlacement      │◄─────┤       DimSkills        │
├────────────────────────┤      ├────────────────────────┤      ├────────────────────────┤
│ PK  academic_key       │      │ PK  fact_id            │      │ PK  skill_key          │
│     cgpa               │      │ FK  student_key        │      │     dsa_questions      │
│     backlogs           │      │ FK  academic_key       │      │     leetcode_questions │
│     attendance_pct     │      │ FK  skill_key          │      │     hackerrank_quest   │
└────────────────────────┘      │ FK  engagement_key     │      │     coding_skill_score │
                                │ FK  placement_key      │      │     aptitude_score     │
                                │     cgpa               │      │     communication_score│
                                │     attendance_pct     │      └────────────────────────┘
                                │     dsa_questions      │
                                │     aptitude_score     │
                                │     placed_flag        │
                                └───────────▲────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                     N:1 │                             │ N:1
        ┌────────────────┴───────┐      ┌──────────────┴─────────┐
        │     DimEngagement      │      │      DimPlacement      │
        ├────────────────────────┤      ├────────────────────────┤
        │ PK  engagement_key     │      │ PK  placement_key      │
        │     internships_count  │      │     placement_status   │
        │     projects_count     │      │     placement_pred     │
        │     hackathons_count   │      │     training_status    │
        │     github_repos       │      └────────────────────────┘
        │     mock_interview_sc  │
        └────────────────────────┘
```

---

## 🧠 Machine Learning & Data Mining Suite

### 1. Supervised Classification
* **Algorithms**: Random Forest (Ensemble Bagging), Decision Tree (CART), Gaussian Naive Bayes.
* **Tunable Hyperparameters**: Max depth, splitting criterion (Gini/Entropy), min samples split, number of estimators, Laplace smoothing variance.
* **Evaluation Framework**: 5-fold Stratified K-Fold Cross-Validation, Confusion Matrices, ROC-AUC Curves, Precision-Recall Curves, and Gini Feature Importances.
* **Production Deployment**: Administrators designate the active production model in 1 click; the chosen classifier instantly powers all student-facing inference endpoints.

### 2. Continuous Numerical Regression
* **Target Variables**: `aptitude_score`, `coding_skill_score`, `cgpa`, `mock_interview_score`.
* **Algorithms**: Simple Linear Regression (SLR) and Multiple Linear Regression (MLR).
* **Statistical Metrics**: Coefficient of Determination ($R^2$), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and residual distribution normality tests.

### 3. Unsupervised Clustering & Cohort Segmentation
* **K-Means Clustering**: WCSS Elbow Method analysis (configurable $K=2$ to $10$), Silhouette score optimization, cluster centroid radar geometry, and 2D PCA projection scatter.
* **Agglomerative Hierarchical**: Ward, Complete, and Average linkage criteria with interactive Scipy/Plotly Dendrogram trees.
* **Cluster Benchmarking**: Direct side-by-side comparison of partition geometries, silhouette coefficients, and computational runtime.

### 4. Dynamic OLAP Engine
* **Slice**: Dynamic single-dimension filtering with instant distribution histograms.
* **Dice**: Multi-dimensional sub-cube extraction with conjunctional filters.
* **2D Simultaneous Roll-Up**: Co-aggregates both row-axis hierarchies (e.g. `[Branch, Gender] → [Branch]`) and column-axis dimensions simultaneously.
* **2D Simultaneous Drill-Down**: De-aggregates row and column dimensions simultaneously into granular sub-matrices.
* **Pivot**: Multi-axis rotation matrix with interactive heatmaps.
* **Drill-Across**: Combines multi-table measures across Fact and Dimension tables via foreign key traversals.
* **Query Audit Trail**: Every executed OLAP operation logs dimensions, aggregation functions, and row counts to SQLite `olap_query_history`.

---

## 👥 Authentication & Demo Credentials

Authentication uses PBKDF2 HMAC SHA-256 with random salt across 100,000 hashing rounds. User roles are resolved automatically from the SQLite database upon login.

| Portal Role | Registered Email | Password | Pre-loaded Context / Purpose |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@college.com` | `admin123` | Prof. K. Sharma (DWM Lead, Executive Overview, SQL Workbench) |
| **Administrator** | `placement@college.com` | `placement123` | Dean D. Joshi (TPO Lead, Candidate Directory, Model Selection) |
| **Student (Placed)** | `student@college.com` | `student123` | Rohan Verma (CSE, CGPA 8.74, 380 DSA, High Placement Readiness) |
| **Student (Action Needed)**| `vikram.m@campus.edu` | `student123` | Vikram Malhotra (Mech, CGPA 6.10, Low Attendance, Action Plan) |
| **New Student** | *Use "Create Account"* | *Any (4+ chars)* | **Empty onboarding state** — demonstrates zero pre-filled mock data |

---

## 🚀 Installation & Quickstart

### Prerequisites
* Python 3.10, 3.11, or 3.12
* Windows, Linux, or macOS

### 1. Clone & Navigate to Workspace
```bash
git clone https://github.com/your-org/DWM_Project.git
cd DWM_Project
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Comprehensive Verification Suite
Validate dataset integrity, database normalization, ML pipelines, and OLAP functionality:
```bash
python validate_project.py
```
> **Expected Output**: `ALL 13 AUTOMATED TEST SUITES PASSED SUCCESSFULLY (13/13)!`

### 5. Launch the Platform
```bash
streamlit run app.py
```
*Or on Windows, simply double-click **`run_dashboard.bat`**.*

Access the interactive web portal at: `http://localhost:8501`

---

## 📂 Repository File Directory

```
DWM_Project/
├── app.py                      # Multi-role entry point & st.navigation router
├── requirements.txt            # Certified Python dependencies
├── run_dashboard.bat           # 1-Click Windows execution launcher
├── validate_project.py         # 13-suite automated test engine
├── README.md                   # Platform architecture & user manual
├── TEST_REPORT.md              # System validation & benchmark report
│
├── data/
│   └── placement_prediction_cleaned.csv  # 15,000 certified records (1.6 MB)
│
├── docs/
│   ├── STAR_SCHEMA.md          # Star schema relational specifications
│   └── project_report.md       # DWM architecture report
│
├── models/                     # Persisted scikit-learn serializations (.joblib)
│   ├── random_forest.joblib    # High-capacity ensemble classifier
│   ├── decision_tree.joblib    # Interpretable decision tree classifier
│   ├── naive_bayes.joblib      # Gaussian probabilistic classifier
│   ├── kmeans.joblib           # Pre-fitted K-Means clustering model
│   ├── slr.joblib              # Simple linear regression model
│   └── mlr.joblib              # Multiple linear regression model
│
├── outputs/                    # SQLite database & analytical exports
│   ├── placement_dw.sqlite     # Star-Schema SQLite database (Users, DWH, History)
│   ├── classification_metrics.csv
│   ├── regression_metrics.csv
│   ├── kmeans_cluster_profiles.csv
│   ├── agglomerative_output.csv
│   └── VALIDATION_REPORT.md
│
├── pages/                      # 19 Dedicated Streamlit multi-page views
│   ├── 0_Home.py               # Public landing page with live institutional KPIs
│   ├── 0_Login.py              # Common Sign In & New Student Registration
│   ├── 1_Student_Dashboard.py  # Student placement readiness overview (gated)
│   ├── 2_Student_Profile.py    # 20-parameter candidate profile entry form
│   ├── 3_Placement_Prediction.py# Real-time probabilistic ML placement inference
│   ├── 4_Skill_Analysis.py     # Multi-dimensional radar vs. placed medians
│   ├── 5_Improvement_Plan.py   # Prioritized gap analysis & targeted roadmap
│   ├── 6_Prediction_History.py # Historical predictions & faculty feedback log
│   ├── 10_Admin_Dashboard.py   # Executive analytics & unified dataset switcher
│   ├── 11_Student_Data.py      # Searchable candidate directory & feedback dispatch
│   ├── 12_Data_Warehouse.py    # Star-Schema visualizer & SQL query workbench
│   ├── 13_OLAP.py              # Universal OLAP builder, 2D Roll-Up & Drill-Down
│   ├── 14_Data_Mining.py       # Feature correlations, Mutual Info, Apriori rules
│   ├── 15_Classification.py    # Classification benchmarks & production selector
│   ├── 16_Regression.py        # Continuous numerical regression (SLR & MLR)
│   ├── 17_KMeans.py            # K-Means clustering, WCSS Elbow & PCA plots
│   ├── 18_Agglomerative.py     # Agglomerative clustering & Scipy dendrograms
│   ├── 19_Cluster_Comparison.py# Side-by-side clustering metrics benchmark
│   ├── 20_Admin_Predictor.py   # Candidate inference & batch CSV prediction
│   ├── 21_Reports.py           # Institutional report generation & CSV downloads
│   ├── 22_Settings.py          # DWH maintenance & production configuration
│   └── 99_Logout.py            # Secure session termination
│
└── src/                        # 16 Modular backend engine modules
    ├── __init__.py             # Python package marker
    ├── auth.py                 # PBKDF2 password hashing & session state management
    ├── database.py             # SQLite normalized tables & transaction handlers
    ├── config.py               # Feature schemas, bounds, and admin accounts
    ├── preprocessing.py        # Dataset validation & Unified Dataset engine
    ├── warehouse.py            # Kimball star-schema builder & SQL executor
    ├── olap.py                 # Multi-dimensional OLAP cubes (Slice, Dice, 2D)
    ├── recommendations.py      # Statistical gap analysis & recommendation logic
    ├── classification.py       # Classifier model training & performance evaluation
    ├── regression.py           # Continuous target regression modeling (SLR/MLR)
    ├── clustering.py           # K-Means, Elbow curve, Agglomerative clustering
    ├── prediction.py           # Model inference pipeline & batch scoring
    ├── data_mining.py          # Pearson correlations, mutual info, Apriori rules
    ├── visualizations.py       # Plotly radar charts, confusion matrices, PCA
    ├── ui.py                   # Global dark glassmorphism CSS & navigation components
    └── submissions.py          # Public profile URL parser & feature extractor
```

---

## 🧪 Comprehensive Quality Assurance & Test Matrix

All system components are continuously validated against a 13-suite automated test engine ([`validate_project.py`](file:///validate_project.py)):

| Test Suite | Subsystem Tested | Key Verifications & Assertions | Status |
| :---: | :--- | :--- | :---: |
| **Suite 1** | **Dataset Integrity** | Validates exact 15,000 rows, 26 expected columns, 0 nulls, 0 duplicates | **PASS** |
| **Suite 2** | **Database Schema** | Verifies normalized SQLite tables (`users`, `student_profiles`, `student_predictions`, `admin_feedback`) | **PASS** |
| **Suite 3** | **Security & Auth** | PBKDF2 password hashing roundtrip, student role enforcement, admin privileges | **PASS** |
| **Suite 4** | **Unified Engine** | Merges 15,000 baseline records with dynamic SQLite profiles into unified cohort | **PASS** |
| **Suite 5** | **Classification** | Trains Decision Tree, Random Forest, Naive Bayes; verifies safe numeric subset formatting | **PASS** |
| **Suite 6** | **Regression** | Fits SLR & MLR on continuous targets (`aptitude_score`); asserts $R^2$, RMSE, MSE | **PASS** |
| **Suite 7** | **Clustering** | Executes K-Means (Elbow $K=2..5$) and Agglomerative Hierarchical ($n=1,000$ dendrogram) | **PASS** |
| **Suite 8** | **Data Mining** | Computes Pearson correlation matrix, mutual information gain, Gini feature importance | **PASS** |
| **Suite 9** | **Star Schema DWH** | Rebuilds SQLite `FactPlacement` ($15,000+$ rows) and 5 relational dimension tables | **PASS** |
| **Suite 10**| **Dynamic OLAP** | Verifies Slice, Dice, Pivot, Drill-Across, 2D Simultaneous Roll-Up & Drill-Down, Query Audit | **PASS** |
| **Suite 11**| **Recommendation** | Computes mathematical gaps vs. placed cohort medians; verifies readiness categorization | **PASS** |
| **Suite 12**| **Batch Scoring** | Validates high-throughput candidate scoring and probability confidence export | **PASS** |
| **Suite 13**| **Feedback Loop** | Dispatches administrative assessments and alerts to Student Dashboard | **PASS** |

---

## 📜 Academic Attribution & License

* **Project**: Student Placement Analytics & Intelligence Platform (PLACEMENT IQ)
* **Domain**: Data Warehousing & Data Mining (DWM)
* **Dataset Reference**: 15,000 Certified University Placement Records (`placement_prediction_cleaned.csv`)
* **License**: MIT Academic License — open for institutional research, teaching, and academic evaluation.

