import React, { useEffect, useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function KMeansPage() {
  const [k, setK] = useState(4);
  const [data, setData] = useState(null);
  const [elbowData, setElbowData] = useState([]);
  const [activeTab, setActiveTab] = useState('clusters');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/admin/kmeans?k=${k}`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [k]);

  const loadElbow = () => {
    fetch('/api/admin/kmeans/elbow?k_min=2&k_max=8')
      .then(r => r.json())
      .then(d => setElbowData(d.elbow || []))
      .catch(console.error);
  };

  const colors = ['#2563EB', '#16A34A', '#F59E0B', '#9333EA', '#0F172A', '#06B6D4', '#EC4899', '#84CC16'];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>K-Means Clustering & Archetype Discovery</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Partition student candidates into unsupervised behavioral personas based on academic, problem-solving, and soft-skill attributes.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 700, color: '#334155' }}>Clusters (K):</label>
          <select className="form-select" style={{ width: '80px' }} value={k} onChange={e => setK(parseInt(e.target.value))}>
            {[2, 3, 4, 5, 6, 7, 8].map(num => <option key={num} value={num}>{num}</option>)}
          </select>
        </div>
      </div>

      <div className="tabs-container">
        <button className={`tab-btn ${activeTab === 'clusters' ? 'active' : ''}`} onClick={() => setActiveTab('clusters')}>
          1. 2D PCA Space & Personas
        </button>
        <button className={`tab-btn ${activeTab === 'elbow' ? 'active' : ''}`} onClick={() => { setActiveTab('elbow'); loadElbow(); }}>
          2. Elbow WCSS Curve
        </button>
        <button className={`tab-btn ${activeTab === 'centroids' ? 'active' : ''}`} onClick={() => setActiveTab('centroids')}>
          3. Cluster Centroids
        </button>
      </div>

      {loading ? (
        <div style={{ padding: '40px', color: '#64748B' }}>Optimizing K-Means centroids...</div>
      ) : (
        <>
          {activeTab === 'clusters' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px', marginBottom: '24px' }}>
              {/* PCA Scatter Chart */}
              <div className="campus-card">
                <div className="campus-card-header">
                  <div className="card-title">2D PCA Hyperspace Projection (K={k})</div>
                  <span className="badge badge-role">Silhouette: {data?.silhouette}</span>
                </div>

                <div style={{ height: '330px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                      <CartesianGrid stroke="#F1F5F9" />
                      <XAxis type="number" dataKey="PCA1" name="PC 1" stroke="#64748B" />
                      <YAxis type="number" dataKey="PCA2" name="PC 2" stroke="#64748B" />
                      <Tooltip />
                      <Scatter name="Students" data={data?.pca_sample || []} fill="#2563EB" opacity={0.7} />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Cluster Size Donut */}
              <div className="campus-card">
                <div className="campus-card-header">
                  <div className="card-title">Student Cohort Balance Across Clusters</div>
                  <span className="badge badge-role">K={k} Partitions</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '180px' }}>
                  <ResponsiveContainer width="60%" height="100%">
                    <PieChart>
                      <Pie data={data?.cluster_sizes || []} cx="50%" cy="50%" innerRadius={45} outerRadius={70} dataKey="Count" nameKey="Cluster">
                        {(data?.cluster_sizes || []).map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="table-container" style={{ marginTop: '12px' }}>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Cluster ID</th>
                        <th>Student Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data?.cluster_sizes?.map((c, i) => (
                        <tr key={i}>
                          <td style={{ fontWeight: 700, color: colors[i % colors.length] }}>{c.Cluster}</td>
                          <td>{c.Count?.toLocaleString?.() ?? c.Count ?? 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'elbow' && (
            <div className="campus-card" style={{ marginBottom: '24px' }}>
              <div className="campus-card-header">
                <div className="card-title">Elbow Method: Within-Cluster Sum of Squares (WCSS) vs K</div>
                <span className="badge badge-role">Inertia Inflection</span>
              </div>

              {elbowData.length > 0 ? (
                <div style={{ height: '340px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={elbowData} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis dataKey="k" stroke="#64748B" label={{ value: 'Number of Clusters (K)', position: 'insideBottom', offset: -5 }} />
                      <YAxis stroke="#64748B" />
                      <Tooltip />
                      <Line type="monotone" dataKey="inertia" stroke="#2563EB" strokeWidth={3} dot={{ r: 6, fill: '#2563EB' }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div style={{ padding: '36px', textAlign: 'center', color: '#64748B' }}>Computing inertia curve across K=2 to K=8...</div>
              )}
            </div>
          )}

          {activeTab === 'centroids' && (
            <div className="campus-card" style={{ marginBottom: '24px' }}>
              <div className="campus-card-header">
                <div className="card-title">Cluster Profile Centroids (Mean Feature Values)</div>
                <span className="badge badge-role">Attribute Averages</span>
              </div>

              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      {data?.profile?.length > 0 && Object.keys(data.profile[0]).map(k => <th key={k}>{k}</th>)}
                    </tr>
                  </thead>
                  <tbody>
                    {data?.profile?.map((row, i) => (
                      <tr key={i}>
                        {Object.values(row).map((v, j) => (
                          <td key={j} style={{ fontWeight: j === 0 ? 700 : 400 }}>
                            {typeof v === 'number' ? v.toFixed(2) : String(v)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {/* Analytical Conclusion & Project Outcomes */}
      <AcademicJustification
        title="Unsupervised Cohort Segmentation: K-Means Rationale & Project Outcomes"
        techniqueName="K-Means Partitional Clustering with Elbow Method & Silhouette Validation"
        whyChosen={[
          [
            "Why Unsupervised K-Means is Used Alongside Classification",
            "Supervised classifiers depend on historical placement labels, which may be biased by external hiring market fluctuations. K-Means operates without labels, partitioning the 15,000+ student feature space strictly by Euclidean distance into natural, unbiased competency archetypes."
          ],
          [
            "Why Elbow Inertia & Silhouette Coefficients are Combined",
            "Instead of guessing K, our system combines Within-Cluster Sum of Squares (Inertia Elbow) with Silhouette boundary cohesion analysis, identifying mathematically optimal natural student cluster counts."
          ],
          [
            "Why 2D PCA Dimensionality Reduction is Applied",
            "Student records span over 10 continuous and discrete dimensions. Fitting 2D Principal Component Analysis (PCA) captures the primary directions of variance, allowing administrators to visually inspect cluster separation, overlaps, and transitional candidates."
          ]
        ]}
        whatWeGet={[
          [
            "Actionable Student Personas & Behavioral Archetypes",
            "Our project discovers distinct student clusters: 'High Academic / Needs Coding Practice', 'Balanced High-Performers', and 'At-Risk Low Engagement'."
          ],
          [
            "Personalized Group Interventions vs Generic Seminars",
            "Enables placement deans to route specific clusters into tailored interventions (e.g., intensive DSA bootcamps for Cluster 1, leadership & mock interview training for Cluster 3)."
          ],
          [
            "Objective Centroid Benchmarks for Student Growth",
            "Provides mathematical centroid coordinate profiles that define clear target milestones for students striving to advance into top-tier placement cohorts."
          ]
        ]}
        institutionalImpact="Enables placement training deans to discard one-size-fits-all training curricula in favor of personalized group interventions—for example, routing Cluster 1 ('Academic Learners') into intensive coding bootcamps while directing Cluster 3 ('High Practical Coders') into leadership and communication development."
        dwmConcept="Partitional Clustering, Lloyd's Centroid Iteration, Within-Cluster Sum of Squares (WCSS), Silhouette Cohesion-Separation, Principal Component Analysis (PCA)."
      />
    </div>
  );
}
