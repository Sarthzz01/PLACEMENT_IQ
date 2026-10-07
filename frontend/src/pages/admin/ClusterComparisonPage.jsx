import React, { useState, useEffect } from 'react';
import { GitCompare, Award, CheckCircle2, RefreshCw, BarChart2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function ClusterComparisonPage() {
  const [k, setK] = useState(4);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  const fetchComparison = async (clusters) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/admin/cluster-comparison?k=${clusters}`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error('Error fetching cluster comparison:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison(k);
  }, []);

  const kmSil = data?.kmeans?.silhouette || 0;
  const aggSil = data?.agglomerative?.silhouette || 0;
  const winner = kmSil >= aggSil ? 'K-Means' : 'Agglomerative';

  const chartData = [
    {
      name: 'Silhouette Score',
      'K-Means': kmSil,
      'Agglomerative': aggSil,
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-main)', margin: '0 0 6px 0' }}>
          Clustering Benchmark: K-Means vs Agglomerative
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: 0 }}>
          Side-by-side comparative evaluation of partitioning versus hierarchical clustering algorithms on candidate cohort data.
        </p>
      </div>

      <AcademicJustification
        title="Comparative Clustering Justification (K-Means vs Agglomerative)"
        algorithmRationale="Comparing centroid-based K-Means against bottom-up Agglomerative Hierarchical clustering provides an empirical validation of cluster boundaries. While K-Means minimizes intra-cluster Euclidean inertia via iterative expectation-maximization assuming spherical clusters, Agglomerative clustering iteratively merges nearest pairs via Ward's minimal variance linkage without assuming spherical geometry. Testing both algorithms under identical feature subsets validates whether student skill profiles naturally conform to hyper-spherical clusters or exhibit hierarchical density structures."
        institutionalImpact="Enables campus placement officers to choose the most mathematically sound student categorization framework. A higher silhouette score proves the resulting student buckets (e.g. 'High Achievers' vs 'Foundational Learners') are distinctly separable, ensuring mentorship resources are targeted without misallocating borderline candidates."
        dwmConcepts="Silhouette Coefficient analysis, Ward's Minimum Variance Linkage, Centroid Vector convergence, Voronoi Cell Partitioning vs Dendrogram Tree Decomposition, Cluster Separation vs Compactness."
      />

      {/* Controls & Benchmark Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20, marginBottom: 24 }}>
        <div className="campus-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: 8, display: 'block' }}>
            Number of Clusters (K): {k}
          </label>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <input
              type="range"
              min="2"
              max="8"
              value={k}
              onChange={(e) => setK(Number(e.target.value))}
              style={{ flex: 1, accentColor: 'var(--primary)' }}
            />
            <button
              onClick={() => fetchComparison(k)}
              disabled={loading}
              className="btn-primary"
              style={{ padding: '8px 14px', fontSize: '0.85rem' }}
            >
              <RefreshCw size={14} className={loading ? 'spin' : ''} /> Run
            </button>
          </div>
        </div>

        <div className="campus-card" style={{ borderLeft: '4px solid var(--primary)' }}>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>K-Means (Centroid Partitioning)</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--primary)', marginTop: 4 }}>
            {loading ? '...' : kmSil}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
            Mean Silhouette Score &bull; Global partition
          </div>
        </div>

        <div className="campus-card" style={{ borderLeft: '4px solid #8B5CF6' }}>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Agglomerative (Ward Linkage)</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#8B5CF6', marginTop: 4 }}>
            {loading ? '...' : aggSil}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
            Mean Silhouette Score &bull; Bottom-up hierarchy
          </div>
        </div>

        <div className="campus-card" style={{ borderLeft: '4px solid var(--success)', background: '#F0FDF4' }}>
          <div style={{ fontSize: '0.85rem', color: '#166534', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 6 }}>
            <Award size={16} /> Higher Quality Clustering
          </div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#15803D', marginTop: 6 }}>
            {loading ? 'Evaluating...' : `${winner} (Δ = ${Math.abs(kmSil - aggSil).toFixed(4)})`}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#166534', marginTop: 4 }}>
            Demonstrates superior cluster separation & compactness
          </div>
        </div>
      </div>

      {/* Visual Silhouette Comparison Chart */}
      <div className="campus-card" style={{ marginBottom: 24 }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)', marginTop: 0, marginBottom: 16 }}>
          Silhouette Quality Comparison (Higher is Superior)
        </h3>
        <div style={{ height: 260 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="name" stroke="#64748B" />
              <YAxis domain={[0, 0.5]} stroke="#64748B" />
              <Tooltip formatter={(val) => (typeof val === 'number' ? val.toFixed(4) : val)} />
              <Legend />
              <Bar dataKey="K-Means" fill="#2563EB" radius={[6, 6, 0, 0]} />
              <Bar dataKey="Agglomerative" fill="#8B5CF6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Side-by-side Profiles */}
      {data && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: 20 }}>
          {/* K-Means Profile */}
          <div className="campus-card">
            <h4 style={{ margin: '0 0 12px 0', color: 'var(--primary)', fontWeight: 700 }}>
              K-Means Cluster Centroid Means (K={k})
            </h4>
            <div style={{ overflowX: 'auto' }}>
              <table className="campus-table">
                <thead>
                  <tr>
                    <th>Cluster</th>
                    <th>CGPA</th>
                    <th>DSA</th>
                    <th>Aptitude</th>
                    <th>Coding</th>
                  </tr>
                </thead>
                <tbody>
                  {data.kmeans?.profile?.map((c, i) => (
                    <tr key={i}>
                      <td><span className="badge badge-blue">Cluster {c.Cluster}</span></td>
                      <td>{Number(c.cgpa || 0).toFixed(2)}</td>
                      <td>{Number(c.dsa_problems_solved || 0).toFixed(0)}</td>
                      <td>{Number(c.aptitude_score || 0).toFixed(1)}</td>
                      <td>{Number(c.coding_skill_score || 0).toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Agglomerative Profile */}
          <div className="campus-card">
            <h4 style={{ margin: '0 0 12px 0', color: '#8B5CF6', fontWeight: 700 }}>
              Agglomerative Cluster Centroid Means (K={k})
            </h4>
            <div style={{ overflowX: 'auto' }}>
              <table className="campus-table">
                <thead>
                  <tr>
                    <th>Cluster</th>
                    <th>CGPA</th>
                    <th>DSA</th>
                    <th>Aptitude</th>
                    <th>Coding</th>
                  </tr>
                </thead>
                <tbody>
                  {data.agglomerative?.profile?.map((c, i) => (
                    <tr key={i}>
                      <td><span className="badge" style={{ background: '#EDE9FE', color: '#6D28D9' }}>Cluster {c.Cluster}</span></td>
                      <td>{Number(c.cgpa || 0).toFixed(2)}</td>
                      <td>{Number(c.dsa_problems_solved || 0).toFixed(0)}</td>
                      <td>{Number(c.aptitude_score || 0).toFixed(1)}</td>
                      <td>{Number(c.coding_skill_score || 0).toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
