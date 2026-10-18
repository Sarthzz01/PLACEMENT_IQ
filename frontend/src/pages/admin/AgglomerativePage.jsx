import React, { useEffect, useState } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, Legend
} from 'recharts';
import { Filter, Info, Network, Layers } from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

const CLUSTER_COLORS = [
  '#2563EB', // Cluster 0: Royal Blue
  '#16A34A', // Cluster 1: Emerald Green
  '#D97706', // Cluster 2: Warm Amber
  '#9333EA', // Cluster 3: Vivid Purple
  '#E11D48', // Cluster 4: Crimson Rose
  '#0891B2', // Cluster 5: Deep Cyan
];

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
        minWidth: 180
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: color, display: 'inline-block' }} />
          <strong style={{ color: color, fontSize: '0.9rem' }}>
            Cluster {cId} (Hierarchical)
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

export default function AgglomerativePage() {
  const [k, setK] = useState(4);
  const [linkage, setLinkage] = useState('ward');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedClusterFilter, setSelectedClusterFilter] = useState('ALL');

  useEffect(() => {
    setLoading(true);
    setSelectedClusterFilter('ALL');
    fetch(`/api/admin/agglomerative?k=${k}&linkage_method=${linkage}`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [k, linkage]);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Agglomerative Hierarchical Clustering</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Bottom-up hierarchical clustering with dendrogram taxonomy, customizable linkage criteria, and multi-level skill tiering.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#334155' }}>Linkage:</label>
            <select className="form-select" style={{ width: '120px' }} value={linkage} onChange={e => setLinkage(e.target.value)}>
              <option value="ward">Ward</option>
              <option value="complete">Complete</option>
              <option value="average">Average</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 700, color: '#334155' }}>Clusters (K):</label>
            <select className="form-select" style={{ width: '80px', fontWeight: 700 }} value={k} onChange={e => setK(parseInt(e.target.value))}>
              {[2, 3, 4, 5, 6].map(num => <option key={num} value={num}>{num}</option>)}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ padding: '40px', color: '#64748B', textAlign: 'center' }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>Computing pairwise distance matrix & hierarchical dendrogram tree...</div>
        </div>
      ) : (
        <>
          {/* Cluster Filter Buttons */}
          <div className="campus-card" style={{ marginBottom: '20px', padding: '14px 20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <Filter size={16} color="var(--primary)" />
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--navy)' }}>Filter Cohort:</span>
              </div>

              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <button
                  type="button"
                  onClick={() => setSelectedClusterFilter('ALL')}
                  style={{
                    padding: '5px 12px',
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
                  All Clusters
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
                        padding: '5px 12px',
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
                        transition: 'all 0.15s ease'
                      }}
                    >
                      <span style={{ width: 8, height: 8, borderRadius: '50%', background: isSelected ? '#FFFFFF' : color }} />
                      Cluster {cId} ({sizeObj?.Count || 0})
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            {/* Multi-Colored PCA Scatter Chart */}
            <div className="campus-card">
              <div className="campus-card-header">
                <div>
                  <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span>Agglomerative PCA Projection (K={k})</span>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#16A34A', background: '#DCFCE7', padding: '2px 8px', borderRadius: 12 }}>
                      Multi-Color Hierarchy
                    </span>
                  </div>
                  <div className="card-subtitle">
                    Hierarchical clusters rendered with distinct color codes ({linkage.toUpperCase()} linkage)
                  </div>
                </div>
                <span className="badge badge-role">Silhouette: {data?.silhouette}</span>
              </div>

              <div style={{ height: '390px', width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 15, right: 20, bottom: 25, left: 10 }}>
                    <CartesianGrid stroke="#F1F5F9" strokeDasharray="3 3" />
                    <XAxis
                      type="number"
                      dataKey="PCA1"
                      name="PC 1"
                      stroke="#64748B"
                      tick={{ fontSize: 11 }}
                      label={{ value: 'Principal Component 1', position: 'insideBottom', offset: -12, fontSize: 11, fill: '#64748B' }}
                    />
                    <YAxis
                      type="number"
                      dataKey="PCA2"
                      name="PC 2"
                      stroke="#64748B"
                      tick={{ fontSize: 11 }}
                      label={{ value: 'Principal Component 2', angle: -90, position: 'insideLeft', offset: 5, fontSize: 11, fill: '#64748B' }}
                    />
                    <Tooltip content={<CustomScatterTooltip />} />
                    <Legend verticalAlign="top" height={36} wrapperStyle={{ paddingBottom: 10, fontSize: '0.8rem', fontWeight: 600 }} />

                    {Array.from({ length: k }, (_, cId) => {
                      const clusterPoints = (data?.pca_sample || []).filter(p => Number(p.Cluster) === cId);
                      const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                      const isVisible = selectedClusterFilter === 'ALL' || selectedClusterFilter === cId;
                      return (
                        <Scatter
                          key={`agg-cluster-${cId}`}
                          name={`Cluster ${cId}`}
                          data={clusterPoints}
                          fill={color}
                          opacity={isVisible ? 0.85 : 0.08}
                        />
                      );
                    })}
                  </ScatterChart>
                </ResponsiveContainer>
              </div>

              <div style={{
                marginTop: 10,
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
                <span>Points are colored by agglomerative taxonomy. Use linkage selector above to observe cluster variance adjustments.</span>
              </div>
            </div>

            {/* Cluster Size Distribution */}
            <div className="campus-card">
              <div className="campus-card-header">
                <div>
                  <div className="card-title">Cluster Size Distribution (Sample Cohort)</div>
                  <div className="card-subtitle">Partition breakdown across {k} dendrogram branches</div>
                </div>
                <span className="badge badge-role">{linkage.toUpperCase()} Linkage</span>
              </div>

              <div className="table-container" style={{ marginBottom: '18px' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Hierarchical Cluster</th>
                      <th>Student Count</th>
                      <th>Color Code</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data?.cluster_sizes?.map((c) => {
                      const cId = c.Cluster;
                      const color = CLUSTER_COLORS[cId % CLUSTER_COLORS.length];
                      return (
                        <tr
                          key={cId}
                          style={{
                            cursor: 'pointer',
                            background: selectedClusterFilter === cId ? `${color}15` : 'transparent'
                          }}
                          onClick={() => setSelectedClusterFilter(selectedClusterFilter === cId ? 'ALL' : cId)}
                        >
                          <td style={{ fontWeight: 700, color: color }}>Cluster {cId}</td>
                          <td>{c.Count?.toLocaleString?.() ?? c.Count ?? 0}</td>
                          <td>
                            <span style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: 6,
                              fontSize: '0.78rem',
                              fontWeight: 700,
                              color: color
                            }}>
                              <span style={{ width: 12, height: 12, borderRadius: 3, background: color }} />
                              {color}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '10px', padding: '14px', fontSize: '0.85rem' }}>
                <strong style={{ color: 'var(--navy)', display: 'block', marginBottom: '4px' }}>Hierarchical Dendrogram Taxonomy:</strong>
                <p style={{ color: '#475569', margin: 0, lineHeight: 1.5 }}>
                  The dendrogram traces each student as an individual leaf node, progressively merging nearest neighbors based on minimal variance until reaching the root. Cutting the tree at distance threshold produces {k} discrete student cohorts.
                </p>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Analytical Conclusion & Project Outcomes */}
      <AcademicJustification
        title="Hierarchical Taxonomy Discovery: Agglomerative Clustering & Project Outcomes"
        techniqueName={`Agglomerative Bottom-Up Clustering (${linkage.toUpperCase()} Linkage, K=${k})`}
        whyChosen={[
          [
            "Why Hierarchical Agglomerative Clustering is Selected",
            "Unlike flat partitional algorithms like K-Means which enforce rigid spherical boundaries, Agglomerative clustering begins with each student as an independent leaf and recursively merges nearest pairs using Ward's minimum variance criterion. This constructs a complete taxonomic tree of candidate competencies."
          ],
          [
            "Why Linkage Metric Comparison is Critical",
            "Testing Ward (minimum variance) vs Complete (maximum distance) vs Average linkage demonstrates sensitivity to outliers and validates whether candidate skill profiles form nested sub-hierarchies or distinct isolated islands."
          ],
          [
            "Why Sampled Representative Cohort is Scaled",
            "Hierarchical clustering requires $O(N^2)$ space and $O(N^3)$ computational time. Subsampling a statistically representative cohort balances mathematical precision with real-time UI interactivity."
          ]
        ]}
        whatWeGet={[
          [
            "Curriculum Prerequisite Dependency Discovery",
            "Reveals natural skill progression hierarchies (e.g., verifying whether basic DSA mastery must precede competitive problem-solving)."
          ],
          [
            "Non-Spherical Candidate Persona Identification",
            "Uncovers irregularly shaped cohorts that spherical K-Means partitions miss, such as candidates with non-traditional multidisciplinary project portfolios."
          ],
          [
            "Institutional Academic Viva Validation",
            "Provides dendrogram tree documentation proving that student categorization is derived from rigorous mathematical taxonomy rather than arbitrary cutoffs."
          ]
        ]}
        institutionalImpact="Provides academic advisory boards with dendrogram visualizations that justify prerequisite restructuring in university curricula, verifying which technical milestones are natural gateways to campus placement readiness."
        dwmConcept="Hierarchical Clustering, Ward's Minimum Variance Linkage, Cophenetic Distance, Dendrogram Pruning, Agglomerative Tree Synthesis."
      />
    </div>
  );
}
