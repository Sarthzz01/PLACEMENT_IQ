import React, { useState, useEffect } from 'react';
import {
  Target, Users, User, Upload, CheckCircle2, AlertTriangle, ArrowRight,
  Save, Download, Cpu, Layers, Sparkles, TrendingUp, Shield, GitBranch,
  Award, Zap, Search, Filter, RefreshCw, Check, FileSpreadsheet, Activity,
  Sliders, ThumbsUp, AlertCircle
} from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

const MODEL_OPTIONS = [
  { value: 'Random Forest', label: 'Random Forest', sub: 'Ensemble Bagging (150 trees)', acc: '~86.5%', badge: 'Ensemble' },
  { value: 'Gradient Boosting', label: 'Gradient Boosting', sub: 'Sequential Error-Correcting', acc: '~85.2%', badge: 'Boosting' },
  { value: 'Decision Tree', label: 'Decision Tree', sub: 'White-Box Splitting Rules', acc: '~81.4%', badge: 'Rules' },
  { value: 'Logistic Regression', label: 'Logistic Regression', sub: 'L2 Log-Odds Sigmoid', acc: '~82.0%', badge: 'Linear' },
  { value: 'Naive Bayes', label: 'Gaussian Naive Bayes', sub: 'Class-Conditional Probability', acc: '~80.9%', badge: 'Bayesian' }
];

const renderStrengthText = (s) => {
  if (!s) return '';
  if (typeof s === 'string') return s;
  return s.title || s.detail || s.feature || 'Strong Skill Profile';
};

const renderImprovementText = (imp) => {
  if (!imp) return '';
  if (typeof imp === 'string') return imp;
  if (imp.title) {
    return imp.advice ? `${imp.title}: ${imp.advice}` : imp.title;
  }
  return imp.advice || imp.feature || 'Improvement Required';
};

export default function PredictionCenter({ user }) {
  const [activeTab, setActiveTab] = useState('registered'); // 'registered' | 'adhoc' | 'consensus' | 'batch'
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [branchFilter, setBranchFilter] = useState('ALL');
  const [selectedStudentEmail, setSelectedStudentEmail] = useState('');
  const [modelChoice, setModelChoice] = useState('Gradient Boosting');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [systemSettingModel, setSystemSettingModel] = useState('Random Forest');

  // Registered Student Inference Result
  const [registeredResult, setRegisteredResult] = useState(null);
  const [feedbackStatus, setFeedbackStatus] = useState('High Potential');
  const [feedbackNotes, setFeedbackNotes] = useState('');
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);
  const [savingFeedback, setSavingFeedback] = useState(false);

  // Multi-Model Consensus State
  const [consensusData, setConsensusData] = useState(null);
  const [comparing, setComparing] = useState(false);

  // Ad-Hoc Simulator Form
  const [adHocForm, setAdHocForm] = useState({
    name: 'External Candidate',
    gender: 'Male',
    branch: 'CSE',
    cgpa: 8.4,
    backlogs: 0,
    attendance_percentage: 88,
    dsa_problems_solved: 240,
    leetcode_problems_solved: 160,
    hackerrank_score: 820,
    aptitude_score: 85,
    coding_skill_score: 8.5,
    internships_completed: 1,
    projects_count: 3,
    hackathons_participated: 2,
    github_repos_count: 5,
    mock_interview_score: 80,
    placement_training: 'Yes'
  });
  const [adHocResult, setAdHocResult] = useState(null);

  // Batch CSV Scoring State
  const [batchFile, setBatchFile] = useState(null);
  const [batchResult, setBatchResult] = useState(null);
  const [batchSearchTerm, setBatchSearchTerm] = useState('');

  // Fetch initial student roster and active settings
  useEffect(() => {
    fetch('/api/admin/students')
      .then((r) => r.json())
      .then((d) => {
        const list = d.students || [];
        setStudents(list);
        if (list.length > 0 && !selectedStudentEmail) {
          setSelectedStudentEmail(list[0].email);
        }
      })
      .catch((e) => console.error(e));

    fetch('/api/admin/settings')
      .then((r) => r.json())
      .then((d) => {
        if (d.production_model) {
          setSystemSettingModel(d.production_model);
          setModelChoice(d.production_model);
        }
      })
      .catch((e) => console.error(e));
  }, []);

  // Filter students by search term and branch
  const filteredStudents = students.filter((s) => {
    const matchesSearch =
      (s.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (s.email || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (s.student_id || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesBranch = branchFilter === 'ALL' || (s.branch || '').toUpperCase() === branchFilter.toUpperCase();
    return matchesSearch && matchesBranch;
  });

  const selectedStudent = students.find((s) => s.email === selectedStudentEmail) || students[0];

  // Run single prediction on registered student
  const handleRunRegisteredPredict = async () => {
    if (!selectedStudent) return;
    setLoading(true);
    setErrorMsg(null);
    setFeedbackSuccess(false);
    try {
      const res = await fetch('/api/admin/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: selectedStudent.email,
          data: selectedStudent,
          model_name: modelChoice,
        }),
      });
      if (!res.ok) {
        throw new Error(`Inference API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setRegisteredResult(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Failed to evaluate candidate placement readiness.');
    } finally {
      setLoading(false);
    }
  };

  // Run consensus across all 5 models for registered student
  const handleRunConsensus = async (customCandidate = null) => {
    const candidateData = customCandidate || selectedStudent;
    if (!candidateData) return;
    setComparing(true);
    setErrorMsg(null);
    try {
      const res = await fetch('/api/admin/predict/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: candidateData }),
      });
      if (!res.ok) {
        throw new Error(`Consensus API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setConsensusData(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Failed to compare all 5 models.');
    } finally {
      setComparing(false);
    }
  };

  // Save Faculty Advisory Feedback
  const handleSaveFeedback = async (e) => {
    e.preventDefault();
    if (!selectedStudent?.email) return;
    setSavingFeedback(true);
    try {
      await fetch('/api/admin/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_email: selectedStudent.email,
          admin_name: user?.name || 'Prof. Shruti Agrawal',
          status: feedbackStatus,
          notes: feedbackNotes,
        }),
      });
      setFeedbackSuccess(true);
      setFeedbackNotes('');
    } catch (err) {
      console.error(err);
    } finally {
      setSavingFeedback(false);
    }
  };

  // Ad-Hoc candidate preset loader
  const applyPreset = (presetType) => {
    if (presetType === 'high') {
      setAdHocForm({
        name: 'Pooja Kulkarni (High Achiever)',
        gender: 'Female',
        branch: 'CSE',
        cgpa: 9.35,
        backlogs: 0,
        attendance_percentage: 94,
        dsa_problems_solved: 380,
        leetcode_problems_solved: 280,
        hackerrank_score: 890,
        aptitude_score: 92,
        coding_skill_score: 9.0,
        internships_completed: 2,
        projects_count: 4,
        hackathons_participated: 3,
        github_repos_count: 12,
        mock_interview_score: 88,
        placement_training: 'Yes'
      });
    } else if (presetType === 'average') {
      setAdHocForm({
        name: 'Kunal Sharma (Average Candidate)',
        gender: 'Male',
        branch: 'IT',
        cgpa: 7.72,
        backlogs: 0,
        attendance_percentage: 82,
        dsa_problems_solved: 160,
        leetcode_problems_solved: 95,
        hackerrank_score: 550,
        aptitude_score: 68,
        coding_skill_score: 6.8,
        internships_completed: 1,
        projects_count: 2,
        hackathons_participated: 1,
        github_repos_count: 6,
        mock_interview_score: 70,
        placement_training: 'Yes'
      });
    } else if (presetType === 'atrisk') {
      setAdHocForm({
        name: 'Arjun Verma (At-Risk Profile)',
        gender: 'Male',
        branch: 'Mechanical',
        cgpa: 6.15,
        backlogs: 2,
        attendance_percentage: 64,
        dsa_problems_solved: 25,
        leetcode_problems_solved: 15,
        hackerrank_score: 180,
        aptitude_score: 48,
        coding_skill_score: 4.2,
        internships_completed: 0,
        projects_count: 1,
        hackathons_participated: 0,
        github_repos_count: 2,
        mock_interview_score: 45,
        placement_training: 'No'
      });
    }
  };

  // Run Ad-Hoc candidate prediction
  const handleRunAdHocPredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch('/api/admin/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: adHocForm,
          model_name: modelChoice,
        }),
      });
      if (!res.ok) {
        throw new Error(`Inference API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setAdHocResult(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Failed to evaluate ad-hoc candidate.');
    } finally {
      setLoading(false);
    }
  };

  // High-Throughput Batch Scoring via CSV Upload
  const handleBatchUpload = async (e) => {
    e.preventDefault();
    if (!batchFile) return;
    setLoading(true);
    setErrorMsg(null);
    const formData = new FormData();
    formData.append('file', batchFile);
    try {
      const res = await fetch(`/api/admin/predict/batch?model_name=${encodeURIComponent(modelChoice)}`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        throw new Error(`Batch scoring API returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setBatchResult(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Batch scoring failed.');
    } finally {
      setLoading(false);
    }
  };

  // Demo Batch Cohort Generator (1-Click Test)
  const handleLoadDemoCohort = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const sampleRows = [
        "name,branch,gender,cgpa,backlogs,attendance_percentage,dsa_questions_solved,leetcode_questions_solved,hackerrank_questions_solved,aptitude_score,coding_skill_score,internships_count,projects_count,hackathons_count,mock_interview_score,placement_training",
        "Aarav Patel,CSE,Male,8.75,0,91,320,210,120,84,8.5,2,3,2,85,Yes",
        "Neha Deshmukh,IT,Female,9.10,0,94,410,290,150,89,9.2,2,4,3,90,Yes",
        "Rohan Gupta,ECE,Male,7.40,0,80,140,85,60,65,6.5,1,2,1,70,Yes",
        "Pooja Nair,CSE,Female,8.20,0,88,260,180,95,78,7.9,1,3,1,80,Yes",
        "Siddharth Rao,Mechanical,Male,6.30,1,68,45,20,25,52,4.8,0,1,0,50,No",
        "Tanvi Kulkarni,CSE,Female,8.90,0,93,350,240,130,86,8.8,2,4,2,88,Yes",
        "Varun Joshi,IT,Male,7.85,0,85,190,130,80,72,7.2,1,2,1,75,Yes",
        "Aniket Shinde,Civil,Male,6.10,2,62,30,15,10,48,4.0,0,1,0,45,No",
        "Meera Iyer,ECE,Female,8.45,0,89,280,195,110,81,8.1,1,3,2,82,Yes",
        "Aditya Sen,CSE,Male,9.40,0,96,480,350,180,94,9.5,3,5,4,95,Yes",
        "Shruti Mane,IT,Female,7.60,0,82,160,110,70,69,6.8,1,2,1,72,Yes",
        "Karan Mehta,Mechanical,Male,6.80,0,74,75,40,40,58,5.5,0,2,0,60,No"
      ].join("\n");

      const blob = new Blob([sampleRows], { type: 'text/csv' });
      const file = new File([blob], "demo_department_roster.csv", { type: 'text/csv' });
      setBatchFile(file);

      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`/api/admin/predict/batch?model_name=${encodeURIComponent(modelChoice)}`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        throw new Error(`Batch demo cohort returned HTTP ${res.status}`);
      }
      const data = await res.json();
      setBatchResult(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Demo batch scoring failed.');
    } finally {
      setLoading(false);
    }
  };

  // Download Sample CSV Template
  const handleDownloadCSVTemplate = () => {
    const csvContent = "name,branch,gender,cgpa,backlogs,attendance_percentage,dsa_questions_solved,leetcode_questions_solved,hackerrank_questions_solved,aptitude_score,coding_skill_score,internships_count,projects_count,hackathons_count,mock_interview_score,placement_training\nSample Student 1,CSE,Male,8.5,0,90,300,200,100,80,8.0,1,3,2,80,Yes\nSample Student 2,IT,Female,7.2,0,80,120,70,50,65,6.5,0,2,0,65,No";
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = "placement_batch_scoring_template.csv";
    link.click();
  };

  // Export Batch Results to CSV
  const handleExportBatchCSV = () => {
    if (!batchResult?.records?.length) return;
    const records = batchResult.records;
    const keys = Object.keys(records[0]);
    const csvRows = [
      keys.join(','),
      ...records.map(row => keys.map(k => JSON.stringify(row[k] ?? '')).join(','))
    ];
    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `scored_batch_roster_${modelChoice.replace(/\s+/g, '_')}.csv`;
    link.click();
  };

  return (
    <div>
      {/* Page Title & Breadcrumb Header */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 14 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
              <h2 style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--navy)', margin: 0 }}>
                Placement Prediction Center & Inference Suite
              </h2>
              <span className="badge badge-role" style={{ fontSize: '0.78rem' }}>
                <Activity size={12} style={{ marginRight: 4 }} /> Multi-Model Engine
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', margin: 0 }}>
              Operationalize 5 trained machine learning classifiers for real-time candidate assessment, consensus voting, and high-throughput departmental batch scoring.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Production Classifier:</span>
            <div className="badge badge-placed" style={{ fontWeight: 800, fontSize: '0.8rem', padding: '6px 12px' }}>
              <CheckCircle2 size={13} style={{ marginRight: 6 }} /> {systemSettingModel}
            </div>
          </div>
        </div>
      </div>

      {/* Global Error Banner */}
      {errorMsg && (
        <div style={{ padding: '12px 16px', background: '#FEE2E2', border: '1px solid #FECACA', color: '#991B1B', borderRadius: 8, marginBottom: 20, display: 'flex', alignItems: 'center', gap: 10 }}>
          <AlertCircle size={18} />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Top Executive KPI Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon-box kpi-icon-blue">
            <Cpu size={22} />
          </div>
          <div>
            <div className="kpi-title">Inference Engine</div>
            <div className="kpi-value" style={{ fontSize: '1.25rem' }}>{modelChoice}</div>
            <div className="kpi-subtitle">
              {MODEL_OPTIONS.find(m => m.value === modelChoice)?.badge || 'Supervised'} Classifier
            </div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-box kpi-icon-purple">
            <Layers size={22} />
          </div>
          <div>
            <div className="kpi-title">Consensus Suite</div>
            <div className="kpi-value" style={{ fontSize: '1.25rem' }}>5 Algorithms</div>
            <div className="kpi-subtitle">Bagging, Boosting, Trees, Log-Odds, Bayes</div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-box kpi-icon-green">
            <Users size={22} />
          </div>
          <div>
            <div className="kpi-title">Registered Candidates</div>
            <div className="kpi-value" style={{ fontSize: '1.25rem' }}>{students.length} Profiles</div>
            <div className="kpi-subtitle">Synchronized from Student Portal</div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-box kpi-icon-amber">
            <Zap size={22} />
          </div>
          <div>
            <div className="kpi-title">Inference Latency</div>
            <div className="kpi-value" style={{ fontSize: '1.25rem' }}>&lt; 15 ms</div>
            <div className="kpi-subtitle">Vectorized Scikit-Learn Engine</div>
          </div>
        </div>
      </div>

      {/* Segmented Tab Navigation Switcher */}
      <div className="tabs-container">
        <button
          className={`tab-btn ${activeTab === 'registered' ? 'active' : ''}`}
          onClick={() => { setActiveTab('registered'); setConsensusData(null); }}
        >
          <Users size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          1. Assess Registered Student
        </button>

        <button
          className={`tab-btn ${activeTab === 'adhoc' ? 'active' : ''}`}
          onClick={() => { setActiveTab('adhoc'); setConsensusData(null); }}
        >
          <Sliders size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          2. Ad-Hoc Candidate Simulator
        </button>

        <button
          className={`tab-btn ${activeTab === 'consensus' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('consensus');
            if (!consensusData && selectedStudent) {
              handleRunConsensus(selectedStudent);
            }
          }}
        >
          <Layers size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          3. 5-Algorithm Consensus Benchmark
        </button>

        <button
          className={`tab-btn ${activeTab === 'batch' ? 'active' : ''}`}
          onClick={() => { setActiveTab('batch'); setConsensusData(null); }}
        >
          <FileSpreadsheet size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          4. High-Throughput Batch CSV Scoring
        </button>
      </div>

      {/* ============================================================== */}
      {/* TAB 1: ASSESS REGISTERED CANDIDATE                            */}
      {/* ============================================================== */}
      {activeTab === 'registered' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: 24, marginBottom: 24 }}>
            
            {/* Left Column: Candidate & Model Selection */}
            <div className="campus-card">
              <div className="campus-card-header">
                <div>
                  <div className="card-title">Candidate Profile & Algorithm Selector</div>
                  <div className="card-subtitle">Choose a registered student and designate the scoring classifier</div>
                </div>
                <span className="badge badge-role">{students.length} Registered</span>
              </div>

              {/* Branch Filter Pills */}
              <div style={{ marginBottom: 14 }}>
                <label className="form-label">Filter Department:</label>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {['ALL', 'CSE', 'IT', 'ECE', 'MECHANICAL'].map((b) => (
                    <button
                      key={b}
                      type="button"
                      onClick={() => setBranchFilter(b)}
                      style={{
                        padding: '4px 10px',
                        borderRadius: 20,
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        border: '1px solid',
                        borderColor: branchFilter === b ? 'var(--primary)' : 'var(--border)',
                        background: branchFilter === b ? 'var(--primary)' : '#FFFFFF',
                        color: branchFilter === b ? '#FFFFFF' : 'var(--text-muted)',
                        transition: 'all 0.15s ease'
                      }}
                    >
                      {b}
                    </button>
                  ))}
                </div>
              </div>

              {/* Search & Select Student Dropdown */}
              <div className="form-group">
                <label className="form-label">Search / Select Candidate:</label>
                <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
                  <div style={{ position: 'relative', flex: 1 }}>
                    <Search size={15} style={{ position: 'absolute', left: 12, top: 13, color: 'var(--text-muted)' }} />
                    <input
                      type="text"
                      className="form-input"
                      style={{ paddingLeft: 34 }}
                      placeholder="Search candidate name or ID..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                </div>

                <select
                  className="form-select"
                  value={selectedStudentEmail}
                  onChange={(e) => {
                    setSelectedStudentEmail(e.target.value);
                    setRegisteredResult(null);
                    setConsensusData(null);
                    setFeedbackSuccess(false);
                  }}
                >
                  {filteredStudents.map((s) => (
                    <option key={s.email} value={s.email}>
                      {s.name} ({s.branch || 'CSE'} &bull; CGPA: {s.cgpa || 0} &bull; {s.student_id || s.email})
                    </option>
                  ))}
                </select>
              </div>

              {/* Selected Candidate Quick Overview Card */}
              {selectedStudent && (
                <div style={{
                  background: '#F8FAFC',
                  borderRadius: 10,
                  border: '1px solid #E2E8F0',
                  padding: 16,
                  marginBottom: 20
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
                    <div style={{
                      width: 44,
                      height: 44,
                      borderRadius: '50%',
                      background: 'var(--primary)',
                      color: '#FFF',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '1rem'
                    }}>
                      {(selectedStudent.name || 'S').charAt(0)}
                    </div>
                    <div>
                      <div style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '1rem' }}>
                        {selectedStudent.name}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {selectedStudent.student_id || 'ID Pending'} &bull; {selectedStudent.email}
                      </div>
                    </div>
                    <span className="badge badge-role" style={{ marginLeft: 'auto' }}>
                      {selectedStudent.branch || 'CSE'}
                    </span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, fontSize: '0.82rem' }}>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>CGPA</span>
                      <strong style={{ color: 'var(--navy)', fontSize: '0.95rem' }}>{selectedStudent.cgpa || 0}</strong>
                    </div>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>DSA Questions</span>
                      <strong style={{ color: 'var(--navy)', fontSize: '0.95rem' }}>{selectedStudent.dsa_questions_solved || selectedStudent.dsa_problems_solved || 0}</strong>
                    </div>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>Aptitude Score</span>
                      <strong style={{ color: 'var(--navy)', fontSize: '0.95rem' }}>{selectedStudent.aptitude_score || 0}/100</strong>
                    </div>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>Coding Skill</span>
                      <strong style={{ color: 'var(--navy)', fontSize: '0.95rem' }}>{selectedStudent.coding_skill_score || 0}/10</strong>
                    </div>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>Backlogs</span>
                      <strong style={{ color: (selectedStudent.backlogs || 0) > 0 ? 'var(--error)' : 'var(--success)', fontSize: '0.95rem' }}>
                        {selectedStudent.backlogs || 0}
                      </strong>
                    </div>
                    <div style={{ background: '#FFF', padding: '8px 10px', borderRadius: 6, border: '1px solid #E2E8F0' }}>
                      <span style={{ color: 'var(--text-muted)', display: 'block' }}>Training Status</span>
                      <strong style={{ color: 'var(--navy)', fontSize: '0.95rem' }}>{selectedStudent.placement_training || 'Yes'}</strong>
                    </div>
                  </div>
                </div>
              )}

              {/* Classifier Dropdown */}
              <div className="form-group">
                <label className="form-label">Inference Classifier:</label>
                <select
                  className="form-select"
                  value={modelChoice}
                  onChange={(e) => setModelChoice(e.target.value)}
                >
                  {MODEL_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label} — {opt.sub} ({opt.acc})
                    </option>
                  ))}
                </select>
              </div>

              {/* Action Buttons */}
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginTop: 20 }}>
                <button
                  type="button"
                  onClick={handleRunRegisteredPredict}
                  disabled={loading || !selectedStudent}
                  className="btn btn-primary"
                  style={{ flex: 1, minWidth: 200 }}
                >
                  <Target size={16} />
                  {loading ? 'Executing Inference...' : `Score with ${modelChoice}`}
                </button>

                <button
                  type="button"
                  onClick={() => handleRunConsensus(selectedStudent)}
                  disabled={comparing || !selectedStudent}
                  className="btn btn-secondary"
                  style={{ flex: 1, minWidth: 200 }}
                >
                  <Layers size={16} />
                  {comparing ? 'Voting Across 5 Models...' : 'Run 5-Model Consensus'}
                </button>
              </div>
            </div>

            {/* Right Column: Inference Result & Faculty Feedback */}
            <div>
              {registeredResult ? (
                <div className="campus-card">
                  <div className="campus-card-header">
                    <div>
                      <div className="card-title">Inference Diagnostic Outcome</div>
                      <div className="card-subtitle">
                        Evaluated by <b>{registeredResult.model_name}</b> on candidate profile
                      </div>
                    </div>
                    <span className={`badge ${registeredResult.status === 'Placed' ? 'badge-placed' : 'badge-not-placed'}`}>
                      {registeredResult.status}
                    </span>
                  </div>

                  {/* Big Outcome Hero Card */}
                  <div
                    style={{
                      padding: 22,
                      borderRadius: 12,
                      textAlign: 'center',
                      marginBottom: 20,
                      background: registeredResult.status === 'Placed' ? '#F0FDF4' : '#FEF2F2',
                      border: `2px solid ${registeredResult.status === 'Placed' ? '#86EFAC' : '#FECACA'}`,
                    }}
                  >
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: '1.75rem', fontWeight: 900, color: registeredResult.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                      {registeredResult.status === 'Placed' ? <CheckCircle2 size={32} /> : <AlertTriangle size={32} />}
                      {registeredResult.status === 'Placed' ? 'LIKELY PLACED' : 'NOT PLACED / AT RISK'}
                    </div>

                    <div style={{ marginTop: 8, fontSize: '1.1rem', fontWeight: 800, color: 'var(--navy)' }}>
                      Confidence: {registeredResult.probability_percent}%
                    </div>

                    {/* Visual Progress Probability Bar */}
                    <div style={{ width: '100%', height: 10, background: '#E2E8F0', borderRadius: 999, overflow: 'hidden', margin: '12px auto' }}>
                      <div
                        style={{
                          width: `${Math.min(100, Math.max(0, registeredResult.probability_percent))}%`,
                          height: '100%',
                          background: registeredResult.status === 'Placed'
                            ? 'linear-gradient(90deg, #22C55E 0%, #16A34A 100%)'
                            : 'linear-gradient(90deg, #F87171 0%, #DC2626 100%)',
                          borderRadius: 999,
                          transition: 'width 0.6s ease'
                        }}
                      />
                    </div>

                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      Placement Readiness Tier: <b style={{ color: 'var(--navy)' }}>{registeredResult.readiness_level || 'Evaluated'}</b>
                    </div>
                  </div>

                  {/* Strengths & Improvement Pillars */}
                  {Array.isArray(registeredResult.strengths) && registeredResult.strengths.length > 0 && (
                    <div style={{ marginBottom: 16 }}>
                      <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#16A34A', textTransform: 'uppercase', marginBottom: 6 }}>
                        Key Technical Strengths:
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                        {registeredResult.strengths.map((str, idx) => (
                          <span key={idx} className="badge badge-placed" style={{ fontSize: '0.78rem' }}>
                            ✓ {renderStrengthText(str)}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {((registeredResult.top_improvements && registeredResult.top_improvements.length > 0) ||
                    (registeredResult.improvements && registeredResult.improvements.length > 0)) && (
                    <div style={{ marginBottom: 20 }}>
                      <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#DC2626', textTransform: 'uppercase', marginBottom: 6 }}>
                        Prescriptive Interventions Needed:
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {(registeredResult.top_improvements || registeredResult.improvements || []).slice(0, 3).map((imp, idx) => (
                          <div key={idx} style={{ padding: '8px 12px', background: '#FEF2F2', borderRadius: 6, border: '1px solid #FECACA', fontSize: '0.82rem', color: '#991B1B' }}>
                            ⚠️ {renderImprovementText(imp)}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Official Faculty Advisory Notes Form */}
                  <div style={{ borderTop: '1px solid var(--border)', paddingTop: 16 }}>
                    <div style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--navy)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                      <ThumbsUp size={16} color="var(--primary)" />
                      Record Official Faculty Advisory Notes
                    </div>
                    <form onSubmit={handleSaveFeedback}>
                      <div className="form-group" style={{ marginBottom: 10 }}>
                        <label className="form-label" style={{ fontSize: '0.8rem' }}>Advisory Verdict:</label>
                        <select
                          className="form-select"
                          value={feedbackStatus}
                          onChange={(e) => setFeedbackStatus(e.target.value)}
                        >
                          <option value="High Potential">High Potential (Day-1 Product Ready)</option>
                          <option value="Placed">Placed (Satisfactory Readiness)</option>
                          <option value="At Risk">At Risk (Needs Targeted Mentorship)</option>
                          <option value="Not Placed">Not Placed (Urgent Bootcamp Required)</option>
                        </select>
                      </div>

                      <div className="form-group" style={{ marginBottom: 12 }}>
                        <label className="form-label" style={{ fontSize: '0.8rem' }}>Feedback Notes (Visible on Student's Portal):</label>
                        <textarea
                          className="form-input"
                          rows={3}
                          value={feedbackNotes}
                          onChange={(e) => setFeedbackNotes(e.target.value)}
                          placeholder="e.g. Good CGPA, but must solve 50+ medium LeetCode DSA questions and attend soft skills mock interview before Day 1."
                          required
                        />
                      </div>

                      {feedbackSuccess && (
                        <div style={{ padding: 10, borderRadius: 6, background: '#DCFCE7', color: '#166534', fontSize: '0.85rem', marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
                          <CheckCircle2 size={16} /> Feedback saved and published to student portal!
                        </div>
                      )}

                      <button type="submit" disabled={savingFeedback} className="btn btn-secondary" style={{ width: '100%' }}>
                        <Save size={15} /> {savingFeedback ? 'Saving Advisory Notes...' : 'Save Notes to Student Profile'}
                      </button>
                    </form>
                  </div>
                </div>
              ) : (
                <div className="campus-card" style={{ textAlign: 'center', padding: '60px 24px', color: 'var(--text-muted)' }}>
                  <Target size={48} style={{ opacity: 0.35, margin: '0 auto 16px auto', color: 'var(--primary)' }} />
                  <h4 style={{ color: 'var(--navy)', marginBottom: 6 }}>Awaiting Inference Run</h4>
                  <p style={{ maxWidth: 360, margin: '0 auto', fontSize: '0.88rem' }}>
                    Select a candidate from the roster and click <b>Score with {modelChoice}</b> or <b>Run 5-Model Consensus</b> to generate instant predictive insights.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Consensus Section if generated */}
          {consensusData && (
            <div className="campus-card" style={{ border: '2px solid var(--primary)', marginBottom: 24 }}>
              <div className="campus-card-header">
                <div>
                  <div className="card-title">5-Algorithm Consensus Decision Matrix</div>
                  <div className="card-subtitle">
                    Ensemble agreement across distinct mathematical inductive biases for candidate <b>{selectedStudent?.name}</b>
                  </div>
                </div>

                <div style={{
                  padding: '8px 18px',
                  borderRadius: 20,
                  background: consensusData.consensus?.status === 'Placed' ? '#DCFCE7' : '#FEE2E2',
                  color: consensusData.consensus?.status === 'Placed' ? '#166534' : '#991B1B',
                  fontWeight: 800,
                  fontSize: '0.92rem'
                }}>
                  Consensus: {consensusData.consensus?.status} ({consensusData.consensus?.placed_votes}/{consensusData.consensus?.total_models} models agree &bull; {consensusData.consensus?.consensus_percent}%)
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))', gap: 14 }}>
                {Object.entries(consensusData.models || {}).map(([mName, mRes]) => {
                  const isPlaced = mRes.status === 'Placed';
                  return (
                    <div
                      key={mName}
                      style={{
                        padding: 16,
                        borderRadius: 10,
                        background: isPlaced ? '#F0FDF4' : '#FEF2F2',
                        border: `1.5px solid ${isPlaced ? '#86EFAC' : '#FECACA'}`,
                      }}
                    >
                      <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-body)', marginBottom: 4 }}>
                        {mName}
                      </div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 900, color: isPlaced ? '#16A34A' : '#DC2626' }}>
                        {mRes.status}
                      </div>
                      <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--navy)', marginTop: 4 }}>
                        {mRes.probability_percent}% prob
                      </div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: 4 }}>
                        Readiness: {mRes.readiness_level || 'Calibrated'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 2: AD-HOC CANDIDATE SIMULATOR                              */}
      {/* ============================================================== */}
      {activeTab === 'adhoc' && (
        <form onSubmit={handleRunAdHocPredict} className="campus-card" style={{ marginBottom: 24 }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">Ad-Hoc Candidate Feature Simulator</div>
              <div className="card-subtitle">Test arbitrary student profiles against any machine learning classifier or consensus engine</div>
            </div>

            {/* Quick Presets */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Quick Presets:</span>
              <button type="button" onClick={() => applyPreset('high')} className="btn btn-secondary" style={{ fontSize: '0.78rem', padding: '5px 10px' }}>
                ⭐ High Achiever
              </button>
              <button type="button" onClick={() => applyPreset('average')} className="btn btn-secondary" style={{ fontSize: '0.78rem', padding: '5px 10px' }}>
                ⚖️ Average Candidate
              </button>
              <button type="button" onClick={() => applyPreset('atrisk')} className="btn btn-secondary" style={{ fontSize: '0.78rem', padding: '5px 10px' }}>
                ⚠️ At-Risk Candidate
              </button>
            </div>
          </div>

          {/* Form Input Groups */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20, marginBottom: 24 }}>
            
            {/* Group 1: Academic History */}
            <div style={{ background: '#F8FAFC', padding: 18, borderRadius: 10, border: '1px solid #E2E8F0' }}>
              <div style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '0.9rem', marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
                <Award size={16} color="var(--primary)" /> 1. Academic Credentials
              </div>
              
              <div className="form-group">
                <label className="form-label">Candidate Name:</label>
                <input
                  type="text"
                  className="form-input"
                  value={adHocForm.name}
                  onChange={(e) => setAdHocForm({ ...adHocForm, name: e.target.value })}
                  required
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">Discipline:</label>
                  <select
                    className="form-select"
                    value={adHocForm.branch}
                    onChange={(e) => setAdHocForm({ ...adHocForm, branch: e.target.value })}
                  >
                    <option value="CSE">CSE</option>
                    <option value="IT">IT</option>
                    <option value="ECE">ECE</option>
                    <option value="EE">EE</option>
                    <option value="Mechanical">Mechanical</option>
                    <option value="Civil">Civil</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Gender:</label>
                  <select
                    className="form-select"
                    value={adHocForm.gender}
                    onChange={(e) => setAdHocForm({ ...adHocForm, gender: e.target.value })}
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">CGPA (0-10):</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    className="form-input"
                    value={adHocForm.cgpa}
                    onChange={(e) => setAdHocForm({ ...adHocForm, cgpa: parseFloat(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Backlogs:</label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    className="form-input"
                    value={adHocForm.backlogs}
                    onChange={(e) => setAdHocForm({ ...adHocForm, backlogs: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Attendance %:</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    className="form-input"
                    value={adHocForm.attendance_percentage}
                    onChange={(e) => setAdHocForm({ ...adHocForm, attendance_percentage: parseFloat(e.target.value) || 0 })}
                  />
                </div>
              </div>
            </div>

            {/* Group 2: Problem Solving & Technical */}
            <div style={{ background: '#F8FAFC', padding: 18, borderRadius: 10, border: '1px solid #E2E8F0' }}>
              <div style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '0.9rem', marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
                <Cpu size={16} color="var(--primary)" /> 2. Competitive Programming & Coding
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">DSA Questions Solved:</label>
                  <input
                    type="number"
                    min="0"
                    max="1000"
                    className="form-input"
                    value={adHocForm.dsa_problems_solved}
                    onChange={(e) => setAdHocForm({ ...adHocForm, dsa_problems_solved: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">LeetCode Solved:</label>
                  <input
                    type="number"
                    min="0"
                    max="1000"
                    className="form-input"
                    value={adHocForm.leetcode_problems_solved}
                    onChange={(e) => setAdHocForm({ ...adHocForm, leetcode_problems_solved: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">HackerRank Score:</label>
                  <input
                    type="number"
                    min="0"
                    max="1000"
                    className="form-input"
                    value={adHocForm.hackerrank_score}
                    onChange={(e) => setAdHocForm({ ...adHocForm, hackerrank_score: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Coding Skill (0-10):</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="10"
                    className="form-input"
                    value={adHocForm.coding_skill_score}
                    onChange={(e) => setAdHocForm({ ...adHocForm, coding_skill_score: parseFloat(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Aptitude Score (0-100):</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  className="form-input"
                  value={adHocForm.aptitude_score}
                  onChange={(e) => setAdHocForm({ ...adHocForm, aptitude_score: parseFloat(e.target.value) || 0 })}
                />
              </div>
            </div>

            {/* Group 3: Co-Curricular & Soft Skills */}
            <div style={{ background: '#F8FAFC', padding: 18, borderRadius: 10, border: '1px solid #E2E8F0' }}>
              <div style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '0.9rem', marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
                <Zap size={16} color="var(--primary)" /> 3. Experience & Soft Skills
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">Internships:</label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    className="form-input"
                    value={adHocForm.internships_completed}
                    onChange={(e) => setAdHocForm({ ...adHocForm, internships_completed: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Projects:</label>
                  <input
                    type="number"
                    min="0"
                    max="15"
                    className="form-input"
                    value={adHocForm.projects_count}
                    onChange={(e) => setAdHocForm({ ...adHocForm, projects_count: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">Hackathons:</label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    className="form-input"
                    value={adHocForm.hackathons_participated}
                    onChange={(e) => setAdHocForm({ ...adHocForm, hackathons_participated: parseInt(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">GitHub Repos:</label>
                  <input
                    type="number"
                    min="0"
                    max="50"
                    className="form-input"
                    value={adHocForm.github_repos_count}
                    onChange={(e) => setAdHocForm({ ...adHocForm, github_repos_count: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div className="form-group">
                  <label className="form-label">Mock Interview (0-100):</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    className="form-input"
                    value={adHocForm.mock_interview_score}
                    onChange={(e) => setAdHocForm({ ...adHocForm, mock_interview_score: parseFloat(e.target.value) || 0 })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Placement Training:</label>
                  <select
                    className="form-select"
                    value={adHocForm.placement_training}
                    onChange={(e) => setAdHocForm({ ...adHocForm, placement_training: e.target.value })}
                  >
                    <option value="Yes">Yes (Enrolled)</option>
                    <option value="No">No</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Action Row */}
          <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Target Classifier:</label>
              <select
                className="form-select"
                style={{ width: 220 }}
                value={modelChoice}
                onChange={(e) => setModelChoice(e.target.value)}
              >
                {MODEL_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>

            <button type="submit" disabled={loading} className="btn btn-primary" style={{ flex: 1, minWidth: 200 }}>
              <Target size={16} /> {loading ? 'Evaluating...' : `Predict with ${modelChoice}`}
            </button>

            <button
              type="button"
              onClick={() => handleRunConsensus(adHocForm)}
              disabled={comparing}
              className="btn btn-secondary"
              style={{ flex: 1, minWidth: 200 }}
            >
              <Layers size={16} /> {comparing ? 'Comparing Across 5 Models...' : 'Compare 5 Models'}
            </button>
          </div>

          {/* Result Card for Ad-Hoc */}
          {adHocResult && (
            <div
              style={{
                marginTop: 24,
                padding: 20,
                borderRadius: 12,
                background: adHocResult.status === 'Placed' ? '#F0FDF4' : '#FEF2F2',
                border: `2px solid ${adHocResult.status === 'Placed' ? '#86EFAC' : '#FECACA'}`,
                display: 'flex',
                flexDirection: 'column',
                gap: 14
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
                <div>
                  <div style={{ fontSize: '1.45rem', fontWeight: 900, color: adHocResult.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                    {adHocResult.status === 'Placed' ? '✓ LIKELY PLACED' : '⚠️ UNLIKELY PLACED / AT RISK'} ({adHocResult.probability_percent}%)
                  </div>
                  <div style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: 4 }}>
                    Readiness: <b>{adHocResult.readiness_level}</b> &bull; Evaluated using <b>{adHocResult.model_name}</b>
                  </div>
                </div>

                {Array.isArray(adHocResult.strengths) && adHocResult.strengths.length > 0 && (
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    {adHocResult.strengths.slice(0, 3).map((s, i) => (
                      <span key={i} className="badge badge-placed">{renderStrengthText(s)}</span>
                    ))}
                  </div>
                )}
              </div>

              {((adHocResult.top_improvements && adHocResult.top_improvements.length > 0) ||
                (adHocResult.improvements && adHocResult.improvements.length > 0)) && (
                <div style={{ borderTop: '1px solid rgba(0,0,0,0.06)', paddingTop: 12 }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#DC2626', textTransform: 'uppercase', marginBottom: 6 }}>
                    Prescriptive Action Items:
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {(adHocResult.top_improvements || adHocResult.improvements || []).slice(0, 3).map((imp, idx) => (
                      <div key={idx} style={{ padding: '6px 12px', background: 'rgba(255,255,255,0.8)', borderRadius: 6, fontSize: '0.82rem', color: '#991B1B', border: '1px solid rgba(220,38,38,0.15)' }}>
                        ⚠️ {renderImprovementText(imp)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Consensus Table for Ad-Hoc */}
          {consensusData && (
            <div style={{ marginTop: 20, padding: 18, background: '#F8FAFC', borderRadius: 12, border: '1.5px solid #CBD5E1' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
                <strong style={{ color: 'var(--navy)', fontSize: '1.05rem' }}>5-Algorithm Consensus Analysis</strong>
                <span className="badge" style={{
                  background: consensusData.consensus?.status === 'Placed' ? '#DCFCE7' : '#FEE2E2',
                  color: consensusData.consensus?.status === 'Placed' ? '#166534' : '#991B1B',
                  fontWeight: 800
                }}>
                  {consensusData.consensus?.placed_votes}/{consensusData.consensus?.total_models} Models Predict Placed
                </span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: 10 }}>
                {Object.entries(consensusData.models || {}).map(([mName, mRes]) => (
                  <div key={mName} style={{ padding: 12, background: '#FFF', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>{mName}</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: 800, color: mRes.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                      {mRes.status} ({mRes.probability_percent}%)
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </form>
      )}

      {/* ============================================================== */}
      {/* TAB 3: 5-ALGORITHM CONSENSUS BENCHMARK VIEW                    */}
      {/* ============================================================== */}
      {activeTab === 'consensus' && (
        <div className="campus-card" style={{ marginBottom: 24 }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">Multi-Model Consensus Inference Suite</div>
              <div className="card-subtitle">
                Cross-validates predictions against 5 distinct mathematical inductive biases
              </div>
            </div>

            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <button
                type="button"
                onClick={() => handleRunConsensus(selectedStudent)}
                disabled={comparing}
                className="btn btn-primary"
                style={{ fontSize: '0.82rem' }}
              >
                <RefreshCw size={14} className={comparing ? 'spin' : ''} />
                {comparing ? 'Calculating...' : 'Re-Evaluate Consensus'}
              </button>
            </div>
          </div>

          {consensusData ? (
            <div>
              {/* Big Consensus Hero */}
              <div style={{
                padding: 24,
                borderRadius: 12,
                background: consensusData.consensus?.status === 'Placed' ? '#F0FDF4' : '#FEF2F2',
                border: `2px solid ${consensusData.consensus?.status === 'Placed' ? '#86EFAC' : '#FECACA'}`,
                marginBottom: 24,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: 16
              }}>
                <div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 900, color: consensusData.consensus?.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                    Consensus Verdict: {consensusData.consensus?.status}
                  </div>
                  <div style={{ fontSize: '0.95rem', color: 'var(--text-body)', marginTop: 4 }}>
                    Candidate: <b>{selectedStudent?.name || 'Selected Candidate'}</b> ({selectedStudent?.branch || 'CSE'}) &bull; Agreement: <b>{consensusData.consensus?.consensus_percent}%</b>
                  </div>
                </div>

                <div style={{
                  padding: '12px 24px',
                  borderRadius: 12,
                  background: '#FFFFFF',
                  boxShadow: 'var(--shadow-sm)',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Model Agreement</div>
                  <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--navy)' }}>
                    {consensusData.consensus?.placed_votes} / {consensusData.consensus?.total_models}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#16A34A', fontWeight: 700 }}>Models Voted Placed</div>
                </div>
              </div>

              {/* Models Comparison Cards Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
                {MODEL_OPTIONS.map((m) => {
                  const mRes = consensusData.models?.[m.value];
                  if (!mRes) return null;
                  const isPlaced = mRes.status === 'Placed';
                  return (
                    <div
                      key={m.value}
                      style={{
                        padding: 18,
                        borderRadius: 10,
                        background: '#FFFFFF',
                        border: `1.5px solid ${isPlaced ? '#86EFAC' : '#FECACA'}`,
                        boxShadow: 'var(--shadow-sm)'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                        <span className="badge badge-role" style={{ fontSize: '0.7rem' }}>{m.badge}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>{m.acc} Acc</span>
                      </div>
                      <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--navy)', marginBottom: 6 }}>
                        {m.value}
                      </div>
                      <div style={{ fontSize: '1.35rem', fontWeight: 900, color: isPlaced ? '#16A34A' : '#DC2626', marginBottom: 4 }}>
                        {mRes.status}
                      </div>

                      <div style={{ width: '100%', height: 6, background: '#E2E8F0', borderRadius: 999, overflow: 'hidden', margin: '8px 0' }}>
                        <div
                          style={{
                            width: `${Math.min(100, Math.max(0, mRes.probability_percent))}%`,
                            height: '100%',
                            background: isPlaced ? '#16A34A' : '#DC2626',
                            borderRadius: 999
                          }}
                        />
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        <span>Probability:</span>
                        <strong style={{ color: 'var(--navy)' }}>{mRes.probability_percent}%</strong>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 2 }}>
                        <span>Readiness:</span>
                        <strong style={{ color: 'var(--navy)' }}>{mRes.readiness_level}</strong>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
              <Layers size={40} style={{ opacity: 0.3, margin: '0 auto 12px auto' }} />
              <p>Click "Re-Evaluate Consensus" above to run parallel inference across all 5 models.</p>
            </div>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 4: HIGH-THROUGHPUT BATCH CSV SCORING                       */}
      {/* ============================================================== */}
      {activeTab === 'batch' && (
        <div className="campus-card" style={{ marginBottom: 24 }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">High-Throughput Departmental Batch Scoring</div>
              <div className="card-subtitle">Score entire student cohorts in milliseconds via CSV upload or instant demo cohort</div>
            </div>

            <div style={{ display: 'flex', gap: 8 }}>
              <button
                type="button"
                onClick={handleDownloadCSVTemplate}
                className="btn btn-secondary"
                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
              >
                <Download size={14} /> Download CSV Template
              </button>
              <button
                type="button"
                onClick={handleLoadDemoCohort}
                disabled={loading}
                className="btn btn-outline-primary"
                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
              >
                <Sparkles size={14} /> 1-Click Demo Cohort
              </button>
            </div>
          </div>

          {/* Model Selector for Batch */}
          <div style={{ marginBottom: 18, display: 'flex', alignItems: 'center', gap: 12 }}>
            <label className="form-label" style={{ margin: 0 }}>Batch Scoring Classifier:</label>
            <select
              className="form-select"
              style={{ maxWidth: 340 }}
              value={modelChoice}
              onChange={(e) => setModelChoice(e.target.value)}
            >
              {MODEL_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label} ({opt.badge})</option>
              ))}
            </select>
          </div>

          {/* Upload Drop Zone Card */}
          <form onSubmit={handleBatchUpload} style={{ marginBottom: 24 }}>
            <div style={{
              border: '2px dashed #CBD5E1',
              borderRadius: 12,
              padding: '24px 20px',
              textAlign: 'center',
              background: '#F8FAFC',
              marginBottom: 16
            }}>
              <Upload size={36} color="var(--primary)" style={{ opacity: 0.7, marginBottom: 8 }} />
              <div style={{ fontWeight: 700, color: 'var(--navy)', marginBottom: 4 }}>
                Choose CSV File or Use 1-Click Demo Cohort
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: 14 }}>
                Accepts comma-separated values containing standard feature columns (e.g. <code>cgpa</code>, <code>dsa_questions_solved</code>, <code>aptitude_score</code>)
              </p>

              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 12 }}>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setBatchFile(e.target.files[0])}
                  style={{ fontSize: '0.88rem' }}
                />
                <button type="submit" disabled={loading || !batchFile} className="btn btn-primary">
                  <Cpu size={16} /> {loading ? 'Scoring Roster...' : `Score Roster with ${modelChoice}`}
                </button>
              </div>
            </div>
          </form>

          {/* Scored Batch Outcomes */}
          {batchResult && (
            <div>
              {/* Batch Summary Stats */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 20 }}>
                <div className="campus-card" style={{ padding: 18, textAlign: 'center', borderTop: '4px solid var(--primary)', margin: 0 }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Total Processed</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--navy)' }}>{batchResult.total}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Candidate profiles</div>
                </div>

                <div className="campus-card" style={{ padding: 18, textAlign: 'center', borderTop: '4px solid var(--success)', margin: 0 }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Predicted Placed</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--success)' }}>{batchResult.placed_count}</div>
                  <div style={{ fontSize: '0.78rem', color: '#16A34A', fontWeight: 600 }}>Ready for placement</div>
                </div>

                <div className="campus-card" style={{ padding: 18, textAlign: 'center', borderTop: '4px solid var(--error)', margin: 0 }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>At Risk / Not Placed</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--error)' }}>
                    {batchResult.total - batchResult.placed_count}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#DC2626', fontWeight: 600 }}>Needs training</div>
                </div>

                <div className="campus-card" style={{ padding: 18, textAlign: 'center', borderTop: '4px solid #8B5CF6', margin: 0 }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Placement Rate</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900, color: '#8B5CF6' }}>
                    {((batchResult.placed_count / (batchResult.total || 1)) * 100).toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Estimated conversion</div>
                </div>
              </div>

              {/* Table Toolbar & Search */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, flexWrap: 'wrap', gap: 10 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Search size={15} color="var(--text-muted)" />
                  <input
                    type="text"
                    className="form-input"
                    style={{ width: 260, padding: '6px 12px', fontSize: '0.85rem' }}
                    placeholder="Search scored candidate..."
                    value={batchSearchTerm}
                    onChange={(e) => setBatchSearchTerm(e.target.value)}
                  />
                </div>

                <button
                  type="button"
                  onClick={handleExportBatchCSV}
                  className="btn btn-secondary"
                  style={{ fontSize: '0.82rem', padding: '6px 14px' }}
                >
                  <Download size={14} /> Export Scored Roster (CSV)
                </button>
              </div>

              {/* Batch Table */}
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Candidate Name / ID</th>
                      <th>Branch</th>
                      <th>CGPA</th>
                      <th>Predicted Status</th>
                      <th>Confidence Score</th>
                      <th>Readiness Tier</th>
                    </tr>
                  </thead>
                  <tbody>
                    {batchResult.records
                      .filter(r => (r.name || r.student_id || '').toLowerCase().includes(batchSearchTerm.toLowerCase()))
                      .map((r, i) => {
                        const isPlaced = r.Predicted_Placement === 'Placed';
                        return (
                          <tr key={i}>
                            <td style={{ fontWeight: 700, color: 'var(--navy)' }}>
                              {r.name || r.student_id || `Candidate #${i + 1}`}
                            </td>
                            <td><span className="badge badge-role" style={{ fontSize: '0.72rem' }}>{r.branch || 'CSE'}</span></td>
                            <td style={{ fontWeight: 600 }}>{r.cgpa || '-'}</td>
                            <td>
                              <span className={`badge ${isPlaced ? 'badge-placed' : 'badge-not-placed'}`}>
                                {isPlaced ? '✓ Placed' : '⚠️ Not Placed'}
                              </span>
                            </td>
                            <td style={{ fontWeight: 700, color: 'var(--navy)' }}>{r.Confidence || '-'}</td>
                            <td>{r.Readiness_Tier || 'Tier 1'}</td>
                          </tr>
                        );
                      })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Analytical Conclusion & Academic Justification */}
      <AcademicJustification
        title="Predictive Inference Center: Multi-Model Scoring & Project Outcomes"
        techniqueName="Ensemble Scoring Console • Multi-Model Consensus Voting • High-Throughput Batch Inference"
        whyChosen={[
          [
            "Why an Operational Multi-Model Inference Center is Deployed",
            "Individual offline ML models often fail to translate into practical administrative workflows. The Prediction Center operationalizes all 5 trained models (Random Forest, Gradient Boosting, Decision Tree, Logistic Regression, Naive Bayes) into an interactive real-time console supporting both individual candidate assessment and high-throughput batch scoring."
          ],
          [
            "Why Multi-Model Consensus Voting is Valuable",
            "Rather than relying blindly on a single algorithm, consensus voting aggregates predictions across multiple distinct inductive principles (bagging, boosting, linear hyperplanes, and probability densities), providing higher confidence when evaluating borderline candidates."
          ],
          [
            "Why High-Throughput Batch CSV Scoring is Integrated",
            "Campus placement cells manage hundreds of eligible candidates per department. Batch inference vectorizes candidate feature matrices, scoring 500+ student profiles in milliseconds."
          ]
        ]}
        whatWeGet={[
          [
            "Proactive Placement Readiness Rosters",
            "Scores graduating classes 6 to 12 months ahead of company visits, generating an early ranked roster of candidate readiness and probability distributions."
          ],
          [
            "Individualized Risk Factor Diagnosis",
            "Breaks down individual prediction confidence, highlighting specific features (e.g. low mock interview score or weak DSA problem count) holding a student back."
          ],
          [
            "Objective, Data-Backed Placement Mentoring",
            "Equips placement coordinators with quantifiable, unbiased guidance to support student counseling and track improvements after training interventions."
          ]
        ]}
        institutionalImpact="Enables early proactive intervention before recruitment drives commence. Placement directors can rapidly score entire departmental cohorts to identify students needing urgent skill bootcamps, mock interviews, or aptitude training, converting retrospective placement reports into forward-looking guidance."
        dwmConcept="Supervised Model Inference, Out-of-sample Generalization, Multi-Model Consensus Voting, Threshold Calibration, Batch Matrix Feature Engineering, Actionable Prescriptive Analytics."
      />
    </div>
  );
}
