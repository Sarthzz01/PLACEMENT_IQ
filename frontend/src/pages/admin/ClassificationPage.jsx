import React, { useEffect, useState } from 'react';
import { GitBranch, Shield, Zap, Award } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function ClassificationPage() {
  const [data, setData] = useState(null);
  const [selectedModel, setSelectedModel] = useState('Random Forest');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/classification')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Evaluating classification models...</div>;

  const currentArt = data?.artifacts?.[selectedModel];
  const cm = currentArt?.confusion_matrix || [[0, 0], [0, 0]];
  const featImp = currentArt?.feature_importance || [];

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Supervised Placement Classification</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Evaluate and benchmark production classifiers across accuracy, precision, recall, and ROC-AUC metrics.
        </p>
      </div>

      {/* Model Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '18px', marginBottom: '24px' }}>
        {[
          { name: 'Random Forest', type: 'Ensemble Learning', icon: <Shield size={20} color="#2563EB" />, badge: 'Recommended', acc: '~86.5%' },
          { name: 'Decision Tree', type: 'Interpretable White-Box', icon: <GitBranch size={20} color="#16A34A" />, badge: 'White-Box Rules', acc: '~81.4%' },
          { name: 'Naive Bayes', type: 'Probabilistic Baseline', icon: <Zap size={20} color="#9333EA" />, badge: 'Bayesian Prior', acc: '~80.9%' }
        ].map(m => (
          <div
            key={m.name}
            className="campus-card"
            style={{
              cursor: 'pointer',
              borderColor: selectedModel === m.name ? 'var(--primary)' : 'var(--border)',
              boxShadow: selectedModel === m.name ? 'var(--shadow-blue)' : 'var(--shadow-sm)',
              transition: 'all 0.2s'
            }}
            onClick={() => setSelectedModel(m.name)}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {m.icon}
                <strong style={{ color: 'var(--navy)', fontSize: '1.05rem' }}>{m.name}</strong>
              </div>
              <span className="badge badge-role" style={{ fontSize: '0.7rem' }}>{m.badge}</span>
            </div>
            <div style={{ fontSize: '0.8rem', color: '#64748B', marginBottom: '12px' }}>{m.type}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #F1F5F9', paddingTop: '10px' }}>
              <span style={{ fontSize: '0.82rem', color: '#64748B' }}>Benchmark Accuracy:</span>
              <span style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--primary)' }}>{m.acc}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics Comparison Table */}
      <div className="campus-card">
        <div className="campus-card-header">
          <div className="card-title">Comprehensive Classifier Performance Benchmark</div>
          <span className="badge badge-role">Stratified 80/20 Test Split</span>
        </div>

        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Classifier Model</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1 Score</th>
                <th>ROC AUC</th>
              </tr>
            </thead>
            <tbody>
              {data?.metrics?.map((row, i) => (
                <tr key={i} style={{ background: row.Model === selectedModel ? '#EFF6FF' : 'transparent' }}>
                  <td style={{ fontWeight: 700, color: '#0F172A' }}>{row.Model}</td>
                  <td style={{ fontWeight: 700, color: 'var(--primary)' }}>{((row.Accuracy ?? 0) * 100).toFixed(1)}%</td>
                  <td>{(row.Precision ?? 0).toFixed(3)}</td>
                  <td>{(row.Recall ?? 0).toFixed(3)}</td>
                  <td>{(row.F1 ?? 0).toFixed(3)}</td>
                  <td style={{ fontWeight: 600 }}>{(row['ROC-AUC'] ?? row['ROC AUC'] ?? 0).toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Model Deep Dive: Confusion Matrix & Feature Importance */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        {/* Confusion Matrix Card */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Confusion Matrix ({selectedModel})</div>
            <span className="badge badge-role">Test Evaluation</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: '16px' }}>
            <div style={{ background: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#16A34A', fontWeight: 700 }}>True Negatives</div>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#16A34A', margin: '4px 0' }}>{cm?.[0]?.[0] ?? 0}</div>
              <div style={{ fontSize: '0.75rem', color: '#64748B' }}>Correctly Not Placed</div>
            </div>
            <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#DC2626', fontWeight: 700 }}>False Positives</div>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#DC2626', margin: '4px 0' }}>{cm?.[0]?.[1] ?? 0}</div>
              <div style={{ fontSize: '0.75rem', color: '#64748B' }}>Type I Error</div>
            </div>
            <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#DC2626', fontWeight: 700 }}>False Negatives</div>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#DC2626', margin: '4px 0' }}>{cm?.[1]?.[0] ?? 0}</div>
              <div style={{ fontSize: '0.75rem', color: '#64748B' }}>Type II Error</div>
            </div>
            <div style={{ background: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#16A34A', fontWeight: 700 }}>True Positives</div>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#16A34A', margin: '4px 0' }}>{cm?.[1]?.[1] ?? 0}</div>
              <div style={{ fontSize: '0.75rem', color: '#64748B' }}>Correctly Placed</div>
            </div>
          </div>
        </div>

        {/* Feature Importance Bar Chart */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Top Predictive Attributes ({selectedModel})</div>
            <span className="badge badge-role">MDI Splitting Weights</span>
          </div>

          {featImp.length > 0 ? (
            <div style={{ height: '240px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featImp.slice(0, 6)} layout="vertical" margin={{ left: 25, right: 20 }}>
                  <XAxis type="number" stroke="#64748B" />
                  <YAxis dataKey="Feature" type="category" stroke="#64748B" width={110} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="Importance" fill="#2563EB" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div style={{ padding: '36px', textAlign: 'center', color: '#64748B' }}>
              Feature importance is derived from tree-based splitting algorithms.
            </div>
          )}
        </div>
      </div>

      {/* Academic Justification */}
      <AcademicJustification
        title="Comparative Supervised Classification Framework"
        algorithmName="Random Forest • Decision Tree • Gaussian Naive Bayes"
        whyUsed={[
          ["Random Forest for Production Generalization", "As an ensemble of 150 bootstrapped decision trees, Random Forest aggregates orthogonal feature subspaces, reducing variance and neutralizing individual decision tree overfitting. In campus placement datasets where non-linear interactions between CGPA, DSA problem counts, and internship pedigree determine outcomes, Random Forest achieves peak generalization (~86.5% accuracy) with robust ROC-AUC (~0.93)."],
          ["Decision Tree for White-Box Explainability", "Decision trees produce an explicit, hierarchical set of human-interpretable boolean decision rules (e.g. If CGPA >= 7.5 and DSA >= 60 then Placed). In an academic institution, black-box models are unacceptable for student counselling; Decision Trees provide transparent, actionable rationales that placement coordinators can directly explain to students."],
          ["Gaussian Naive Bayes as a Probabilistic Baseline", "Naive Bayes applies Bayes' Theorem under the conditional class-independence assumption. While real-world student features correlate, Naive Bayes serves as an essential rapid, low-variance benchmark. Its calibrated posterior class probabilities confirm whether more computationally demanding non-linear algorithms deliver statistically significant accuracy gains."]
        ]}
        institutionalImpact="Enables placement officers to deploy Random Forest as the high-accuracy automated scoring engine while using Decision Tree feature splits to establish clear departmental eligibility benchmarks (e.g., minimum project count and mock interview thresholds) that maximize campus-wide placement conversion."
        dwmConcept="Supervised Learning, Information Gain (Gini Impurity / Entropy), Bagging & Variance Reduction, Posterior Class Probability Estimation."
      />
    </div>
  );
}
