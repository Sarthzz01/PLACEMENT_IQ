import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function DataMining() {
  const [data, setData] = useState(null);
  const [activeTab, setActiveTab] = useState('correlation');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/data-mining')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Mining patterns from student dataset...</div>;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Data Mining & Pattern Discovery</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Uncover latent behavioral correlations, non-linear dependencies, tree-based feature importances, and Apriori association rules.
        </p>
      </div>

      <div className="tabs-container">
        {[
          { id: 'correlation', label: '1. Pearson Correlation' },
          { id: 'mutual_info', label: '2. Mutual Information' },
          { id: 'importance', label: '3. Tree Feature Importance' },
          { id: 'association', label: '4. Association Rules (Apriori)' }
        ].map(t => (
          <button
            key={t.id}
            className={`tab-btn ${activeTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {activeTab === 'correlation' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Pearson Correlation Matrix (Target: placement_prediction)</div>
            <span className="badge badge-role">Linear Associations</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Feature Dimension</th>
                    <th>Correlation (r)</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.correlation?.map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 600 }}>{row.Feature}</td>
                      <td style={{ fontWeight: 700, color: row.Correlation > 0 ? '#2563EB' : '#DC2626' }}>
                        {row.Correlation.toFixed(3)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ height: '320px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data?.correlation?.slice(0, 8)} layout="vertical" margin={{ left: 30, right: 20 }}>
                  <XAxis type="number" stroke="#64748B" />
                  <YAxis dataKey="Feature" type="category" stroke="#64748B" width={120} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="Correlation" fill="#2563EB" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'mutual_info' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Mutual Information Ranking (Non-Linear Dependencies)</div>
            <span className="badge badge-role">Information Gain</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Feature Dimension</th>
                    <th>Mutual Information (nats)</th>
                  </tr>
                </thead>
                <tbody>
                  {(data?.mutual_info || data?.mutual_information || []).map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 600 }}>{row.Feature}</td>
                      <td style={{ fontWeight: 700, color: '#2563EB' }}>
                        {(Number(row['Mutual Information'] ?? 0)).toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ height: '320px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={(data?.mutual_info || data?.mutual_information || []).slice(0, 8)} layout="vertical" margin={{ left: 30, right: 20 }}>
                  <XAxis type="number" stroke="#64748B" />
                  <YAxis dataKey="Feature" type="category" stroke="#64748B" width={120} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="Mutual Information" fill="#60A5FA" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'importance' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Random Forest Gini Impurity Feature Importance (MDI)</div>
            <span className="badge badge-role">Ensemble Weights</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Feature</th>
                    <th>Gini Importance</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.feature_importance?.map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 600 }}>{row.Feature}</td>
                      <td style={{ fontWeight: 700, color: '#16A34A' }}>
                        {(Number(row.Importance ?? 0)).toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ height: '320px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data?.feature_importance?.slice(0, 8)} layout="vertical" margin={{ left: 30, right: 20 }}>
                  <XAxis type="number" stroke="#64748B" />
                  <YAxis dataKey="Feature" type="category" stroke="#64748B" width={120} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="Importance" fill="#16A34A" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'association' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Association Rules (Apriori Pattern Mining)</div>
            <span className="badge badge-role">Frequent Itemsets</span>
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Antecedent (Condition)</th>
                  <th>Consequent (Outcome)</th>
                  <th>Support</th>
                  <th>Confidence</th>
                  <th>Lift Ratio</th>
                </tr>
              </thead>
              <tbody>
                {data?.association_rules?.map((rule, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 600, color: '#0F172A' }}>{rule.antecedents}</td>
                    <td style={{ color: 'var(--primary)', fontWeight: 700 }}>{rule.consequents}</td>
                    <td>{(Number(rule.support ?? 0) * 100).toFixed(1)}%</td>
                    <td>{(Number(rule.confidence ?? 0) * 100).toFixed(1)}%</td>
                    <td style={{ fontWeight: 700, color: (rule.lift ?? 0) > 1.2 ? '#16A34A' : '#0F172A' }}>
                      {(Number(rule.lift ?? 0)).toFixed(2)}x
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Academic Justification */}
      <AcademicJustification
        title="Multi-Perspective Feature Relevance & Association Discovery"
        algorithmName="Pearson Correlation • Mutual Information • Gini Impurity (MDI) • Association Rules (Apriori)"
        whyUsed={[
          ["Triangulation of Linear and Non-Linear Signals", "Standard statistical methods often rely exclusively on linear Pearson correlation (r), which fails to detect complex non-linear or threshold-driven educational dependencies. By computing non-parametric Mutual Information (quantifying shared entropy I(X;Y)) alongside Pearson coefficients, we uncover subtle non-linear dependencies that standard correlation overlooks."],
          ["Mean Decrease in Impurity (MDI) Feature Importance", "Using an ensemble of 120 decision trees, Gini Importance measures the exact average reduction in node impurity achieved by splitting on each candidate attribute. This isolates the true predictive drivers of placement readiness, preventing placement cells from over-indexing on superficial markers."],
          ["Association Rule Mining for Prescriptive Curricular Bundles", "Applying the Apriori principle on binned student credentials computes Support, Confidence, and Lift for co-occurring success criteria (e.g. {DSA >= 70, Projects >= 3} → {Placed} with Lift > 1.4). Unlike point predictions, association rules provide easily intelligible, prescriptive roadmaps that students can directly execute."]
        ]}
        institutionalImpact="Enables university academic committees to audit their engineering syllabus with empirical evidence, identifying which co-curricular activities directly contribute to placement success and which outdated prerequisites should be modernized."
        dwmConcept="Feature Selection, Information Theory (Mutual Information / Entropy Gain), Gini Impurity Reduction, Association Rule Mining (Support, Confidence, Lift)."
      />
    </div>
  );
}
