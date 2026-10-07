# 🎓 PLACEMENT IQ: Student Placement Intelligence & Data Warehousing Platform

> **An enterprise-grade academic analytics and decision-support ecosystem bridging dimensional Data Warehousing (Kimball Star Schema), 2D dynamic OLAP cube operations, and dual-paradigm Machine Learning for predictive student career readiness and campus recruitment optimization.**

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![SQLite Star Schema](https://img.shields.io/badge/SQLite-Kimball%20Star--Schema-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Validation Status](https://img.shields.io/badge/Tests-13%2F13%20Passing-10B981?style=for-the-badge&logo=checkmarx&logoColor=white)](TEST_REPORT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🧭 Table of Contents

- [📌 Executive Overview & Core Problem](#-executive-overview--core-problem)
- [⚡ Key Features & Platform Differentiators](#-key-features--platform-differentiators)
- [🏛️ System Architecture & Data Flow](#️-system-architecture--data-flow)
- [📊 Kimball Star-Schema Data Warehouse Design](#-kimball-star-schema-data-warehouse-design)
- [🧊 2D Dynamic OLAP Analytics Engine](#-2d-dynamic-olap-analytics-engine)
- [👥 Dual-Persona Interactive Workspaces](#-dual-persona-interactive-workspaces)
  - [🎓 Student Career Workspace (6 Modules)](#-student-career-workspace)
  - [🛡️ Administrator Intelligence Center (13 Modules)](#️-administrator-intelligence-center)
- [🧠 Machine Learning & Data Mining Suite](#-machine-learning--data-mining-suite)
- [📐 Mathematical Rigor & Formulations](#-mathematical-rigor--formulations)
- [📈 Validated Benchmarks & Empirical Audit](#-validated-benchmarks--empirical-audit)
- [🔐 Authentication & Demo Credentials](#-authentication--demo-credentials)
- [🚀 Quickstart & Installation Guide](#-quickstart--installation-guide)
- [🧪 13-Suite Automated Quality Assurance](#-13-suite-automated-quality-assurance)
- [📂 Repository Directory Anatomy](#-repository-directory-anatomy)
- [🛡️ Security, Privacy & Data Governance](#️-security-privacy--data-governance)
- [❓ Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [📜 Academic Attribution & License](#-academic-attribution--license)

---

## 📌 Executive Overview & Core Problem

Higher education institutions face systemic bottlenecks during campus placement cycles:
1. **Fragmented Academic Records**: Student performance data remains trapped in disparate spreadsheets (CGPA, attendance, competitive coding handles, hackathon participation, and mock interview notes).
2. **Uncalibrated Student Expectations**: Students lack quantitative visibility into industry recruitment benchmarks, often realizing skill deficits only after failing technical screening interviews.
3. **Static, Retrospective TPO Reporting**: Training & Placement Officers (TPOs) and department heads rely on end-of-year tabular reports, lacking multi-dimensional slice-and-dice tools, proactive at-risk student detection, and predictive modeling capabilities.

**PLACEMENT IQ** resolves these institutional challenges by integrating **Dimensional Data Warehousing (Kimball Star Schema)**, **Online Analytical Processing (OLAP)**, and **Dual-Paradigm Machine Learning (Supervised Classification & Regression + Unsupervised Clustering)** into a single, high-performance web analytics application.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                      PLACEMENT IQ                                      │
│                                                                                        │
│   ┌─────────────────────┐    ┌───────────────────────────┐    ┌────────────────────┐   │
│   │   15,000 Verified   │    │    Kimball Star Schema    │    │   Dual-Paradigm    │   │
│   │  Alumni Records +   ├───►│     Data Warehouse        ├───►│  Machine Learning  │   │
│   │ Dynamic Registrations│    │   (Fact + 5 Dimensions)   │    │  (Supervised + US) │   │
│   └─────────────────────┘    └─────────────┬─────────────┘    └─────────┬──────────┘   │
│                                            │                            │              │
│                                            ▼                            ▼              │
│                              ┌───────────────────────────┐    ┌────────────────────┐   │
│                              │      2D Dynamic OLAP      │    │  Multi-Role Web UI │   │
│                              │   Roll-Up, Drill-Down,    ├───►│  Student Portal &  │   │
│                              │   Slice, Dice, Pivot      │    │  Admin Center (22P)│   │
│                              └───────────────────────────┘    └────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Features & Platform Differentiators

| Core Capability | Implementation Architecture | Institutional Value / Impact |
| :--- | :--- | :--- |
| **Strict Dataset Grounding** | Certified `placement_prediction_cleaned.csv` (15,000 records, 26 features) | 100% empirical distributions; zero hallucinated metrics or fabricated benchmarks. |
| **Clean Onboarding Gating** | Session & Profile Completion Verifier (`is_completed = 1`) | Brand-new accounts start completely blank; zero dummy data or unearned scores are displayed until the student enters their details. |
| **Unified Dataset Architecture** | In-memory normalization + SQLite candidate ingestion | Admins toggle seamlessly between the 15,000 baseline records and the live unified dataset ($15,000 + N$ records) without retraining lag. |
| **2D Dynamic OLAP Engine** | Simultaneous multi-axis roll-up and drill-down across arbitrary rows and columns | Interactive matrix summarization and de-aggregation with automatic audit logging to `olap_query_history`. |
| **Mathematical Gap Engine** | $Gap_i = \max(0, \text{Median}_{i}^{(\text{placed})} - \text{Score}_i)$ | Quantifies exact skill and competency deficits, mapping them directly to actionable milestones and priority tiers. |
| **Dual-Paradigm ML Suite** | Supervised (Random Forest, CART, Naive Bayes, SLR, MLR) + Unsupervised (K-Means, Agglomerative) | Combines binary placement inference, continuous aptitude forecasting, and unsupervised student cohort segmentation. |
| **1-Click Model Deployment** | SQLite `system_settings` persistence (`active_model`) | Administrators designate the active production classifier in one click; all student inference endpoints update immediately. |
| **Full Security & RBAC** | PBKDF2 HMAC-SHA256 (100,000 rounds) + Role Enforcement | Cryptographically protected credentials with complete separation of student workspaces and administrative analytics consoles. |

---

## 🏛️ System Architecture & Data Flow

PLACEMENT IQ is architected as a high-throughput, decoupled analytics pipeline:

```
                                    ┌───────────────────────────────────────┐
                                    │       PUBLIC ACCESS & ROUTING         │
                                    │   pages/0_Home.py & 0_Login.py        │
                                    └───────────────────┬───────────────────┘
                                                        │
                                           Role Auto-Detection (PBKDF2)
                                                        │
                           ┌─────────────────────────────┴─────────────────────────────┐
                           ▼                                                           ▼
        ┌─────────────────────────────────────┐                     ┌─────────────────────────────────────┐
        │         STUDENT WORKSPACE           │                     │        ADMINISTRATOR CENTER         │
        ├─────────────────────────────────────┤                     ├─────────────────────────────────────┤
        │ 📊 1_Student_Dashboard.py           │                     │ 🛡️ 10_Admin_Dashboard.py            │
        │ 👤 2_Student_Profile.py             │                     │ 👥 11_Student_Data.py               │
        │ 🎯 3_Placement_Prediction.py        │                     │ 🏛️ 12_Data_Warehouse.py            │
        │ 🕸️ 4_Skill_Analysis.py              │                     │ 🧊 13_OLAP.py                       │
        │ 📈 5_Improvement_Plan.py            │                     │ ⛏️ 14_Data_Mining.py                │
        │ 📜 6_Prediction_History.py          │                     │ 🎯 15_Classification.py             │
        │ 🚪 99_Logout.py                     │                     │ 📈 16_Regression.py                 │
        │                                     │                     │ 🔮 17_KMeans.py                     │
        │                                     │                     │ 🌳 18_Agglomerative.py              │
        │                                     │                     │ ⚖️ 19_Cluster_Comparison.py         │
        │                                     │                     │ 🚀 20_Admin_Predictor.py            │
        │                                     │                     │ 📄 21_Reports.py                    │
        │                                     │                     │ ⚙️ 22_Settings.py                   │
        │                                     │                     │ 🚪 99_Logout.py                     │
        └──────────────────┬──────────────────┘                     └──────────────────┬──────────────────┘
                           │                                                           │
                           └─────────────────────────────┬─────────────────────────────┘
                                                         │
                                                         ▼
                                    ┌───────────────────────────────────────┐
                                    │          ANALYTICS BACKEND            │
                                    │            (src/ Modules)             │
                                    ├───────────────────────────────────────┤
                                    │ • src/preprocessing.py (Unified Cohort│
                                    │ • src/warehouse.py     (Star Schema)  │
                                    │ • src/olap.py          (2D Multi-Axis)│
                                    │ • src/classification.py (Supervised)  │
                                    │ • src/regression.py    (SLR / MLR)    │
                                    │ • src/clustering.py    (KMeans/Agglom)│
                                    │ • src/recommendations.py (Gap Engine) │
                                    │ • src/database.py      (Normalized DB)│
                                    └───────────────────┬───────────────────┘
                                                        │
                                                        ▼
                                    ┌───────────────────────────────────────┐
                                    │       PERSISTENCE & STORAGE           │
                                    ├───────────────────────────────────────┤
                                    │ 📂 data/placement_prediction_cleaned  │
                                    │ 🗄️ outputs/placement_dw.sqlite        │
                                    │ 📦 models/*.joblib (Fitted Pipelines) │
                                    │ 📝 outputs/*.csv (Audit Logs & Export)│
                                    └───────────────────────────────────────┘
```

---

## 📊 Kimball Star-Schema Data Warehouse Design

The core data warehouse (`outputs/placement_dw.sqlite`) implements a classic Kimball-style dimensional Star Schema, refreshed directly from the Unified Dataset Engine:

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

### Relational Table Definitions & Measures

| Table Name | Entity Type | Grain / Cardinality | Primary / Foreign Keys | Captured Features / Measures |
| :--- | :--- | :--- | :--- | :--- |
| `FactPlacement` | Fact Table | 1 record per student profile ($15,000+$ rows) | `fact_id` (PK), `student_key`, `academic_key`, `skill_key`, `engagement_key`, `placement_key` | Additive & semi-additive measures: `cgpa`, `attendance_pct`, `dsa_questions`, `aptitude_score`, `placed_flag` |
| `DimStudent` | Dimension | 1 row per unique student demographic | `student_key` (PK) | `age`, `gender`, `branch` |
| `DimAcademic` | Dimension | 1 row per academic standing combination | `academic_key` (PK) | `cgpa`, `backlogs`, `attendance_percentage` |
| `DimSkills` | Dimension | 1 row per skill competency profile | `skill_key` (PK) | `dsa_questions_solved`, `leetcode_questions_solved`, `hackerrank_questions_solved`, `coding_skill_score`, `aptitude_score`, `communication_score` |
| `DimEngagement`| Dimension | 1 row per student co-curricular record | `engagement_key` (PK) | `internships_count`, `projects_count`, `hackathons_count`, `github_repos`, `mock_interview_score` |
| `DimPlacement` | Dimension | 1 row per placement outcome state | `placement_key` (PK) | `placement_status`, `placement_prediction`, `placement_training` |

---

## 🧊 2D Dynamic OLAP Analytics Engine

PLACEMENT IQ features a fully interactive On-Line Analytical Processing (OLAP) engine supporting full multi-dimensional exploration across all student attributes:

```
              ┌────────────────────────────────────────────────────────┐
              │                   UNIVERSAL OLAP CUBE                  │
              │                                                        │
              │                 ┌───────────────────────┐              │
              │                 │   Branch × Gender     │              │
              │                 └───────────┬───────────┘              │
              │                             │                          │
              │       ┌─────────────────────┼─────────────────────┐    │
              │       ▼                     ▼                     ▼    │
              │ ┌───────────┐         ┌───────────┐         ┌───────────┐
              │ │   SLICE   │         │   DICE    │         │   PIVOT   │
              │ └───────────┘         └───────────┘         └───────────┘
              │       │                     │                     │    │
              │       └─────────────────────┼─────────────────────┘    │
              │                             │                          │
              │                             ▼                          │
              │             ┌───────────────────────────────┐          │
              │             │  2D SIMULTANEOUS ROLL-UP &   │          │
              │             │         DRILL-DOWN            │          │
              │             │  (Rows & Columns in 1 Click)  │          │
              │             └───────────────┬───────────────┘          │
              │                             │                          │
              │                             ▼                          │
              │             ┌───────────────────────────────┐          │
              │             │  SQLite Query Audit History   │          │
              │             │     (olap_query_history)      │          │
              │             └───────────────────────────────┘          │
              └────────────────────────────────────────────────────────┘
```

1. **Slice**: Isolates a single dimensional plane (e.g., `Branch = 'CSE'`) and displays instantaneous aggregations (Mean CGPA, Mean Attendance, Placement %).
2. **Dice**: Extracts a sub-cube by applying compound conjunctional predicates (e.g., `Branch IN ('CSE', 'IT') AND CGPA >= 7.5 AND Attendance >= 75%`).
3. **2D Simultaneous Roll-Up**: Aggregates both row hierarchies (e.g., `['Branch', 'Gender']` $\rightarrow$ `['Branch']`) and column dimensions (e.g., `['Placement Status', 'Training']` $\rightarrow$ `['Placement Status']`) simultaneously in one operation.
4. **2D Simultaneous Drill-Down**: De-aggregates parent row and column hierarchies into detailed multi-level sub-matrices simultaneously.
5. **Pivot**: Rotates dimensional axes (e.g., `Branch` across rows $\times$ `Placement Status` across columns) with interactive Plotly density heatmaps.
6. **Drill-Across**: Traverses foreign keys across `FactPlacement`, `DimStudent`, and `DimAcademic` to correlate disparate performance indicators.
7. **Query Audit History**: Every executed OLAP operation automatically registers dimensions, aggregation operators, execution timestamps, and row counts in the SQLite `olap_query_history` table.

---

## 👥 Dual-Persona Interactive Workspaces

The platform features 22 dedicated multi-page views separated by strict Role-Based Access Control (RBAC):

### 🎓 Student Career Workspace

| Page / Route | Core Capabilities & UI Workflow |
| :--- | :--- |
| **`pages/1_Student_Dashboard.py`** | **Placement Readiness Hub**: Displays real-time placement probability gauge, active production model name, key academic metrics, and readiness tier (High, Moderate, Action Needed). Gated for new users until onboarding profile is submitted. |
| **`pages/2_Student_Profile.py`** | **20-Dimensional Candidate Profile**: Interactive input form covering academics (CGPA, backlogs, attendance), coding metrics (DSA, LeetCode, HackerRank), engagement (internships, hackathons, projects, GitHub), and soft skills (communication, mock interview). |
| **`pages/3_Placement_Prediction.py`** | **Live ML Inference Engine**: Evaluates candidate profile in real time against the active production model. Outputs predicted class (`Placed` / `Not Placed`), probability confidence score, and top contributing factors. |
| **`pages/4_Skill_Analysis.py`** | **Multi-Dimensional Radar Benchmarking**: Overlays the student's 15 competency dimensions against the median profile of placed alumni from the 15,000-record baseline. |
| **`pages/5_Improvement_Plan.py`** | **Targeted Action Roadmap**: Quantifies exact deficits ($Gap = \text{Placed Median} - \text{Score}$), groups them into Critical, Moderate, and Strengths tiers, and provides personalized weekly improvement milestones. |
| **`pages/6_Prediction_History.py`** | **Timeline & Advisory Log**: Interactive chronologically ordered history of all past predictions, model versions, and administrative advisory notes dispatched by faculty mentors. |

### 🛡️ Administrator Intelligence Center

| Page / Route | Core Capabilities & UI Workflow |
| :--- | :--- |
| **`pages/10_Admin_Dashboard.py`** | **Executive Overview**: High-level institutional KPIs (total cohort, placement rate, average CGPA, active backlogs). Features the **Unified Dataset Switcher** (Base 15,000 vs. Live Unified $15,000 + N$). |
| **`pages/11_Student_Data.py`** | **Candidate Directory & Audit Workbench**: Searchable, filterable directory of all registered students with profile audits, risk status, and a one-click **Feedback Dispatcher** to send advisory guidance to student dashboards. |
| **`pages/12_Data_Warehouse.py`** | **Kimball Star-Schema Console**: Visual ER diagram explorer for `FactPlacement` and dimension tables with an embedded, live **ANSI SQL Query Workbench**. |
| **`pages/13_OLAP.py`** | **Universal Dynamic OLAP Builder**: Interactive execution of Slice, Dice, 2D Simultaneous Roll-Up & Drill-Down, Pivot heatmaps, Drill-Across, and query execution audit logs. |
| **`pages/14_Data_Mining.py`** | **Correlation & Feature Discovery**: Pearson correlation matrix, Mutual Information gain rankings, Gini feature importance bar charts, and Apriori association rule extraction. |
| **`pages/15_Classification.py`** | **Supervised Classification Suite**: Trains and benchmarks Random Forest, CART Decision Tree, and Gaussian Naive Bayes with 5-fold cross-validation, confusion matrices, ROC-AUC, and precision-recall curves. |
| **`pages/16_Regression.py`** | **Continuous Numerical Regression**: Fits Simple Linear Regression (SLR) and Multiple Linear Regression (MLR) on continuous competencies (`aptitude_score`, `coding_skill_score`, `cgpa`) with residual normality tests. |
| **`pages/17_KMeans.py`** | **K-Means Clustering Suite**: Automated WCSS Elbow curve analysis ($K=2$ to $10$), Silhouette score optimization, 2D PCA cluster projection, and cluster centroid radar geometry. |
| **`pages/18_Agglomerative.py`** | **Hierarchical Clustering**: Agglomerative clustering with Ward, Complete, and Average linkages, accompanied by interactive Scipy / Plotly dendrograms. |
| **`pages/19_Cluster_Comparison.py`**| **Clustering Benchmark Engine**: Side-by-side comparison of K-Means vs. Agglomerative clustering across silhouette coefficients, cluster geometries, and computational runtime. |
| **`pages/20_Admin_Predictor.py`** | **Batch Prediction Engine**: High-throughput candidate inference supporting single candidate scoring and bulk CSV uploads with one-click export of scored candidates. |
| **`pages/21_Reports.py`** | **Institutional Report Generator**: Generates comprehensive institutional health reports, executive summaries, and CSV data downloads for academic accreditation. |
| **`pages/22_Settings.py`** | **System Governance & Configuration**: One-click **Active Production Model Selector** (updates student inference endpoints) and DWH database rebuild utilities. |

---

## 🧠 Machine Learning & Data Mining Suite

```
                                  ┌──────────────────────────────────────────────┐
                                  │       DATA MINING & MACHINE LEARNING         │
                                  └──────────────────────┬───────────────────────┘
                                                         │
             ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
             ▼                                           ▼                                           ▼
┌───────────────────────────┐               ┌───────────────────────────┐               ┌───────────────────────────┐
│ SUPERVISED CLASSIFICATION │               │   CONTINUOUS REGRESSION   │               │  UNSUPERVISED CLUSTERING  │
├───────────────────────────┤               ├───────────────────────────┤               ├───────────────────────────┤
│ • Random Forest (Ensemble)│               │ • Simple Linear (SLR)     │               │ • K-Means (Elbow K=2..10) │
│ • Decision Tree (CART)    │               │ • Multiple Linear (MLR)   │               │ • Agglomerative (Ward/Avg)│
│ • Gaussian Naive Bayes    │               │ • Residual Normal Diagnostics│           │ • 2D PCA Projections      │
│ • 5-Fold Stratified CV    │               │ • R², MSE, RMSE, MAE      │               │ • Silhouette Optimization │
│ • 1-Click Prod Switcher   │               │ • Continuous Score Forecast│              │ • Side-by-Side Benchmark  │
└───────────────────────────┘               └───────────────────────────┘               └───────────────────────────┘
```

### 1. Supervised Classification
- **Algorithms**: Random Forest (Ensemble Bagging), Decision Tree (CART), Gaussian Naive Bayes.
- **Hyperparameter Controls**: Splitting criterion (Gini/Entropy), max tree depth, min samples split, number of estimators, and variance smoothing.
- **Evaluation Framework**: 5-Fold Stratified Cross-Validation, Confusion Matrices, ROC-AUC Curves, Precision-Recall Curves, and Gini Feature Importance rankings.
- **Production Deployment**: Administrators designate the active model in one click (`outputs/placement_dw.sqlite` $\rightarrow$ `system_settings`), instantly updating the student inference engine.

### 2. Continuous Numerical Regression
- **Predictive Targets**: `aptitude_score`, `coding_skill_score`, `cgpa`, `mock_interview_score`.
- **Algorithms**: Simple Linear Regression (SLR) and Multiple Linear Regression (MLR).
- **Statistical Metrics**: Coefficient of Determination ($R^2$), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and residual distribution normality plots.

### 3. Unsupervised Clustering & Cohort Segmentation
- **K-Means Clustering**: WCSS Elbow Method analysis ($K=2$ to $10$), Silhouette score optimization, cluster centroid radar geometry, and 2D PCA projection scatter.
- **Agglomerative Hierarchical**: Ward, Complete, and Average linkage criteria with interactive Scipy/Plotly Dendrogram trees.
- **Cluster Benchmarking**: Direct side-by-side comparison of partition geometries, silhouette coefficients, and computational runtime.

### 4. Data Mining & Association Rules
- **Correlation Analysis**: Full 16-variable Pearson correlation matrix with heatmaps.
- **Mutual Information Gain**: Non-linear feature dependency rankings against placement outcome.
- **Apriori Association Rules**: Frequent itemset mining discovering combinatorial rules (e.g., `High DSA` $\wedge$ `Internship >= 1` $\Rightarrow$ `Placement = True`).

---

## 📐 Mathematical Rigor & Formulations

### 1. Skill Gap Recommendation Formulation
For any student competency vector $\mathbf{x} = [x_1, x_2, \dots, x_m]$ and the corresponding median vector of placed alumni $\mathbf{M}^{(\text{placed})} = [M_1, M_2, \dots, M_m]$:

$$\text{Deficit}_i = \max\left(0, M_i^{(\text{placed})} - x_i\right)$$

$$\text{Deficit Percentage}_i = \left( \frac{\text{Deficit}_i}{M_i^{(\text{placed})}} \right) \times 100\%$$

- **Critical Priority**: $\text{Deficit Percentage}_i \ge 35\%$
- **Moderate Priority**: $10\% \le \text{Deficit Percentage}_i < 35\%$
- **Strength**: $\text{Deficit Percentage}_i < 10\%$ (or $x_i \ge M_i$)

### 2. Empirical Regression Models (Fitted on Placement Dataset)
- **Simple Linear Regression (SLR)**:
  $$\widehat{\text{aptitude}} = 6.2035 \times \text{CGPA} + 14.6948$$

- **Multiple Linear Regression (MLR)**:
  $$\widehat{\text{aptitude}} = -0.049 \cdot \text{Age} + 4.214 \cdot \text{CGPA} - 0.004 \cdot \text{Backlogs} + \dots + 12.249$$

### 3. Classification & Decision Trees
- **Gini Impurity**:
  $$I_G(p) = 1 - \sum_{i=1}^J p_i^2$$

- **Gaussian Naive Bayes Posterior Probability**:
  $$P(C_k \mid \mathbf{x}) \propto P(C_k) \prod_{j=1}^D \frac{1}{\sqrt{2\pi \sigma_{kj}^2}} \exp\left( -\frac{(x_j - \mu_{kj})^2}{2\sigma_{kj}^2} \right)$$

### 4. Clustering Optimization
- **Within-Cluster Sum of Squares (WCSS / Inertia)**:
  $$\text{WCSS} = \sum_{k=1}^K \sum_{\mathbf{x} \in S_k} \|\mathbf{x} - \boldsymbol{\mu}_k\|^2$$

- **Silhouette Coefficient**:
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]$$
  where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance.

---

## 📈 Validated Benchmarks & Empirical Audit

*Empirical metrics extracted directly from the system validation engine ([`TEST_REPORT.md`](TEST_REPORT.md))*:

### Supervised Classification Benchmarks (15,000 Records)

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Ensemble)** | **81.52%** | **0.7456** | **0.8112** | **0.7770** | **0.8936** | 2.939s |
| **Gaussian Naive Bayes** | 80.95% | 0.7558 | 0.7685 | 0.7621 | 0.8875 | **0.059s** |
| **Decision Tree (CART)** | 77.52% | 0.6996 | 0.7601 | 0.7286 | 0.8547 | 0.137s |

### Continuous Numerical Regression (Target: `aptitude_score`)

| Regression Model | $R^2$ Score | MSE | RMSE | MAE | Mathematical Equation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Multiple Linear Regression (MLR)** | **0.4052** | **77.757** | **8.818** | **7.057** | $y = (-0.049 \times \text{age}) + (4.214 \times \text{cgpa}) + \dots + 12.249$ |
| **Simple Linear Regression (SLR)** | 0.2158 | 102.518 | 10.125 | 8.047 | $y = (6.2035 \times \text{cgpa}) + 14.6948$ |

### Unsupervised Clustering Benchmarks ($K=4$)

| Clustering Model | Silhouette Score | Fitting Time | Feature Dimensions Analyzed |
| :--- | :---: | :---: | :--- |
| **K-Means Clustering** | **0.0762** | 0.417s | 15 numeric competency dimensions |
| **Agglomerative Hierarchical** | 0.0732 | **0.081s** | 15 numeric competency dimensions ($n=1,000$ sample) |

---

## 🔐 Authentication & Demo Credentials

Authentication uses **PBKDF2 HMAC SHA-256** with random per-user salts across 100,000 hashing rounds. User roles are resolved automatically from the SQLite database upon login.

| Portal Role | Registered Email | Password | Pre-loaded Context / Demonstration Purpose |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@college.com` | `admin123` | **Prof. K. Sharma**: DWM Lead; full executive dashboard, SQL workbench, model switcher. |
| **Administrator** | `placement@college.com` | `placement123` | **Dean D. Joshi**: TPO Lead; candidate directory, batch scoring, institutional report export. |
| **Student (Placed)** | `student@college.com` | `student123` | **Rohan Verma**: CSE, CGPA 8.74, 380 DSA solved; high placement readiness demo. |
| **Student (Action Needed)**| `vikram.m@campus.edu` | `student123` | **Vikram Malhotra**: Mech, CGPA 6.10, backlogs; demonstrates deficit gap engine & roadmap. |
| **New Student** | *Use "Create Account"* | *Any (4+ chars)* | **Empty onboarding state**: demonstrates zero pre-filled mock data and onboarding gate. |

---

## 🚀 Quickstart & Installation Guide

### Prerequisites
- **Python**: 3.10, 3.11, or 3.12 installed
- **Operating System**: Windows 10/11, macOS, or Linux

### 1. Clone the Repository
```bash
git clone https://github.com/Sarthzz01/PLACEMENT_IQ.git
cd PLACEMENT_IQ
```

### 2. Set Up a Virtual Environment
```bash
# Windows (PowerShell or CMD)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install Python backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install Frontend dependencies
cd frontend
npm install
cd ..
```

### 4. Run Automated Platform Validation (Optional but Recommended)
Validate dataset integrity, Star Schema reconstruction, regression, classification, and OLAP suites:
```bash
python backend/validate_project.py
```
> **Expected Output**: `ALL 13 AUTOMATED TEST SUITES PASSED SUCCESSFULLY (13/13)!`

### 5. Launch the Full-Stack Application
To start both backend and frontend together:
- **Windows 1-Click**: Double-click [`start_all.bat`](start_all.bat)
- **Manual Launch**:
  ```bash
  # Terminal 1: FastAPI Backend
  cd backend
  python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000

  # Terminal 2: React Frontend
  cd frontend
  npm run dev
  ```

- Access the **React Web Application** at: `http://localhost:5173`
- Access the **FastAPI Swagger API Documentation** at: `http://127.0.0.1:8000/docs`

---

## 🧪 13-Suite Automated Quality Assurance

The platform includes an automated testing framework ([`validate_project.py`](validate_project.py)) that executes 13 distinct verification suites:

| Suite | Component Tested | Verification Scope & Assertions | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Dataset Integrity** | Validates exact 15,000 rows, 26 expected columns, 0 null values, 0 duplicate rows | **PASS** |
| **2** | **Database Schema** | Asserts SQLite normalized tables (`users`, `student_profiles`, `student_predictions`, `admin_feedback`) | **PASS** |
| **3** | **Security & Auth** | PBKDF2 HMAC-SHA256 password hashing roundtrip, student role enforcement, admin privileges | **PASS** |
| **4** | **Unified Engine** | Merges 15,000 baseline records with dynamic SQLite profiles into unified cohort ($15,000 + N$) | **PASS** |
| **5** | **Classification** | Trains Decision Tree, Random Forest, Naive Bayes; verifies safe numeric subset formatting | **PASS** |
| **6** | **Regression** | Fits SLR & MLR on continuous targets (`aptitude_score`); asserts $R^2$, RMSE, MSE, equations | **PASS** |
| **7** | **Clustering** | Executes K-Means (Elbow $K=2..5$) and Agglomerative Hierarchical ($n=1,000$ dendrogram) | **PASS** |
| **8** | **Data Mining** | Computes Pearson correlation matrix, mutual information gain, Gini feature importance | **PASS** |
| **9** | **Star Schema DWH** | Rebuilds SQLite `FactPlacement` ($15,000+$ rows) and 5 relational dimension tables | **PASS** |
| **10**| **Dynamic OLAP** | Verifies Slice, Dice, Pivot, Drill-Across, 2D Simultaneous Roll-Up & Drill-Down, Query Audit | **PASS** |
| **11**| **Recommendation** | Computes mathematical gaps vs. placed cohort medians; verifies readiness categorization | **PASS** |
| **12**| **Batch Scoring** | Validates high-throughput candidate scoring and probability confidence export | **PASS** |
| **13**| **Feedback Loop** | Dispatches administrative assessments and alerts to Student Dashboard | **PASS** |

---

## 📂 Repository Directory Anatomy

```
PLACEMENT_IQ/
├── backend/                       # Python Backend, API Engine & ML Analytics
│   ├── api.py                    # FastAPI REST server for React frontend
│   ├── main.py                   # Alternative entry point for Uvicorn
│   ├── requirements.txt          # Python dependencies (FastAPI, Scikit-learn, etc.)
│   ├── validate_project.py       # 13-suite automated test engine
│   ├── run_api.bat               # 1-Click launcher for FastAPI server (Port 8000)
│   ├── data/
│   │   └── placement_prediction_cleaned.csv  # 15,000 records dataset
│   ├── models/                   # Persisted scikit-learn models (.joblib)
│   │   ├── random_forest.joblib
│   │   ├── decision_tree.joblib
│   │   ├── naive_bayes.joblib
│   │   ├── kmeans.joblib
│   │   ├── slr.joblib
│   │   └── mlr.joblib
│   ├── outputs/                  # SQLite database & analytical exports
│   │   ├── placement_dw.sqlite   # Star-Schema SQLite database
│   │   ├── classification_metrics.csv
│   │   ├── regression_metrics.csv
│   │   ├── kmeans_cluster_profiles.csv
│   │   └── student_submissions.csv
│   └── src/                      # Core backend Python modules
│       ├── auth.py               # Authentication & PBKDF2 hashing
│       ├── classification.py     # Supervised classification suite
│       ├── clustering.py         # K-Means & Agglomerative clustering
│       ├── config.py             # Feature definitions & paths
│       ├── database.py           # SQLite persistence layer
│       ├── data_mining.py        # Correlations, MI, Apriori rules
│       ├── olap.py               # Multi-dimensional OLAP cubes
│       ├── prediction.py         # Real-time placement inference
│       ├── preprocessing.py      # Data cleaning & validation
│       ├── recommendations.py    # Student improvement roadmap
│       ├── regression.py         # Linear & polynomial regression
│       ├── submissions.py        # Student submission parsing
│       ├── visualizations.py     # Plotly & Matplotlib charts
│       └── warehouse.py          # Kimball star-schema builder
│
├── frontend/                      # Modern React + Vite Single-Page Application
│   ├── src/
│   │   ├── components/           # TopHeader, Sidebar, Navigation
│   │   ├── pages/
│   │   │   ├── admin/            # Admin analytics, OLAP, DWH, ML pages
│   │   │   ├── student/          # Student portal, prediction, skills
│   │   │   ├── HomePage.jsx      # Public landing page
│   │   │   └── LoginPage.jsx     # Authentication & registration
│   │   ├── App.jsx               # Application router & theme
│   │   └── index.css             # Glassmorphism styling & tokens
│   ├── package.json              # Frontend scripts & dependencies
│   └── vite.config.js            # Vite proxy configuration (/api -> :8000)
│
├── docs/                          # Architectural documentation & project report
├── run_backend.bat                # Root 1-click launcher for FastAPI backend
├── run_frontend.bat               # Root 1-click launcher for React frontend
├── start_all.bat                  # Root 1-click launcher to run full stack
├── README.md                      # Comprehensive manual & docs
└── TEST_REPORT.md                 # System validation & benchmark report
```

---

## 🛡️ Security, Privacy & Data Governance

1. **Password Protection**: Passwords are never stored in plaintext. Passwords utilize standard `PBKDF2 HMAC SHA-256` hashing with cryptographically secure random per-user salts and 100,000 hashing rounds.
2. **Role-Based Access Control (RBAC)**: Student accounts are restricted to their individual profile, predictions, radar benchmarks, and improvement roadmaps. Administrative portals (`pages/10_*.py` through `pages/22_*.py`) require verified administrative email credentials (`src/config.py`).
3. **Empty Gating for New Candidates**: To uphold data integrity and eliminate deceptive mock data, new student accounts start completely empty (`is_completed = 0`). No fabricated placement predictions, scores, or charts are displayed until the student actively submits their verified 20-parameter profile.
4. **OLAP Query Auditing**: Every dimensional OLAP operation logs the requesting session, operation type, dimensions analyzed, aggregation functions, and timestamp to `olap_query_history`.

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>1. How does the Unified Dataset differ from the raw CSV?</b></summary>
The raw CSV (`placement_prediction_cleaned.csv`) contains 15,000 historical student records used as the empirical benchmark. The Unified Dataset dynamically joins these 15,000 records with newly registered candidate profiles stored in SQLite (`student_profiles`), normalizing column types on the fly. Administrators can toggle between analyzing the pure baseline (15,000) or the combined live cohort ($15,000 + N$) from the Admin Executive Dashboard.
</details>

<details>
<summary><b>2. How is the active machine learning model switched?</b></summary>
Admins can visit <b>Machine Learning Suite ➔ Classification Suite</b> or <b>Settings</b> and select between Random Forest, Decision Tree, and Naive Bayes with a single click. The setting is persisted in SQLite (`system_settings`), instantly updating the prediction engine for all student portals.
</details>

<details>
<summary><b>3. What happens if I encounter a port conflict on 8000 or 5173?</b></summary>
Run the backend or frontend on alternative ports:
```bash
# FastAPI Backend
python -m uvicorn api:app --port 8001

# React Frontend
npm run dev -- --port 5174
```
</details>

<details>
<summary><b>4. How do I reset or rebuild the SQLite database from scratch?</b></summary>
You can rebuild the database by running `python validate_project.py` or clicking <b>"Rebuild Data Warehouse"</b> in <b>System Settings (Page 22)</b>.
</details>

---

## 📜 Academic Attribution & License

- **Project**: Student Placement Analytics & Intelligence Platform (PLACEMENT IQ)
- **Domain**: Data Warehousing & Data Mining (DWM)
- **Dataset Reference**: 15,000 Certified University Placement Records (`placement_prediction_cleaned.csv`)
- **License**: MIT Academic License — open for institutional research, teaching, and academic evaluation.

```
Copyright (c) 2026 PLACEMENT IQ Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

[⬆ Back to Top](#-placement-iq-student-placement-intelligence--data-warehousing-platform)
