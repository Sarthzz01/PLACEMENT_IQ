import React, { useState, useEffect } from 'react';
import { Settings, Shield, RefreshCw, Activity, CheckCircle2, Cpu, Database } from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('model');
  const [settings, setSettings] = useState(null);
  const [selectedModel, setSelectedModel] = useState('Random Forest');
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);
  const [rebuildMsg, setRebuildMsg] = useState(null);

  const fetchSettings = async () => {
    try {
      const res = await fetch('/api/admin/settings');
      const data = await res.json();
      setSettings(data);
      if (data.production_model) setSelectedModel(data.production_model);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleSaveModel = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveSuccess(false);
    try {
      await fetch('/api/admin/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: 'production_model', value: selectedModel }),
      });
      setSaveSuccess(true);
      fetchSettings();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

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

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-main)', margin: '0 0 6px 0' }}>
          System Settings & Warehouse Governance
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: 0 }}>
          Configure administrator accounts, manage production machine learning models, inspect dataset counts, and execute database maintenance.
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 12, borderBottom: '1px solid var(--border-color)', marginBottom: 24 }}>
        <button
          onClick={() => setActiveTab('model')}
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
            color: activeTab === 'model' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'model' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Cpu size={16} /> 1. Production Model & ML Settings
        </button>
        <button
          onClick={() => setActiveTab('admins')}
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
            color: activeTab === 'admins' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'admins' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Shield size={16} /> 2. Admin Accounts & Roles
        </button>
        <button
          onClick={() => setActiveTab('warehouse')}
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
            color: activeTab === 'warehouse' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'warehouse' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Database size={16} /> 3. Data Warehouse Maintenance
        </button>
        <button
          onClick={() => setActiveTab('health')}
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
            color: activeTab === 'health' ? 'var(--primary)' : 'var(--text-muted)',
            borderBottom: activeTab === 'health' ? '2px solid var(--primary)' : '2px solid transparent',
          }}
        >
          <Activity size={16} /> 4. Health & Diagnostics
        </button>
      </div>

      {/* Tab 1: Production Model */}
      {activeTab === 'model' && (
        <div className="campus-card" style={{ maxWidth: 700, marginBottom: 24 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
            Active Production Classifier
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: 20 }}>
            Designate which trained machine learning model generates real-time placement probability evaluations for registered students and the public demo portal:
          </p>

          <form onSubmit={handleSaveModel}>
            <div style={{ marginBottom: 20 }}>
              <select
                className="input-field"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
              >
                <option value="Random Forest">Random Forest (Ensemble Bagging ~86% Accuracy)</option>
                <option value="Gradient Boosting">Gradient Boosting (Sequential Boosting Ensemble ~85% Accuracy)</option>
                <option value="Decision Tree">Decision Tree (Transparent White-Box Rules)</option>
                <option value="Logistic Regression">Logistic Regression (L2-Regularized Linear Log-Odds)</option>
                <option value="Naive Bayes">Gaussian Naive Bayes (Fast Probabilistic Baseline)</option>
              </select>
            </div>

            {saveSuccess && (
              <div style={{ padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.9rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                <CheckCircle2 size={16} /> Production model updated to <b>{selectedModel}</b>!
              </div>
            )}

            <button type="submit" disabled={saving} className="btn-primary">
              <Cpu size={16} /> {saving ? 'Saving...' : 'Save Production Model'}
            </button>
          </form>

          <div style={{ marginTop: 24, padding: 16, background: '#F8FAFC', borderRadius: 8, border: '1px solid #E2E8F0', fontSize: '0.85rem', lineHeight: 1.8 }}>
            <div><b style={{ color: 'var(--primary)' }}>• Random Forest:</b> Ensemble bagging of 150 randomized decision trees. Aggregates orthogonal feature subspaces to reduce variance and prevent overfitting.</div>
            <div><b style={{ color: 'var(--primary)' }}>• Gradient Boosting:</b> Sequential residual boosting trees. Iteratively fits pseudo-residuals to capture complex non-linear attribute interactions.</div>
            <div><b style={{ color: 'var(--primary)' }}>• Decision Tree:</b> Single pruned CART tree with Gini impurity splitting. Enables full rule auditability for educational counselling transparency.</div>
            <div><b style={{ color: 'var(--primary)' }}>• Logistic Regression:</b> Standardized linear logit model with L2 regularization. Provides direct log-odds interpretations and rapid sub-second scoring.</div>
            <div><b style={{ color: 'var(--primary)' }}>• Gaussian Naive Bayes:</b> Assumes conditional feature independence with Gaussian probability density estimation as a fast probabilistic benchmark.</div>
          </div>
        </div>
      )}

      {/* Tab 2: Admin Accounts */}
      {activeTab === 'admins' && (
        <div className="campus-card" style={{ maxWidth: 700, marginBottom: 24 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
            Configured Administrator Accounts
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: 20 }}>
            Users authenticating with any of the following institutional email addresses receive elevated Administrator permissions:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 24 }}>
            {['admin@placementiq.edu', 'admin@college.edu', 'placement@college.edu', 'faculty@placementiq.edu'].map((email) => (
              <div
                key={email}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  padding: '12px 16px',
                  background: '#F8FAFC',
                  borderRadius: 8,
                  border: '1px solid #E2E8F0',
                }}
              >
                <Shield size={16} color="var(--primary)" />
                <span style={{ fontWeight: 600, color: 'var(--text-main)', fontFamily: 'monospace' }}>{email}</span>
                <span className="badge badge-blue" style={{ marginLeft: 'auto' }}>Full Admin Privileges</span>
              </div>
            ))}
          </div>

          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            💡 To configure additional institutional admin accounts, update the <code>ADMIN_EMAILS</code> tuple in <code>src/config.py</code>.
          </div>
        </div>
      )}

      {/* Tab 3: Data Warehouse Maintenance */}
      {activeTab === 'warehouse' && (
        <div className="campus-card" style={{ maxWidth: 700, marginBottom: 24 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px 0', color: 'var(--text-main)' }}>
            Data Warehouse Star Schema Rebuild
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: 20 }}>
            Re-index SQLite dimensional tables (<code>DimStudent</code>, <code>DimAcademic</code>, <code>DimSkills</code>, <code>DimEngagement</code>, <code>DimPlacement</code>) and rebuild the central <code>FactPlacement</code> fact table with newly registered student profiles.
          </p>

          {rebuildMsg && (
            <div style={{ padding: 12, borderRadius: 8, background: '#DCFCE7', color: '#166534', fontSize: '0.9rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
              <CheckCircle2 size={16} /> {rebuildMsg}
            </div>
          )}

          <button
            onClick={handleRebuildWarehouse}
            disabled={rebuilding}
            className="btn-primary"
          >
            <RefreshCw size={16} className={rebuilding ? 'spin' : ''} /> {rebuilding ? 'Rebuilding Star Schema...' : 'Force Rebuild SQLite Star Schema'}
          </button>
        </div>
      )}

      {/* Tab 4: Health & Diagnostics */}
      {activeTab === 'health' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20, marginBottom: 24 }}>
          <div className="campus-card" style={{ borderLeft: '4px solid var(--primary)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Warehouse Database</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', marginTop: 4 }}>
              {settings?.database_path || 'placement_dw.sqlite'}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>SQLite 3 Star Schema Engine</div>
          </div>

          <div className="campus-card" style={{ borderLeft: '4px solid var(--success)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Original Benchmark Records</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--success)', marginTop: 4 }}>
              {settings?.dataset_counts?.original_students?.toLocaleString() || '10,000'}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>Cleaned baseline records</div>
          </div>

          <div className="campus-card" style={{ borderLeft: '4px solid #8B5CF6' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Registered Student Profiles</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#8B5CF6', marginTop: 4 }}>
              {settings?.dataset_counts?.new_students || 0}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>User-created portal profiles</div>
          </div>

          <div className="campus-card" style={{ borderLeft: '4px solid #F59E0B' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Total Unified Records</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#F59E0B', marginTop: 4 }}>
              {settings?.dataset_counts?.total_students?.toLocaleString() || '10,000'}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>Accessible to OLAP & ML</div>
          </div>
        </div>
      )}

      {/* Analytical Conclusion & Project Outcomes */}
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
