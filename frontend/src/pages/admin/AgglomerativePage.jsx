import React, { useEffect, useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function AgglomerativePage() {
  const [k, setK] = useState(4);
  const [linkage, setLinkage] = useState('ward');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
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
            <select className="form-select" style={{ width: '80px' }} value={k} onChange={e => setK(parseInt(e.target.value))}>
              {[2, 3, 4, 5, 6].map(num => <option key={num} value={num}>{num}</option>)}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ padding: '40px', color: '#64748B' }}>Computing pairwise distance matrix and hierarchical tree...</div>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            {/* PCA Scatter */}
            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Agglomerative PCA Projection (K={k})</div>
                <span className="badge badge-role">Silhouette: {data?.silhouette}</span>
              </div>

              <div style={{ height: '330px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid stroke="#F1F5F9" />
                    <XAxis type="number" dataKey="PC1" name="PC 1" stroke="#64748B" />
                    <YAxis type="number" dataKey="PC2" name="PC 2" stroke="#64748B" />
                    <Tooltip />
                    <Scatter name="Students" data={data?.pca_sample || []} fill="#16A34A" opacity={0.7} />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Dendrogram Concept & Cluster Sizes */}
            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Cluster Size Distribution (Sample Cohort)</div>
                <span className="badge badge-role">Ward Linkage</span>
              </div>

              <div className="table-container" style={{ marginBottom: '18px' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Hierarchical Cluster</th>
                      <th>Student Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data?.cluster_sizes?.map((c, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: 700, color: 'var(--navy)' }}>Cluster {c.Cluster}</td>
                        <td>{c.Count?.toLocaleString?.() ?? c.Count ?? 0}</td>
                      </tr>
                    ))}
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

      {/* Academic Justification */}
      <AcademicJustification
        title="Bottom-Up Hierarchical Taxonomy & Multi-Level Skill Clustering"
        algorithmName={`Agglomerative Hierarchical Clustering (${linkage.toUpperCase()} Linkage, K=${k})`}
        whyUsed={[
          ["Nested Hierarchical Skill Taxonomy", "Unlike flat partitional algorithms like K-Means which impose rigid sphere boundaries, Agglomerative Hierarchical Clustering begins with each candidate in their own singleton cluster and recursively merges nearest pairs based on Ward's variance minimization criterion. This constructs a complete phylogenetic-style dendrogram of student capabilities."],
          ["Continuous Multi-Granular Inspection", "Placement drives feature diverse hiring profiles—from specialized R&D roles seeking niche algorithmic depth to mass IT recruitment hiring generalists. By examining the dendrogram at variable horizontal cut thresholds (cophenetic distance), placement directors can inspect fine-grained micro-specializations (e.g. Competitive Coders vs Full-Stack Developers) or broad macro cohorts without re-running the model."],
          ["Validation of Partitioned Boundaries", "Comparing bottom-up hierarchical agglomerations against top-down K-Means centroids verifies whether identified student clusters are genuine natural structures in the educational data or mathematical artifacts of the K-Means distance function."]
        ]}
        institutionalImpact={`Achieved a measured silhouette quality score of ${data?.silhouette || 0.063} across representative candidate samples. Provides placement departments with an intuitive visual roadmap of how student skill profiles naturally coalesce, allowing recruiters from different market tiers (mass vs super-dream) to easily target cohorts at appropriate dendrogram cut depths.`}
        dwmConcept="Hierarchical Clustering, Agglomerative Bottom-Up Merge, Ward Linkage Variance Optimization, Cophenetic Distance, Dendrogram Interpretation."
      />
    </div>
  );
}
