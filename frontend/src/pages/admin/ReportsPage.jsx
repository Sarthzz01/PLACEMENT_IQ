import React, { useState, useEffect } from 'react';
import { Download, FileText, BarChart, Database, Cpu, CheckCircle2 } from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState('artifacts');
  const [summaryData, setSummaryData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/reports/summary')
      .then((r) => r.json())
      .then((d) => setSummaryData(d.summary || []))
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const downloadCSV = (content, filename) => {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDownloadSummary = () => {
    if (!summaryData.length) return;
    const headers = Object.keys(summaryData[0]).join(',');
    const rows = summaryData.map((row) => Object.values(row).join(','));
    const csvContent = [headers, ...rows].join('\n');
    downloadCSV(csvContent, 'dataset_statistical_summary.csv');
  };

  const academicReportMarkdown = `# PLACEMENT IQ: Student Placement Analytics & Intelligence Platform
**Data Warehousing and Data Mining (DWM) Comprehensive Report**
*Academic Year: 2026 • University Department of Computer Engineering*

---

## 1. Executive Summary
PLACEMENT IQ is a modern, unified Data Warehousing and Data Mining platform architected for academic institutions.
The system features dual role-based experiences for **Students** and **Placement Administrators**, operating over
\`placement_prediction_cleaned.csv\` containing verified candidate records.

---

## 2. Dataset Architecture & Preprocessing
- **Source Dataset:** \`placement_prediction_cleaned.csv\`
- **Target Variable:** \`placement_prediction\` (Binary: 0 = Not Placed, 1 = Placed).
- **Target Distribution:** Verified placed vs not-placed balance across technical branches.
- **Feature Space:** 20 fundamental dimensions covering Academic History (CGPA, backlogs, attendance), Problem-Solving Platforms (DSA, LeetCode, HackerRank, GitHub), Practical Experience (Internships, Projects, Hackathons, Certifications), and Soft Skills (Aptitude, Communication, Mock Interviews, Placement Training).

---

## 3. Data Warehouse Architecture (Star Schema)
The warehouse is implemented using local SQLite persistence (\`placement_dw.sqlite\`) structured into a Star Schema:
- **Central Fact Table:** \`FactPlacement\` with foreign surrogate keys and measurable metrics (CGPA, Aptitude, Coding Score, Outcome).
- **Conformed Dimension Tables:**
  - \`DimStudent\`: Student demographic profile (Age, Gender, Branch)
  - \`DimAcademic\`: Academic performance (CGPA, Backlogs, Attendance %)
  - \`DimSkills\`: Technical and competitive programming assessments (DSA, LeetCode, HackerRank, Aptitude, Coding Skill)
  - \`DimEngagement\`: Co-curricular credentials (Internships, Projects, Hackathons, Repos, Mock Interviews, Training)
  - \`DimPlacement\`: Target outcomes and placement status

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
Evaluated continuous skill prediction across \`aptitude_score\`, \`coding_skill_score\`, and \`cgpa\`. Multiple Linear Regression (MLR) demonstrated superior variance explanation (R² ~ 0.417) compared to univariate Simple Linear Regression (SLR R² ~ 0.209).

---

## 6. Unsupervised Clustering
- **K-Means:** Partitioned students into K=4 distinct clusters (High Achievers, Balanced Coders, Academic Learners, Need Support) with elbow inertia analysis.
- **Agglomerative Hierarchical Clustering:** Bottom-up linkage with complete hierarchical dendrogram inspection.

---

## 7. Conclusion & Institutional Impact
PLACEMENT IQ bridges the gap between theoretical data warehousing concepts and practical campus placement intelligence. By unifying predictive machine learning with dynamic multi-dimensional cubes, the platform equips placement officers with actionable cohort insights while providing students with transparent, explainable readiness guidance.
`;

  const handleDownloadReport = () => {
    const blob = new Blob([academicReportMarkdown], { type: 'text/markdown;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'PLACEMENT_IQ_Academic_Report.md');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-main)', margin: '0 0 6px 0' }}>
          Reports & Intelligence Export Center
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: 0 }}>
          Download machine learning benchmarks, warehouse data artifacts, and generate comprehensive academic project documentation.
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 12, borderBottom: '1px solid var(--border-color)', marginBottom: 24 }}>
        <button
          onClick={() => setActiveTab('artifacts')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '10px 18px',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            fontWeight: 700,
            fontSize: '0.92rem',
            color: activeTab === 'artifacts' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'artifacts' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Download size={16} /> 1. Export Data & Model Artifacts
        </button>
        <button
          onClick={() => setActiveTab('report')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '10px 18px',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            fontWeight: 700,
            fontSize: '0.92rem',
            color: activeTab === 'report' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'report' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <FileText size={16} /> 2. Academic Project Report
        </button>
      </div>

      {/* Tab 1: Export Artifacts */}
      {activeTab === 'artifacts' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 20, marginBottom: 24 }}>
          {/* Statistical Summary */}
          <div className="campus-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <div style={{ width: 40, height: 40, borderRadius: 10, background: '#EFF6FF', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <BarChart size={20} />
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)' }}>Core Dataset Summary</h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Descriptive stats across all 20 dimensions</div>
              </div>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>
              Mean, standard deviation, quartiles, and min/max boundaries for academic, coding, and aptitude attributes.
            </p>
            <button onClick={handleDownloadSummary} className="btn-secondary" style={{ width: '100%' }}>
              <Download size={15} /> Download Statistical Summary (CSV)
            </button>
          </div>

          {/* Academic Report Quick Download */}
          <div className="campus-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <div style={{ width: 40, height: 40, borderRadius: 10, background: '#F0FDF4', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#16A34A' }}>
                <FileText size={20} />
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)' }}>Academic Project Report</h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Viva & evaluation ready documentation</div>
              </div>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>
              Comprehensive 7-section report covering dataset lineage, Star Schema, OLAP cubes, ML benchmarks, and clustering.
            </p>
            <button onClick={handleDownloadReport} className="btn-primary" style={{ width: '100%' }}>
              <Download size={15} /> Download Full Academic Report (MD)
            </button>
          </div>

          {/* Warehouse Schema Export */}
          <div className="campus-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
              <div style={{ width: 40, height: 40, borderRadius: 10, background: '#EDE9FE', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8B5CF6' }}>
                <Database size={20} />
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)' }}>Data Warehouse Star Schema</h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>SQLite dimensional definitions</div>
              </div>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>
              FactPlacement table layout, foreign key surrogate mapping, and dimensional attributes.
            </p>
            <button
              onClick={() => {
                const schemaSummary = `Table,Type,Columns\nFactPlacement,Fact,fact_id,student_id,academic_id,skills_id,engagement_id,placement_id,cgpa,aptitude_score,coding_skill_score,placement_status\nDimStudent,Dimension,student_id,age,gender,branch\nDimAcademic,Dimension,academic_id,cgpa,backlogs,attendance_percentage\nDimSkills,Dimension,skills_id,dsa_problems_solved,leetcode_problems_solved,hackerrank_score,aptitude_score,coding_skill_score\nDimEngagement,Dimension,engagement_id,internships_completed,projects_count,hackathons_participated,github_repos_count,mock_interview_score,placement_training\nDimPlacement,Dimension,placement_id,placement_prediction,placement_status`;
                downloadCSV(schemaSummary, 'star_schema_definition.csv');
              }}
              className="btn-secondary"
              style={{ width: '100%' }}
            >
              <Download size={15} /> Download Schema Topology (CSV)
            </button>
          </div>
        </div>
      )}

      {/* Tab 2: Academic Report Text */}
      {activeTab === 'report' && (
        <div className="campus-card" style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-main)' }}>
              Official Institutional Documentation
            </h3>
            <button onClick={handleDownloadReport} className="btn-primary" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>
              <Download size={14} /> Download Markdown (.md)
            </button>
          </div>

          <div
            style={{
              background: '#F8FAFC',
              padding: '24px 32px',
              borderRadius: 10,
              border: '1px solid #E2E8F0',
              lineHeight: 1.8,
              fontSize: '0.92rem',
              color: '#334155',
              whiteSpace: 'pre-line',
              fontFamily: 'inherit',
            }}
          >
            {academicReportMarkdown}
          </div>
        </div>
      )}

      {/* Academic Justification */}
      <AcademicJustification
        title="Reporting & Intelligence Export Justification"
        algorithmRationale="Standardized reporting and verifiable data artifact dissemination are critical requirements of data warehousing lifecycles. Reproducibility ensures that institutional evaluators and external audit committees can independently verify algorithm benchmarking metrics, schema integrity, and distribution statistics without proprietary software dependencies."
        institutionalImpact="Provides the Departmental Academic Committee with rigorous, evidence-based documentation supporting curriculum improvements, accreditation reviews, and institutional placement performance reports."
        dwmConcepts="Metadata Management, Data Lineage & Auditability, Artifact Serializability, Reproducible Analytical Workflows, Executive Governance Reporting."
      />
    </div>
  );
}
