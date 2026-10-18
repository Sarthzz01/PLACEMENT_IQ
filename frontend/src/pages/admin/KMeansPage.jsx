import React, { useEffect, useState } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, LineChart, Line, PieChart, Pie, Cell, Legend
} from 'recharts';
import {
  Layers, Filter, Sparkles, Award, Cpu, CheckCircle2,
  AlertTriangle, Users, TrendingUp, Info
} from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

const CLUSTER_COLORS = [
  '#2563EB', // Cluster 0: Royal Blue
  '#16A34A', // Cluster 1: Emerald Green
  '#D97706', // Cluster 2: Warm Amber
  '#9333EA', // Cluster 3: Vivid Purple
  '#E11D48', // Cluster 4: Crimson Rose
  '#0891B2', // Cluster 5: Deep Cyan
  '#EA580C', // Cluster 6: Sunset Orange
  '#4F46E5', // Cluster 7: Indigo
];

// Helper to derive human-readable archetypes from cluster centroid statistics
const getClusterPersona = (clusterId, profileRows) => {
  if (!profileRows || !profileRows[clusterId]) {
    const defaultLabels = [
      'Day-1 Product Achievers',
      'High Practical Coders',
      'Academic Core Discipline',
      'At-Risk / Needs Intervention',
      'Emerging Problem Solvers',
      'Specialized Competency',
      'General Technical Cohort',
      'Foundational Candidates'
    ];
    return defaultLabels[clusterId % defaultLabels.length];
  }
  
  const row = profileRows[clusterId];
  const cgpa = Number(row.cgpa || 0);
  const dsa = Number(row.dsa_questions_solved || 0);
  const coding = Number(row.coding_skill_score || 0);
  const placed = row.placement_prediction !== undefined ? Number(row.placement_prediction) : Number(row.placement_status || 0);

  if (cgpa >= 8.2 && (dsa >= 180 || coding >= 7.5)) return 'Day-1 Product Achievers';
  if (dsa >= 160 || coding >= 7.0) return 'Algorithmic Coders';
  if (cgpa >= 8.0) return 'Academic High Performers';
  if (cgpa <= 6.5 || (row.backlogs !== undefined && Number(row.backlogs) > 1)) return 'At-Risk / Needs Intervention';
  if (placed >= 0.7) return 'Core Placement Ready';
  return `Archetype Tier ${clusterId + 1}`;
};

// Rich custom tooltip for 2D PCA hyperspace scatter points
const CustomScatterTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const pt = payload[0].payload;
    const cId = pt.Cluster !== undefined ? Number(pt.Cluster) : 0;
    const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
    
    return (
      <div style={{
        background: 'rgba(15, 23, 42, 0.96)',
        color: '#FFFFFF',
        padding: '12px 16px',
        borderRadius: 8,
        fontSize: '0.82rem',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.35)',
        border: `2px solid ${color}`,
        minWidth: 190
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: color, display: 'inline-block' }} />
          <strong style={{ color: color, fontSize: '0.9rem' }}>
            {pt.isCentroid ? `★ Centroid: Cluster ${cId}` : `Cluster ${cId}`}
          </strong>
        </div>
        <div style={{ color: '#E2E8F0', lineHeight: 1.6 }}>
          <div><b>PC 1:</b> {Number(pt.PCA1 ?? pt.PC1 ?? 0).toFixed(2)}</div>
          <div><b>PC 2:</b> {Number(pt.PCA2 ?? pt.PC2 ?? 0).toFixed(2)}</div>
          {pt.branch && <div><b>Branch:</b> {pt.branch}</div>}
          {pt.cgpa !== undefined && <div><b>CGPA:</b> {pt.cgpa}</div>}
          {pt.placement_status !== undefined && (
            <div><b>Status:</b> {pt.placement_status === 1 || pt.placement_status === 'Placed' ? '✓ Placed' : '⚠️ Not Placed'}</div>
          )}
        </div>
      </div>
    );
  }
  return null;
};

export default function KMeansPage() {
  const [k, setK] = useState(4);
  const [data, setData] = useState(null);
  const [elbowData, setElbowData] = useState([]);
  const [activeTab, setActiveTab] = useState('clusters');
  const [loading, setLoading] = useState(true);
  const [selectedClusterFilter, setSelectedClusterFilter] = useState('ALL');

  useEffect(() => {
    setLoading(true);
    setSelectedClusterFilter('ALL');
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

  const totalStudents = (data?.cluster_sizes || []).reduce((acc, curr) => acc + (curr.Count || 0), 0);

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>K-Means Clustering & Archetype Discovery</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Partition student candidates into unsupervised behavioral personas based on academic, problem-solving, and soft-skill attributes.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 700, color: '#334155' }}>Clusters (K):</label>
          <select
            className="form-select"
            style={{ width: '80px', fontWeight: 700 }}
            value={k}
            onChange={e => setK(parseInt(e.target.value))}
          >
            {[2, 3, 4, 5, 6, 7, 8].map(num => <option key={num} value={num}>{num}</option>)}
          </select>
        </div>
      </div>

      {/* Tabs */}
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
        <div style={{ padding: '40px', color: '#64748B', textAlign: 'center' }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>Optimizing K-Means centroids & projecting PCA space...</div>
        </div>
      ) : (
        <>
          {activeTab === 'clusters' && (
            <div>
              {/* Top Banner: Cluster Color Palette & Isolation Filter */}
              <div className="campus-card" style={{ marginBottom: '20px', padding: '16px 20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Filter size={16} color="var(--primary)" />
                    <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--navy)' }}>Filter / Focus Cluster:</span>
                  </div>

                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                    <button
                      type="button"
                      onClick={() => setSelectedClusterFilter('ALL')}
                      style={{
                        padding: '6px 14px',
                        borderRadius: 20,
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        border: '1.5px solid',
                        borderColor: selectedClusterFilter === 'ALL' ? 'var(--navy)' : '#CBD5E1',
                        background: selectedClusterFilter === 'ALL' ? 'var(--navy)' : '#FFFFFF',
                        color: selectedClusterFilter === 'ALL' ? '#FFFFFF' : 'var(--text-muted)',
                        transition: 'all 0.15s ease'
                      }}
                    >
                      All Clusters ({data?.pca_sample?.length || 0} Points)
                    </button>

                    {Array.from({ length: k }, (_, cId) => {
                      const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                      const sizeObj = (data?.cluster_sizes || []).find(s => s.Cluster === cId);
                      const isSelected = selectedClusterFilter === cId;
                      return (
                        <button
                          key={cId}
                          type="button"
                          onClick={() => setSelectedClusterFilter(isSelected ? 'ALL' : cId)}
                          style={{
                            padding: '6px 12px',
                            borderRadius: 20,
                            fontSize: '0.78rem',
                            fontWeight: 700,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: 6,
                            border: `2px solid ${color}`,
                            background: isSelected ? color : '#FFFFFF',
                            color: isSelected ? '#FFFFFF' : color,
                            boxShadow: isSelected ? `0 2px 8px ${color}40` : 'none',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <span style={{
                            width: 8,
                            height: 8,
                            borderRadius: '50%',
                            background: isSelected ? '#FFFFFF' : color
                          }} />
                          Cluster {cId} ({sizeObj?.Count || 0})
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Main Grid: Multi-Color PCA Scatter & Cohort Donut */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: '20px', marginBottom: '24px' }}>
                
                {/* Multi-Colored PCA Hyperspace Projection */}
                <div className="campus-card">
                  <div className="campus-card-header">
                    <div>
                      <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span>2D PCA Hyperspace Projection (K={k})</span>
                        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#16A34A', background: '#DCFCE7', padding: '2px 8px', borderRadius: 12 }}>
                          Multi-Color Partition
                        </span>
                      </div>
                      <div className="card-subtitle">
                        Student candidates partitioned into {k} clusters with distinct color spectrum
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <span className="badge" style={{
                        background: '#EFF6FF',
                        color: '#1D4ED8',
                        border: '1px solid #BFDBFE',
                        fontWeight: 800,
                        fontSize: '0.78rem'
                      }}>
                        Silhouette: {data?.silhouette}
                      </span>
                    </div>
                  </div>

                  {/* Multi-Color Recharts Scatter Chart */}
                  <div style={{ height: '420px', width: '100%' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <ScatterChart margin={{ top: 15, right: 20, bottom: 25, left: 10 }}>
                        <CartesianGrid stroke="#F1F5F9" strokeDasharray="3 3" />
                        <XAxis
                          type="number"
                          dataKey="PCA1"
                          name="PC 1"
                          stroke="#64748B"
                          tick={{ fontSize: 11 }}
                          label={{
                            value: 'Principal Component 1 (Academic & Problem Solving Variance)',
                            position: 'insideBottom',
                            offset: -12,
                            fontSize: 11,
                            fill: '#64748B'
                          }}
                        />
                        <YAxis
                          type="number"
                          dataKey="PCA2"
                          name="PC 2"
                          stroke="#64748B"
                          tick={{ fontSize: 11 }}
                          label={{
                            value: 'Principal Component 2',
                            angle: -90,
                            position: 'insideLeft',
                            offset: 5,
                            fontSize: 11,
                            fill: '#64748B'
                          }}
                        />
                        <Tooltip content={<CustomScatterTooltip />} />
                        <Legend
                          verticalAlign="top"
                          height={36}
                          wrapperStyle={{ paddingBottom: 10, fontSize: '0.8rem', fontWeight: 600 }}
                        />

                        {/* Separate Scatter series for EACH cluster with its own unique color */}
                        {Array.from({ length: k }, (_, cId) => {
                          const clusterPoints = (data?.pca_sample || []).filter(p => Number(p.Cluster) === cId);
                          const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                          const isVisible = selectedClusterFilter === 'ALL' || selectedClusterFilter === cId;
                          const persona = getClusterPersona(cId, data?.profile);
                          
                          return (
                            <Scatter
                              key={`cluster-scatter-${cId}`}
                              name={`Cluster ${cId}: ${persona}`}
                              data={clusterPoints}
                              fill={color}
                              opacity={isVisible ? 0.85 : 0.08}
                            />
                          );
                        })}

                        {/* Centroids highlighted with distinct dark star crosshair marker */}
                        {Array.isArray(data?.centroids) && data.centroids.length > 0 && (
                          <Scatter
                            name="Cluster Centroids (★)"
                            data={data.centroids.filter(c => selectedClusterFilter === 'ALL' || selectedClusterFilter === c.Cluster)}
                            fill="#0F172A"
                            shape="cross"
                          />
                        )}
                      </ScatterChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Chart Annotation Footer */}
                  <div style={{
                    marginTop: 12,
                    padding: '8px 12px',
                    borderRadius: 6,
                    background: '#F8FAFC',
                    border: '1px solid #E2E8F0',
                    fontSize: '0.78rem',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6
                  }}>
                    <Info size={14} color="var(--primary)" />
                    <span>
                      Each cluster is mapped to a distinct color. Click legend items or the filter buttons above to isolate specific student cohorts in the hyperspace.
                    </span>
                  </div>
                </div>

                {/* Cluster Size Donut & Breakdown Table */}
                <div className="campus-card">
                  <div className="campus-card-header">
                    <div>
                      <div className="card-title">Student Cohort Balance Across Clusters</div>
                      <div className="card-subtitle">Unsupervised distribution of {totalStudents.toLocaleString()} candidates</div>
                    </div>
                    <span className="badge badge-role">K={k} Partitions</span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '200px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={data?.cluster_sizes || []}
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={80}
                          dataKey="Count"
                          nameKey="Cluster"
                          paddingAngle={3}
                        >
                          {(data?.cluster_sizes || []).map((entry, index) => (
                            <Cell
                              key={`pie-cell-${index}`}
                              fill={CLUSTER_COLORS[entry.Cluster % CLUSTER_COLORS.length]}
                            />
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
                          <th>Archetype Persona</th>
                          <th>Student Count</th>
                          <th>Share %</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data?.cluster_sizes?.map((c) => {
                          const cId = c.Cluster;
                          const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                          const count = c.Count ?? 0;
                          const pct = totalStudents > 0 ? ((count / totalStudents) * 100).toFixed(1) : 0;
                          const persona = getClusterPersona(cId, data?.profile);
                          return (
                            <tr
                              key={cId}
                              style={{
                                cursor: 'pointer',
                                background: selectedClusterFilter === cId ? `${color}15` : 'transparent'
                              }}
                              onClick={() => setSelectedClusterFilter(selectedClusterFilter === cId ? 'ALL' : cId)}
                            >
                              <td>
                                <span style={{
                                  display: 'inline-flex',
                                  alignItems: 'center',
                                  gap: 6,
                                  fontWeight: 800,
                                  color: color
                                }}>
                                  <span style={{ width: 10, height: 10, borderRadius: '50%', background: color }} />
                                  Cluster {cId}
                                </span>
                              </td>
                              <td style={{ fontWeight: 600, color: 'var(--navy)' }}>{persona}</td>
                              <td>{count.toLocaleString()}</td>
                              <td><b>{pct}%</b></td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Cluster Archetype Personas Detailed Cards */}
              <div style={{ marginTop: 20 }}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--navy)', marginBottom: 14 }}>
                  Discovered Behavioral Archetypes & Prescriptive Interventions (K={k})
                </h3>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
                  {Array.from({ length: k }, (_, cId) => {
                    const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                    const sizeObj = (data?.cluster_sizes || []).find(s => s.Cluster === cId);
                    const profRow = (data?.profile || []).find(p => p.Cluster === cId) || {};
                    const persona = getClusterPersona(cId, data?.profile);
                    const count = sizeObj?.Count || 0;
                    const pct = totalStudents > 0 ? ((count / totalStudents) * 100).toFixed(1) : 0;
                    
                    return (
                      <div
                        key={cId}
                        style={{
                          background: '#FFFFFF',
                          borderRadius: 12,
                          border: `2px solid ${color}`,
                          padding: 18,
                          boxShadow: 'var(--shadow-sm)',
                          position: 'relative',
                          overflow: 'hidden'
                        }}
                      >
                        {/* Top Color Accent */}
                        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 5, background: color }} />

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8, marginTop: 4 }}>
                          <span style={{
                            padding: '3px 10px',
                            borderRadius: 12,
                            background: `${color}18`,
                            color: color,
                            fontWeight: 800,
                            fontSize: '0.78rem'
                          }}>
                            Cluster {cId}
                          </span>
                          <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)' }}>
                            {count.toLocaleString()} Students ({pct}%)
                          </span>
                        </div>

                        <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--navy)', marginBottom: 10 }}>
                          {persona}
                        </div>

                        {/* Metric Highlights */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, background: '#F8FAFC', padding: 10, borderRadius: 8, fontSize: '0.78rem', marginBottom: 10 }}>
                          <div>
                            <span style={{ color: 'var(--text-muted)', display: 'block' }}>Avg CGPA:</span>
                            <strong style={{ color: 'var(--navy)', fontSize: '0.92rem' }}>
                              {profRow.cgpa ? Number(profRow.cgpa).toFixed(2) : 'N/A'}
                            </strong>
                          </div>
                          <div>
                            <span style={{ color: 'var(--text-muted)', display: 'block' }}>Avg DSA Solved:</span>
                            <strong style={{ color: 'var(--navy)', fontSize: '0.92rem' }}>
                              {profRow.dsa_questions_solved ? Math.round(profRow.dsa_questions_solved) : 'N/A'}
                            </strong>
                          </div>
                          <div>
                            <span style={{ color: 'var(--text-muted)', display: 'block' }}>Coding Skill:</span>
                            <strong style={{ color: 'var(--navy)', fontSize: '0.92rem' }}>
                              {profRow.coding_skill_score ? Number(profRow.coding_skill_score).toFixed(1) : 'N/A'}/10
                            </strong>
                          </div>
                          <div>
                            <span style={{ color: 'var(--text-muted)', display: 'block' }}>Mock Interview:</span>
                            <strong style={{ color: 'var(--navy)', fontSize: '0.92rem' }}>
                              {profRow.mock_interview_score ? Number(profRow.mock_interview_score).toFixed(1) : 'N/A'}/10
                            </strong>
                          </div>
                        </div>

                        <button
                          type="button"
                          onClick={() => setSelectedClusterFilter(selectedClusterFilter === cId ? 'ALL' : cId)}
                          style={{
                            width: '100%',
                            padding: '6px 12px',
                            borderRadius: 6,
                            border: `1px solid ${color}`,
                            background: selectedClusterFilter === cId ? color : 'transparent',
                            color: selectedClusterFilter === cId ? '#FFFFFF' : color,
                            fontSize: '0.78rem',
                            fontWeight: 700,
                            cursor: 'pointer',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          {selectedClusterFilter === cId ? '✓ Focused on Graph' : 'Highlight on PCA Hyperspace'}
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'elbow' && (
            <div className="campus-card" style={{ marginBottom: '24px' }}>
              <div className="campus-card-header">
                <div>
                  <div className="card-title">Elbow Method: Within-Cluster Sum of Squares (WCSS) vs K</div>
                  <div className="card-subtitle">Inertia inflection heuristic for determining optimal cluster count</div>
                </div>
                <span className="badge badge-role">Inertia Inflection</span>
              </div>

              {elbowData.length > 0 ? (
                <div style={{ height: '360px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={elbowData} margin={{ top: 20, right: 30, left: 10, bottom: 10 }}>
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
                <div>
                  <div className="card-title">Cluster Profile Centroids (Mean Feature Vectors)</div>
                  <div className="card-subtitle">Mathematical center coordinates across all standardized metrics</div>
                </div>
                <span className="badge badge-role">Attribute Averages</span>
              </div>

              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      {data?.profile?.length > 0 && Object.keys(data.profile[0]).map(col => <th key={col}>{col}</th>)}
                    </tr>
                  </thead>
                  <tbody>
                    {data?.profile?.map((row, i) => {
                      const color = CLUSTER_COLORS[row.Cluster % CLUSTER_COLORS.length] || '#2563EB';
                      return (
                        <tr key={i}>
                          {Object.entries(row).map(([kKey, v], j) => (
                            <td key={j} style={{
                              fontWeight: j === 0 || kKey === 'Cluster' ? 700 : 400,
                              color: kKey === 'Cluster' ? color : 'inherit'
                            }}>
                              {kKey === 'Cluster' ? `Cluster ${v}` : typeof v === 'number' ? v.toFixed(2) : String(v)}
                            </td>
                          ))}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {/* Analytical Academic Justification */}
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
            "Student records span over 10 continuous and discrete dimensions. Fitting 2D Principal Component Analysis (PCA) captures the primary directions of variance, allowing administrators to visually inspect cluster separation, overlaps, and transitional candidates with distinct cluster colors."
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
