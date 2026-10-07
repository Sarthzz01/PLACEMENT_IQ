import React, { useState, useEffect } from 'react';
import { Target, Users, User, Upload, CheckCircle2, AlertTriangle, ArrowRight, Save, Download } from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

export default function PredictionCenter({ user }) {
  const [activeTab, setActiveTab] = useState('registered');
  const [students, setStudents] = useState([]);
  const [selectedStudentEmail, setSelectedStudentEmail] = useState('');
  const [modelChoice, setModelChoice] = useState('Random Forest');
  const [loading, setLoading] = useState(false);
  
  // Registered student state
  const [registeredResult, setRegisteredResult] = useState(null);
  const [feedbackStatus, setFeedbackStatus] = useState('High Potential');
  const [feedbackNotes, setFeedbackNotes] = useState('');
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);

  // Ad-hoc candidate form state
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
    placement_training: 'Yes',
  });
  const [adHocResult, setAdHocResult] = useState(null);

  // Batch CSV state
  const [batchFile, setBatchFile] = useState(null);
  const [batchResult, setBatchResult] = useState(null);

  useEffect(() => {
    fetch('/api/admin/students')
      .then((r) => r.json())
      .then((d) => {
        const list = d.students || [];
        setStudents(list);
        if (list.length > 0) setSelectedStudentEmail(list[0].email);
      })
      .catch((e) => console.error(e));
  }, []);

  const handleRunRegisteredPredict = async () => {
    const student = students.find((s) => s.email === selectedStudentEmail);
    if (!student) return;
    setLoading(true);
    setFeedbackSuccess(false);
    try {
      const res = await fetch('/api/admin/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: student.email,
          data: student,
          model_name: modelChoice,
        }),
      });
      const data = await res.json();
      setRegisteredResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveFeedback = async (e) => {
    e.preventDefault();
    if (!selectedStudentEmail) return;
    try {
      await fetch('/api/admin/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_email: selectedStudentEmail,
          admin_name: user?.name || 'Administrator',
          status: feedbackStatus,
          notes: feedbackNotes,
        }),
      });
      setFeedbackSuccess(true);
      setFeedbackNotes('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleRunAdHocPredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/admin/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: adHocForm,
          model_name: modelChoice,
        }),
      });
      const data = await res.json();
      setAdHocResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBatchUpload = async (e) => {
    e.preventDefault();
    if (!batchFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', batchFile);
    try {
      const res = await fetch(`/api/admin/predict/batch?model_name=${encodeURIComponent(modelChoice)}`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setBatchResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const selectedStudent = students.find((s) => s.email === selectedStudentEmail);

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-main)', margin: '0 0 6px 0' }}>
          Placement Prediction Center & Batch Assessment
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: 0 }}>
          Evaluate candidate likelihoods across registered student records or upload external CSV rosters for automated batch scoring.
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 12, borderBottom: '1px solid var(--border-color)', marginBottom: 24 }}>
        <button
          onClick={() => setActiveTab('registered')}
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
            color: activeTab === 'registered' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'registered' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Users size={16} /> 1. Assess Registered Student
        </button>
        <button
          onClick={() => setActiveTab('adhoc')}
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
            color: activeTab === 'adhoc' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'adhoc' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <User size={16} /> 2. Ad-Hoc Candidate Profile
        </button>
        <button
          onClick={() => setActiveTab('batch')}
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
            color: activeTab === 'batch' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'batch' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Upload size={16} /> 3. High-Throughput Batch CSV Scoring
        </button>
      </div>

      {/* Tab 1: Registered Student */}
      {activeTab === 'registered' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
          <div className="campus-card">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
              Candidate Selection & Model Parameters
            </h3>

            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
                Select Registered Student:
              </label>
              <select
                className="input-field"
                value={selectedStudentEmail}
                onChange={(e) => {
                  setSelectedStudentEmail(e.target.value);
                  setRegisteredResult(null);
                  setFeedbackSuccess(false);
                }}
              >
                {students.map((s) => (
                  <option key={s.email} value={s.email}>
                    {s.name} ({s.branch || 'CSE'} - {s.email})
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: 20 }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
                Evaluation Classifier:
              </label>
              <select
                className="input-field"
                value={modelChoice}
                onChange={(e) => setModelChoice(e.target.value)}
              >
                <option value="Random Forest">Random Forest (Recommended - 86.5% Acc)</option>
                <option value="Decision Tree">Decision Tree (Transparent Rules)</option>
                <option value="Naive Bayes">Gaussian Naive Bayes (Probabilistic)</option>
              </select>
            </div>

            {selectedStudent && (
              <div style={{ background: '#F8FAFC', padding: 14, borderRadius: 8, border: '1px solid #E2E8F0', fontSize: '0.85rem', lineHeight: 1.8, marginBottom: 20 }}>
                <div><b>Candidate:</b> {selectedStudent.name} &bull; <b>Branch:</b> {selectedStudent.branch || 'CSE'}</div>
                <div><b>CGPA:</b> {selectedStudent.cgpa || 0} &bull; <b>Attendance:</b> {selectedStudent.attendance_percentage || 0}% &bull; <b>Backlogs:</b> {selectedStudent.backlogs || 0}</div>
                <div><b>DSA Solved:</b> {selectedStudent.dsa_problems_solved || 0} &bull; <b>Aptitude:</b> {selectedStudent.aptitude_score || 0}/100 &bull; <b>Coding:</b> {selectedStudent.coding_skill_score || 0}/10</div>
              </div>
            )}

            <button
              onClick={handleRunRegisteredPredict}
              disabled={loading || !selectedStudentEmail}
              className="btn-primary"
              style={{ width: '100%' }}
            >
              <Target size={16} /> {loading ? 'Running Model Inference...' : 'Evaluate Candidate Placement'}
            </button>
          </div>

          <div>
            {registeredResult ? (
              <div className="campus-card">
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
                  Inference Outcome
                </h3>

                <div
                  style={{
                    padding: 20,
                    borderRadius: 12,
                    textAlign: 'center',
                    marginBottom: 20,
                    background: registeredResult.status === 'Placed' ? '#F0FDF4' : '#FEF2F2',
                    border: `1.5px solid ${registeredResult.status === 'Placed' ? '#86EFAC' : '#FECACA'}`,
                  }}
                >
                  <div style={{ fontSize: '1.6rem', fontWeight: 900, color: registeredResult.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                    {registeredResult.status === 'Placed' ? '✓ PLACED' : '⚠️ NOT PLACED'} ({registeredResult.probability_percent}%)
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 4 }}>
                    Model: <b>{registeredResult.model_name}</b> &bull; Readiness: <b>{registeredResult.readiness_level}</b>
                  </div>
                </div>

                {/* Faculty Feedback Form */}
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, margin: '0 0 12px 0', color: 'var(--text-main)' }}>
                  Record Official Faculty Feedback
                </h4>
                <form onSubmit={handleSaveFeedback}>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>
                      Verdict:
                    </label>
                    <select
                      className="input-field"
                      value={feedbackStatus}
                      onChange={(e) => setFeedbackStatus(e.target.value)}
                    >
                      <option value="High Potential">High Potential</option>
                      <option value="Placed">Placed</option>
                      <option value="At Risk">At Risk (Needs Mentorship)</option>
                      <option value="Not Placed">Not Placed</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: 14 }}>
                    <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>
                      Advisory Notes (Visible to Student):
                    </label>
                    <textarea
                      className="input-field"
                      rows={3}
                      value={feedbackNotes}
                      onChange={(e) => setFeedbackNotes(e.target.value)}
                      placeholder="e.g. Focus on graph algorithms and improve mock interview communication before next week's campus drive."
                      required
                    />
                  </div>

                  {feedbackSuccess && (
                    <div style={{ padding: 10, borderRadius: 6, background: '#DCFCE7', color: '#166534', fontSize: '0.85rem', marginBottom: 12 }}>
                      ✓ Feedback recorded and synchronized to student's portal!
                    </div>
                  )}

                  <button type="submit" className="btn-secondary" style={{ width: '100%' }}>
                    <Save size={16} /> Save Feedback to Student Profile
                  </button>
                </form>
              </div>
            ) : (
              <div className="campus-card" style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                <Target size={40} style={{ opacity: 0.3, marginBottom: 12 }} />
                <p>Select a candidate and click "Evaluate Candidate Placement" to generate predictive insights.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 2: Ad-Hoc Profile */}
      {activeTab === 'adhoc' && (
        <form onSubmit={handleRunAdHocPredict} className="campus-card" style={{ marginBottom: 24 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
            Ad-Hoc Candidate Feature Input
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 20 }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Gender</label>
              <select className="input-field" value={adHocForm.gender} onChange={(e) => setAdHocForm({ ...adHocForm, gender: e.target.value })}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Branch</label>
              <select className="input-field" value={adHocForm.branch} onChange={(e) => setAdHocForm({ ...adHocForm, branch: e.target.value })}>
                <option value="CSE">CSE</option>
                <option value="IT">IT</option>
                <option value="ECE">ECE</option>
                <option value="EE">EE</option>
                <option value="MECH">MECH</option>
                <option value="CIVIL">CIVIL</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>CGPA</label>
              <input type="number" step="0.01" min="0" max="10" className="input-field" value={adHocForm.cgpa} onChange={(e) => setAdHocForm({ ...adHocForm, cgpa: parseFloat(e.target.value) })} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Backlogs</label>
              <input type="number" min="0" max="10" className="input-field" value={adHocForm.backlogs} onChange={(e) => setAdHocForm({ ...adHocForm, backlogs: parseInt(e.target.value) })} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Attendance %</label>
              <input type="number" min="0" max="100" className="input-field" value={adHocForm.attendance_percentage} onChange={(e) => setAdHocForm({ ...adHocForm, attendance_percentage: parseFloat(e.target.value) })} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>DSA Solved</label>
              <input type="number" min="0" max="1000" className="input-field" value={adHocForm.dsa_problems_solved} onChange={(e) => setAdHocForm({ ...adHocForm, dsa_problems_solved: parseInt(e.target.value) })} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Aptitude (0-100)</label>
              <input type="number" min="0" max="100" className="input-field" value={adHocForm.aptitude_score} onChange={(e) => setAdHocForm({ ...adHocForm, aptitude_score: parseFloat(e.target.value) })} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>Coding (0-10)</label>
              <input type="number" step="0.1" min="0" max="10" className="input-field" value={adHocForm.coding_skill_score} onChange={(e) => setAdHocForm({ ...adHocForm, coding_skill_score: parseFloat(e.target.value) })} />
            </div>
          </div>

          <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
            <button type="submit" disabled={loading} className="btn-primary" style={{ flex: 1 }}>
              <Target size={16} /> {loading ? 'Evaluating...' : 'Predict Ad-Hoc Outcome'}
            </button>
          </div>

          {adHocResult && (
            <div
              style={{
                marginTop: 20,
                padding: 20,
                borderRadius: 12,
                background: adHocResult.status === 'Placed' ? '#F0FDF4' : '#FEF2F2',
                border: `1.5px solid ${adHocResult.status === 'Placed' ? '#86EFAC' : '#FECACA'}`,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <div>
                <div style={{ fontSize: '1.4rem', fontWeight: 900, color: adHocResult.status === 'Placed' ? '#16A34A' : '#DC2626' }}>
                  {adHocResult.status === 'Placed' ? '✓ Likely Placed' : '⚠️ Unlikely Placed'} ({adHocResult.probability_percent}%)
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  Readiness: <b>{adHocResult.readiness_level}</b> &bull; Evaluated using {adHocResult.model_name}
                </div>
              </div>
            </div>
          )}
        </form>
      )}

      {/* Tab 3: Batch CSV Scoring */}
      {activeTab === 'batch' && (
        <div className="campus-card" style={{ marginBottom: 24 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
            Automated Roster Scoring via CSV
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: 20 }}>
            Upload a departmental candidate list (CSV) with standard feature columns (e.g. cgpa, dsa_problems_solved, aptitude_score) to score all candidates in a single high-throughput batch.
          </p>

          <form onSubmit={handleBatchUpload} style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 24 }}>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setBatchFile(e.target.files[0])}
              style={{ border: '1px solid #CBD5E1', padding: '8px 12px', borderRadius: 8, fontSize: '0.9rem', flex: 1 }}
              required
            />
            <button type="submit" disabled={loading || !batchFile} className="btn-primary">
              <Upload size={16} /> {loading ? 'Scoring Roster...' : 'Score Batch Roster'}
            </button>
          </form>

          {batchResult && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 20 }}>
                <div className="campus-card" style={{ textAlign: 'center', padding: 16 }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Total Candidates</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-main)' }}>{batchResult.total}</div>
                </div>
                <div className="campus-card" style={{ textAlign: 'center', padding: 16, borderLeft: '4px solid var(--success)' }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Predicted Placed</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--success)' }}>{batchResult.placed_count}</div>
                </div>
                <div className="campus-card" style={{ textAlign: 'center', padding: 16, borderLeft: '4px solid var(--primary)' }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Batch Placement Ratio</div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--primary)' }}>
                    {((batchResult.placed_count / batchResult.total) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              <div style={{ overflowX: 'auto' }}>
                <table className="campus-table">
                  <thead>
                    <tr>
                      <th>Candidate ID / Name</th>
                      <th>Branch</th>
                      <th>CGPA</th>
                      <th>Prediction</th>
                      <th>Confidence</th>
                      <th>Readiness Tier</th>
                    </tr>
                  </thead>
                  <tbody>
                    {batchResult.records.map((r, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: 600 }}>{r.name || r.student_id || `Candidate #${i + 1}`}</td>
                        <td>{r.branch || 'CSE'}</td>
                        <td>{r.cgpa || '-'}</td>
                        <td>
                          <span className={`badge ${r.Predicted_Placement === 'Placed' ? 'badge-green' : 'badge-red'}`}>
                            {r.Predicted_Placement}
                          </span>
                        </td>
                        <td>{r.Confidence}</td>
                        <td>{r.Readiness_Tier}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Academic Justification */}
      <AcademicJustification
        title="Predictive Scoring Center & Batch Inference Justification"
        algorithmRationale="The Prediction Center serves as the operational inference engine bridging trained statistical learning models with live administrative decision-making. By allowing placement officers to evaluate individual candidates or execute batch inference across external rosters, the platform verifies model generalization on out-of-sample data. Multiple model choices (Random Forest, Decision Trees, and Naive Bayes) allow administrators to cross-validate marginal predictions against both complex ensemble aggregations and transparent rule trees."
        institutionalImpact="Enables early proactive intervention before recruitment drives commence. Placement directors can rapidly score entire departmental cohorts to identify students needing urgent skill bootcamps, mock interviews, or aptitude training, converting retrospective placement reports into forward-looking guidance."
        dwmConcepts="Supervised Model Inference, Out-of-sample Generalization, Threshold Calibration, Batch Matrix Feature Engineering, Direct Actionable Prescriptive Analytics."
      />
    </div>
  );
}
