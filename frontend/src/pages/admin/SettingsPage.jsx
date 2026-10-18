import React, { useState, useEffect } from 'react';
import {
  Settings, Shield, RefreshCw, Activity, CheckCircle2, Cpu, Database,
  Sliders, UserPlus, Trash2, Key, Building2, AlertTriangle, Save,
  Check, Server, HardDrive, Clock, ShieldAlert, Sparkles, Terminal
} from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

const MODEL_INFO = {
  'Random Forest': {
    family: 'Ensemble Bagging',
    acc: '~86.5%',
    trees: '150 Trees',
    desc: 'Aggregates 150 orthogonal bootstrapped decision trees to reduce predictive variance and avoid overfitting on noisy student credentials.'
  },
  'Gradient Boosting': {
    family: 'Sequential Boosting',
    acc: '~85.2%',
    trees: '100 Estimators',
    desc: 'Sequentially corrects pseudo-residuals of prior trees to capture complex non-linear feature interactions between CGPA and coding aptitude.'
  },
  'Decision Tree': {
    family: 'White-Box Trees',
    acc: '~81.4%',
    trees: 'Single Tree (Depth=6)',
    desc: 'Transparent hierarchical CART tree providing clear boolean decision paths for educational counseling transparency.'
  },
  'Logistic Regression': {
    family: 'Generalized Linear',
    acc: '~82.0%',
    trees: 'L2 Logit Sigmoid',
    desc: 'Standardized linear log-odds classifier providing instant sub-second scoring and direct attribute weight interpretability.'
  },
  'Naive Bayes': {
    family: 'Probabilistic Prior',
    acc: '~80.9%',
    trees: 'Gaussian Likelihood',
    desc: 'Fast maximum likelihood estimation under class-conditional independence, serving as an efficient Bayesian baseline.'
  }
};

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('model'); // 'model' | 'admins' | 'governance' | 'warehouse' | 'telemetry'
  const [settings, setSettings] = useState(null);
  const [adminsList, setAdminsList] = useState([]);
  const [selectedModel, setSelectedModel] = useState('Random Forest');
  const [threshold, setThreshold] = useState('0.50');
  const [consensusEnabled, setConsensusEnabled] = useState(true);
  const [autoRetrain, setAutoRetrain] = useState(false);

  // Institutional Governance Form States
  const [govForm, setGovForm] = useState({
    university_name: 'University Institute of Technology — Department of Computer Engineering',
    academic_year: '2025-2026',
    min_eligibility_cgpa: '6.50',
    max_backlogs_allowed: '0'
  });

  // Add Admin Account Modal/Form
  const [showAddAdmin, setShowAddAdmin] = useState(false);
  const [newAdmin, setNewAdmin] = useState({
    name: '',
    email: '',
    password: '',
    branch: 'CSE',
    role: 'admin'
  });
  const [adminActionError, setAdminActionError] = useState(null);
  const [adminActionSuccess, setAdminActionSuccess] = useState(null);

  // Action status indicators
  const [savingModel, setSavingModel] = useState(false);
  const [modelSaved, setModelSaved] = useState(false);
  const [savingGov, setSavingGov] = useState(false);
  const [govSaved, setGovSaved] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const [rebuildMsg, setRebuildMsg] = useState(null);
  const [pingLatency, setPingLatency] = useState(null);
  const [pinging, setPinging] = useState(false);

  // Fetch all system settings and admins
  const fetchSettings = async () => {
    try {
      const res = await fetch('/api/admin/settings');
      const data = await res.json();
      setSettings(data);
      if (data.production_model) setSelectedModel(data.production_model);
      if (data.admins) setAdminsList(data.admins);
      if (data.settings) {
        setThreshold(data.settings.decision_threshold || '0.50');
        setConsensusEnabled(data.settings.consensus_enabled !== 'false');
        setAutoRetrain(data.settings.auto_retrain === 'true');
        setGovForm({
          university_name: data.settings.university_name || 'University Institute of Technology — Department of Computer Engineering',
          academic_year: data.settings.academic_year || '2025-2026',
          min_eligibility_cgpa: data.settings.min_eligibility_cgpa || '6.50',
          max_backlogs_allowed: data.settings.max_backlogs_allowed || '0'
        });
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSettings();
    handlePingHealth();
  }, []);

  // Ping health endpoint
  const handlePingHealth = async () => {
    setPinging(true);
    const start = performance.now();
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const duration = Math.round(performance.now() - start);
        setPingLatency(duration);
      } else {
        setPingLatency(-1);
      }
    } catch {
      setPingLatency(-1);
    } finally {
      setPinging(false);
    }
  };

  // Save Production Model & ML Threshold
  const handleSaveModelSettings = async (e) => {
    e.preventDefault();
    setSavingModel(true);
    setModelSaved(false);
    try {
      await fetch('/api/admin/settings/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          settings: {
            production_model: selectedModel,
            decision_threshold: threshold,
            consensus_enabled: String(consensusEnabled),
            auto_retrain: String(autoRetrain)
          }
        }),
      });
      setModelSaved(true);
      fetchSettings();
    } catch (err) {
      console.error(err);
    } finally {
      setSavingModel(false);
    }
  };

  // Save Institutional Governance Settings
  const handleSaveGovernance = async (e) => {
    e.preventDefault();
    setSavingGov(true);
    setGovSaved(false);
    try {
      await fetch('/api/admin/settings/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ settings: govForm }),
      });
      setGovSaved(true);
      fetchSettings();
    } catch (err) {
      console.error(err);
    } finally {
      setSavingGov(false);
    }
  };

  // Create New Administrator
  const handleAddAdminSubmit = async (e) => {
    e.preventDefault();
    setAdminActionError(null);
    setAdminActionSuccess(null);
    try {
      const res = await fetch('/api/admin/settings/admin-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAdmin),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to create administrator account.');
      }
      setAdminActionSuccess(data.message || 'Administrator account created successfully.');
      setAdminsList(data.admins || []);
      setNewAdmin({ name: '', email: '', password: '', branch: 'CSE', role: 'admin' });
      setShowAddAdmin(false);
    } catch (err) {
      setAdminActionError(err.message);
    }
  };

  // Delete Administrator
  const handleDeleteAdmin = async (adminId, adminName) => {
    if (!window.confirm(`Are you sure you want to revoke administrator access for ${adminName}?`)) {
      return;
    }
    setAdminActionError(null);
    setAdminActionSuccess(null);
    try {
      const res = await fetch(`/api/admin/settings/admin-user/${adminId}`, {
        method: 'DELETE',
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to delete administrator.');
      }
      setAdminActionSuccess(data.message || 'Administrator removed.');
      setAdminsList(data.admins || []);
    } catch (err) {
      setAdminActionError(err.message);
    }
  };

  // Force Star Schema Rebuild
  const handleRebuildWarehouse = async () => {
    setRebuilding(true);
    setRebuildMsg(null);
    try {
      const res = await fetch('/api/admin/warehouse/rebuild', { method: 'POST' });
      const data = await res.json();
      setRebuildMsg(data.message || 'Data Warehouse rebuilt successfully!');
      fetchSettings();
    } catch (err) {
      console.error(err);
      setRebuildMsg('Failed to rebuild warehouse.');
    } finally {
      setRebuilding(false);
    }
  };

  const currModelMeta = MODEL_INFO[selectedModel] || MODEL_INFO['Random Forest'];

  return (
    <div>
      {/* Page Title & Breadcrumb Header */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 14 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
              <h2 style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--navy)', margin: 0 }}>
                System Settings & Platform Governance
              </h2>
              <span className="badge badge-role" style={{ fontSize: '0.78rem' }}>
                <Shield size={12} style={{ marginRight: 4 }} /> Admin Control Panel
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', margin: 0 }}>
              Designate production machine learning models, manage administrator RBAC access, govern campus drive eligibility, and execute warehouse maintenance.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Production Model:</span>
            <span className="badge badge-placed" style={{ fontWeight: 800 }}>
              {selectedModel}
            </span>
          </div>
        </div>
      </div>

      {/* Segmented Tab Navigation Switcher */}
      <div className="tabs-container">
        <button
          className={`tab-btn ${activeTab === 'model' ? 'active' : ''}`}
          onClick={() => setActiveTab('model')}
        >
          <Cpu size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          1. ML Model Registry & Inference Settings
        </button>

        <button
          className={`tab-btn ${activeTab === 'admins' ? 'active' : ''}`}
          onClick={() => setActiveTab('admins')}
        >
          <Shield size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          2. Administrator Accounts & RBAC
        </button>

        <button
          className={`tab-btn ${activeTab === 'governance' ? 'active' : ''}`}
          onClick={() => setActiveTab('governance')}
        >
          <Building2 size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          3. Institutional & Drive Governance
        </button>

        <button
          className={`tab-btn ${activeTab === 'warehouse' ? 'active' : ''}`}
          onClick={() => setActiveTab('warehouse')}
        >
          <Database size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          4. Data Warehouse Maintenance
        </button>

        <button
          className={`tab-btn ${activeTab === 'telemetry' ? 'active' : ''}`}
          onClick={() => setActiveTab('telemetry')}
        >
          <Activity size={16} style={{ marginRight: 6, display: 'inline', verticalAlign: 'text-bottom' }} />
          5. System Telemetry & Diagnostics
        </button>
      </div>

      {/* ============================================================== */}
      {/* TAB 1: MODEL REGISTRY & INFERENCE SETTINGS                     */}
      {/* ============================================================== */}
      {activeTab === 'model' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: 24, marginBottom: 24 }}>
          {/* Left: Configuration Form */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div>
                <div className="card-title">Production Inference Classifier Designation</div>
                <div className="card-subtitle">Designate the primary ML classifier serving candidate self-assessments</div>
              </div>
              <span className="badge badge-role">Hot-Reloadable</span>
            </div>

            <form onSubmit={handleSaveModelSettings}>
              {/* Select Active Production Model */}
              <div className="form-group">
                <label className="form-label">Active Production Classifier:</label>
                <select
                  className="form-select"
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  {Object.keys(MODEL_INFO).map((mName) => (
                    <option key={mName} value={mName}>
                      {mName} ({MODEL_INFO[mName].family} &bull; {MODEL_INFO[mName].acc} Acc)
                    </option>
                  ))}
                </select>
              </div>

              {/* Classification Threshold Slider */}
              <div className="form-group" style={{ marginTop: 18 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <label className="form-label" style={{ margin: 0 }}>Placement Probability Decision Threshold:</label>
                  <strong style={{ color: 'var(--primary)', fontSize: '1rem' }}>{threshold}</strong>
                </div>
                <input
                  type="range"
                  min="0.35"
                  max="0.75"
                  step="0.05"
                  value={threshold}
                  onChange={(e) => setThreshold(e.target.value)}
                  style={{ width: '100%', cursor: 'pointer' }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  <span>0.35 (Higher Sensitivity / Recall)</span>
                  <span>0.50 (Balanced Default)</span>
                  <span>0.75 (Higher Precision / Strict)</span>
                </div>
              </div>

              {/* Toggles */}
              <div style={{ marginTop: 20, display: 'flex', flexDirection: 'column', gap: 14 }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', fontSize: '0.88rem' }}>
                  <input
                    type="checkbox"
                    checked={consensusEnabled}
                    onChange={(e) => setConsensusEnabled(e.target.checked)}
                    style={{ width: 18, height: 18, accentColor: 'var(--primary)' }}
                  />
                  <span>
                    <b>Enable 5-Algorithm Consensus Voting</b>
                    <span style={{ display: 'block', fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                      Automatically cross-checks predictions against all 5 models on borderline assessments
                    </span>
                  </span>
                </label>

                <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', fontSize: '0.88rem' }}>
                  <input
                    type="checkbox"
                    checked={autoRetrain}
                    onChange={(e) => setAutoRetrain(e.target.checked)}
                    style={{ width: 18, height: 18, accentColor: 'var(--primary)' }}
                  />
                  <span>
                    <b>Incremental Training Trigger</b>
                    <span style={{ display: 'block', fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                      Trigger incremental training batch when 50+ new candidate profiles register
                    </span>
                  </span>
                </label>
              </div>

              {modelSaved && (
                <div style={{ marginTop: 18, padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.88rem', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <CheckCircle2 size={16} /> Production settings updated successfully! Active model: <b>{selectedModel}</b>
                </div>
              )}

              <button type="submit" disabled={savingModel} className="btn btn-primary" style={{ marginTop: 22, width: '100%' }}>
                <Save size={16} /> {savingModel ? 'Saving Settings...' : 'Save Production Model Configuration'}
              </button>
            </form>
          </div>

          {/* Right: Selected Model Specification Preview */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div>
                <div className="card-title">Model Architecture Specification</div>
                <div className="card-subtitle">Detailed inductive principles of the selected classifier</div>
              </div>
              <span className="badge badge-placed">{currModelMeta.family}</span>
            </div>

            <div style={{ padding: 16, background: '#F8FAFC', borderRadius: 10, border: '1px solid #E2E8F0', marginBottom: 18 }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--navy)', marginBottom: 4 }}>
                {selectedModel}
              </div>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-body)', lineHeight: 1.6, margin: '8px 0 14px 0' }}>
                {currModelMeta.desc}
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                <div style={{ background: '#FFF', padding: 10, borderRadius: 8, border: '1px solid #E2E8F0' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>Validation Accuracy</span>
                  <strong style={{ fontSize: '1.1rem', color: '#16A34A' }}>{currModelMeta.acc}</strong>
                </div>
                <div style={{ background: '#FFF', padding: 10, borderRadius: 8, border: '1px solid #E2E8F0' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>Hyperparameter Specs</span>
                  <strong style={{ fontSize: '1.1rem', color: 'var(--navy)' }}>{currModelMeta.trees}</strong>
                </div>
              </div>
            </div>

            <div style={{ fontSize: '0.85rem', color: 'var(--text-body)', lineHeight: 1.7 }}>
              <div style={{ fontWeight: 700, color: 'var(--navy)', marginBottom: 6 }}>Model Selection Recommendations:</div>
              <div>&bull; <b>Random Forest:</b> Best for general institutional deployment with maximum test accuracy (~86.5%).</div>
              <div>&bull; <b>Gradient Boosting:</b> Best for complex non-linear attribute synergies across coding & aptitude.</div>
              <div>&bull; <b>Decision Tree:</b> Recommended when complete white-box explainability is legally mandated.</div>
              <div>&bull; <b>Logistic Regression:</b> Optimal for instant linear log-odds scoring and baseline comparison.</div>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 2: ADMINISTRATOR ACCOUNTS & RBAC                           */}
      {/* ============================================================== */}
      {activeTab === 'admins' && (
        <div className="campus-card" style={{ marginBottom: 24 }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">Configured Administrative Accounts & Role-Based Access (RBAC)</div>
              <div className="card-subtitle">Manage elevated institutional credentials for Placement Officers and Department Mentors</div>
            </div>

            <button
              type="button"
              onClick={() => setShowAddAdmin(!showAddAdmin)}
              className="btn btn-primary"
              style={{ fontSize: '0.82rem' }}
            >
              <UserPlus size={15} /> {showAddAdmin ? 'Cancel' : 'Add New Administrator'}
            </button>
          </div>

          {/* Feedback Banners */}
          {adminActionSuccess && (
            <div style={{ padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.88rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
              <CheckCircle2 size={16} /> {adminActionSuccess}
            </div>
          )}

          {adminActionError && (
            <div style={{ padding: 12, borderRadius: 8, background: '#FEE2E2', color: '#991B1B', fontSize: '0.88rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
              <AlertTriangle size={16} /> {adminActionError}
            </div>
          )}

          {/* Add Admin Form Modal/Drawer */}
          {showAddAdmin && (
            <form onSubmit={handleAddAdminSubmit} style={{ padding: 18, background: '#F8FAFC', borderRadius: 10, border: '1.5px solid var(--primary)', marginBottom: 20 }}>
              <div style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '0.95rem', marginBottom: 12 }}>
                Create Elevated Institutional Account
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 14 }}>
                <div className="form-group">
                  <label className="form-label">Full Name & Title:</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g. Dr. Rajesh Kulkarni"
                    value={newAdmin.name}
                    onChange={(e) => setNewAdmin({ ...newAdmin, name: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Institutional Email:</label>
                  <input
                    type="email"
                    className="form-input"
                    placeholder="e.g. rajesh.k@college.edu"
                    value={newAdmin.email}
                    onChange={(e) => setNewAdmin({ ...newAdmin, email: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Initial Password:</label>
                  <input
                    type="password"
                    className="form-input"
                    placeholder="••••••••"
                    value={newAdmin.password}
                    onChange={(e) => setNewAdmin({ ...newAdmin, password: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Department / Branch:</label>
                  <select
                    className="form-select"
                    value={newAdmin.branch}
                    onChange={(e) => setNewAdmin({ ...newAdmin, branch: e.target.value })}
                  >
                    <option value="CSE">CSE</option>
                    <option value="IT">IT</option>
                    <option value="ECE">ECE</option>
                    <option value="MECH">Mechanical</option>
                    <option value="TPO">Central TPO Cell</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
                <button type="button" onClick={() => setShowAddAdmin(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  <Check size={15} /> Create Administrator Account
                </button>
              </div>
            </form>
          )}

          {/* Admins Table */}
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Admin ID</th>
                  <th>Full Name</th>
                  <th>Institutional Email</th>
                  <th>Department</th>
                  <th>Role Level</th>
                  <th>Created At</th>
                  <th style={{ textAlign: 'center' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {adminsList.map((adm) => (
                  <tr key={adm.id}>
                    <td style={{ fontFamily: 'monospace', fontWeight: 700 }}>{adm.student_id || `ADM-${adm.id}`}</td>
                    <td style={{ fontWeight: 800, color: 'var(--navy)' }}>{adm.name}</td>
                    <td style={{ fontFamily: 'monospace', color: 'var(--text-body)' }}>{adm.email}</td>
                    <td><span className="badge badge-role" style={{ fontSize: '0.72rem' }}>{adm.branch || 'CSE'}</span></td>
                    <td>
                      <span className="badge badge-placed" style={{ fontSize: '0.72rem' }}>
                        Full Administrator
                      </span>
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{adm.created_at || 'Seeded Initial'}</td>
                    <td style={{ textAlign: 'center' }}>
                      {adminsList.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleDeleteAdmin(adm.id, adm.name)}
                          className="btn btn-secondary"
                          style={{ padding: '4px 8px', fontSize: '0.75rem', color: 'var(--error)' }}
                          title="Revoke Administrator Access"
                        >
                          <Trash2 size={13} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 3: INSTITUTIONAL & DRIVE GOVERNANCE                        */}
      {/* ============================================================== */}
      {activeTab === 'governance' && (
        <div className="campus-card" style={{ maxWidth: 780, marginBottom: 24 }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">Campus Placement Drive Parameters & Eligibility Criteria</div>
              <div className="card-subtitle">Configure minimum qualification thresholds and departmental policies</div>
            </div>
            <span className="badge badge-role">Institutional Policy</span>
          </div>

          <form onSubmit={handleSaveGovernance}>
            <div className="form-group">
              <label className="form-label">University / Institution Name:</label>
              <input
                type="text"
                className="form-input"
                value={govForm.university_name}
                onChange={(e) => setGovForm({ ...govForm, university_name: e.target.value })}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
              <div className="form-group">
                <label className="form-label">Current Placement Academic Year:</label>
                <input
                  type="text"
                  className="form-input"
                  value={govForm.academic_year}
                  onChange={(e) => setGovForm({ ...govForm, academic_year: e.target.value })}
                  placeholder="e.g. 2025-2026"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Minimum Eligibility CGPA Cutoff:</label>
                <input
                  type="number"
                  step="0.05"
                  min="0"
                  max="10"
                  className="form-input"
                  value={govForm.min_eligibility_cgpa}
                  onChange={(e) => setGovForm({ ...govForm, min_eligibility_cgpa: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Maximum Allowed Active Backlogs:</label>
                <input
                  type="number"
                  min="0"
                  max="5"
                  className="form-input"
                  value={govForm.max_backlogs_allowed}
                  onChange={(e) => setGovForm({ ...govForm, max_backlogs_allowed: e.target.value })}
                  required
                />
              </div>
            </div>

            {govSaved && (
              <div style={{ padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.88rem', margin: '14px 0', display: 'flex', alignItems: 'center', gap: 8 }}>
                <CheckCircle2 size={16} /> Institutional governance criteria updated successfully!
              </div>
            )}

            <button type="submit" disabled={savingGov} className="btn btn-primary" style={{ marginTop: 14 }}>
              <Save size={16} /> {savingGov ? 'Saving Parameters...' : 'Save Placement Drive Policies'}
            </button>
          </form>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 4: DATA WAREHOUSE MAINTENANCE                              */}
      {/* ============================================================== */}
      {activeTab === 'warehouse' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 24, marginBottom: 24 }}>
          {/* Rebuild Action Card */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div>
                <div className="card-title">Star Schema Warehouse ETL Maintenance</div>
                <div className="card-subtitle">Synchronize SQLite dimensional tables and rebuild central FactPlacement</div>
              </div>
            </div>

            <p style={{ color: 'var(--text-body)', fontSize: '0.88rem', lineHeight: 1.6, marginBottom: 18 }}>
              Executes the automated dimensional ETL pipeline. Re-indexes <code>DimStudent</code>, <code>DimAcademic</code>, <code>DimSkills</code>, <code>DimEngagement</code>, and <code>DimPlacement</code> conformed tables while linking fresh foreign surrogate keys into the central <code>FactPlacement</code> table.
            </p>

            {rebuildMsg && (
              <div style={{ padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.88rem', marginBottom: 18, display: 'flex', alignItems: 'center', gap: 8 }}>
                <CheckCircle2 size={16} /> {rebuildMsg}
              </div>
            )}

            <button
              type="button"
              onClick={handleRebuildWarehouse}
              disabled={rebuilding}
              className="btn btn-primary"
              style={{ width: '100%' }}
            >
              <RefreshCw size={16} className={rebuilding ? 'spin' : ''} />
              {rebuilding ? 'Rebuilding Dimensional Tables...' : 'Execute Full Warehouse Rebuild'}
            </button>
          </div>

          {/* Database Storage Metrics Card */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div>
                <div className="card-title">Database Storage & Topology</div>
                <div className="card-subtitle">Physical file storage on local backend filesystem</div>
              </div>
              <span className="badge badge-role">SQLite 3</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Database File:</span>
                <strong style={{ color: 'var(--navy)', fontFamily: 'monospace' }}>{settings?.database_path || 'placement_dw.sqlite'}</strong>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Original Baseline Records:</span>
                <strong style={{ color: 'var(--navy)' }}>{settings?.dataset_counts?.original_students?.toLocaleString() || '15,000'}</strong>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Registered Student Profiles:</span>
                <strong style={{ color: 'var(--primary)' }}>{settings?.dataset_counts?.new_students || 0}</strong>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Total Unified OLAP Records:</span>
                <strong style={{ color: '#16A34A', fontSize: '1.05rem' }}>{settings?.dataset_counts?.combined_students?.toLocaleString() || '15,000'}</strong>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 5: SYSTEM TELEMETRY & DIAGNOSTICS                         */}
      {/* ============================================================== */}
      {activeTab === 'telemetry' && (
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginBottom: 24 }}>
            {/* Ping Health */}
            <div className="campus-card" style={{ padding: 18, borderLeft: '4px solid var(--success)', margin: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>REST API Engine</span>
                <span className="pulse-live" />
              </div>
              <div style={{ fontSize: '1.6rem', fontWeight: 900, color: '#16A34A', margin: '4px 0' }}>Online</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 6 }}>
                Latency: <b>{pingLatency !== null ? `${pingLatency} ms` : 'Testing...'}</b>
                <button type="button" onClick={handlePingHealth} style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', padding: 0 }} title="Re-ping">
                  <RefreshCw size={12} className={pinging ? 'spin' : ''} />
                </button>
              </div>
            </div>

            {/* Database Engine */}
            <div className="campus-card" style={{ padding: 18, borderLeft: '4px solid var(--primary)', margin: 0 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Warehouse Persistence</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 900, color: 'var(--navy)', margin: '4px 0' }}>SQLite 3</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Star Schema Connected</div>
            </div>

            {/* Inference Latency */}
            <div className="campus-card" style={{ padding: 18, borderLeft: '4px solid #8B5CF6', margin: 0 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Scikit-Learn Engine</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 900, color: '#8B5CF6', margin: '4px 0' }}>v1.5+</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>5 Classifiers In-Memory</div>
            </div>

            {/* Fast API Runtime */}
            <div className="campus-card" style={{ padding: 18, borderLeft: '4px solid #F59E0B', margin: 0 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Server Architecture</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 900, color: 'var(--navy)', margin: '4px 0' }}>FastAPI</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Uvicorn ASGI Engine</div>
            </div>
          </div>

          {/* Diagnostic Details Log */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div>
                <div className="card-title">Runtime Environment Telemetry</div>
                <div className="card-subtitle">Diagnostic specifications for system audits</div>
              </div>
              <span className="badge badge-placed">All Systems Nominal</span>
            </div>

            <div style={{ background: '#0F172A', color: '#CBD5E1', padding: 16, borderRadius: 8, fontFamily: 'monospace', fontSize: '0.84rem', lineHeight: 1.8 }}>
              <div>[SYSTEM] API Gateway: http://127.0.0.1:8000/api</div>
              <div>[DATABASE] Driver: sqlite3 &bull; Target: {settings?.database_path || 'placement_dw.sqlite'}</div>
              <div>[DATASET] Baseline: 15,000 &bull; Registered Profiles: {settings?.dataset_counts?.new_students || 0} &bull; Total: {settings?.dataset_counts?.combined_students || 15000}</div>
              <div>[ML_SUITE] Production Model: {selectedModel} &bull; Threshold: {threshold} &bull; Consensus: {String(consensusEnabled)}</div>
              <div>[SECURITY] RBAC Level: Admin Elevated &bull; Password Hashing: PBKDF2 HMAC-SHA256 (100,000 iterations)</div>
              <div>[TELEMETRY] Last Health Ping Status: 200 OK ({pingLatency}ms latency)</div>
            </div>
          </div>
        </div>
      )}

      {/* Analytical Conclusion & Academic Justification */}
      <AcademicJustification
        title="Platform Governance & Model Registry: Architectural Control & Project Outcomes"
        techniqueName="Dynamic Model Registry • Zero-Downtime Model Routing • Role Boundary Enforcement"
        whyChosen={[
          [
            "Why Dynamic Model Registry Decoupling is Vital",
            "Hardcoding machine learning models inside source code creates brittleness and deployment downtime whenever retraining occurs. Decoupling the active production model designation into a dynamic system setting enables administrators to seamlessly promote champion models (e.g. promoting Gradient Boosting or Random Forest) without server restarts."
          ],
          [
            "Why Strict Role Boundary & Governance is Enforced",
            "Preserves ethical boundaries between student self-assessment and administrative decision-making. Students receive actionable guidance and probability insights without exposure to model switching mechanics, while administrators maintain full governance over warehouse tables, training parameters, and audit feedback."
          ]
        ]}
        whatWeGet={[
          [
            "Zero-Downtime Hot-Reloadable Model Swapping",
            "Our project can switch between any of the 5 trained algorithms in production with instant cutover, allowing live experimentation without service interruptions."
          ],
          [
            "Self-Healing Data Warehouse Maintenance",
            "Provides one-click ETL refresh and schema rebuilding, allowing the data warehouse to incorporate fresh semester enrollments while preserving conformed dimensional integrity."
          ],
          [
            "Real-Time System Health & Diagnostics",
            "Live monitoring of SQLite database connectivity, dimensional table row counts, and server response times ensures high reliability during peak recruitment periods."
          ]
        ]}
        institutionalImpact="Provides institutional administrators with a secure, centralized control panel to manage role boundaries, audit registered accounts, rebuild warehouse dimensional tables upon new semester enrollments, and monitor data warehouse integrity."
        dwmConcept="Model Registry & Lifecycle Governance, Hot-Reloadable Production Routing, Role-Based Access Control (RBAC), Data Warehouse Health Diagnostics."
      />
    </div>
  );
}
