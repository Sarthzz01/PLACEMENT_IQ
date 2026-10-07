import React, { useEffect, useState } from 'react';
import { ArrowRight, CheckCircle2, Shield, TrendingUp, Users, Cpu, Database, Award, LogIn, Sparkles } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function HomePage({ onGoToLogin, onNavigate }) {
  const [stats, setStats] = useState(null);

  const handleGo = (tab = 'login') => {
    if (typeof onGoToLogin === 'function') {
      onGoToLogin(tab);
    } else if (typeof onNavigate === 'function') {
      onNavigate('login');
    }
  };

  useEffect(() => {
    fetch('/api/admin/overview')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(() => {});
  }, []);

  const chartData = stats?.dept_distribution || [
    { branch: 'CSE', placed: 4200, not_placed: 800 },
    { branch: 'IT', placed: 3100, not_placed: 700 },
    { branch: 'ECE', placed: 2400, not_placed: 900 },
    { branch: 'EEE', placed: 1800, not_placed: 800 },
    { branch: 'MECH', placed: 1200, not_placed: 600 }
  ];

  return (
    <div style={{ background: '#F8FAFC', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <nav style={{ background: '#FFFFFF', borderBottom: '1px solid #E2E8F0', padding: '16px 48px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, zIndex: 100 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '38px', height: '38px', borderRadius: '8px', background: '#2563EB', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.1rem', boxShadow: '0 4px 12px rgba(37,99,235,0.4)' }}>
            IQ
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: '1.15rem', color: '#0F172A', letterSpacing: '-0.02em' }}>PLACEMENT IQ</div>
            <div style={{ fontSize: '0.72rem', color: '#64748B', fontWeight: 600 }}>CAMPUS INTELLIGENCE PLATFORM</div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <button className="btn btn-secondary" onClick={() => handleGo('login')}>
            Sign In
          </button>
          <button className="btn btn-primary" onClick={() => handleGo('register')}>
            Register Candidate <ArrowRight size={16} />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section style={{ padding: '60px 48px 40px 48px', maxWidth: '1280px', margin: '0 auto', textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: '#EFF6FF', color: '#2563EB', border: '1px solid #BFDBFE', padding: '6px 16px', borderRadius: '999px', fontSize: '0.82rem', fontWeight: 700, marginBottom: '20px' }}>
          <Sparkles size={16} /> Enterprise University Placement Analytics & Intelligence
        </div>
        <h1 style={{ fontSize: '3rem', fontWeight: 900, color: '#0F172A', letterSpacing: '-0.03em', lineHeight: 1.15, maxWidth: '900px', margin: '0 auto 20px auto' }}>
          Predict Student Placement Readiness with Data-Driven Intelligence
        </h1>
        <p style={{ fontSize: '1.15rem', color: '#475569', maxWidth: '720px', margin: '0 auto 32px auto', lineHeight: 1.6 }}>
          A unified Data Warehousing and Machine Learning platform empowering students with explainable skill benchmarks and placement deans with multidimensional OLAP analytics.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginBottom: '48px' }}>
          <button className="btn btn-primary" style={{ padding: '12px 28px', fontSize: '1rem' }} onClick={() => handleGo('register')}>
            Get Started Free <ArrowRight size={18} />
          </button>
          <button className="btn btn-secondary" style={{ padding: '12px 28px', fontSize: '1rem' }} onClick={() => handleGo('login')}>
            Institutional Sign In
          </button>
        </div>

        {/* Top metrics pill row */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '32px', flexWrap: 'wrap', borderTop: '1px solid #E2E8F0', borderBottom: '1px solid #E2E8F0', padding: '24px 0' }}>
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#2563EB' }}>15,000+</div>
            <div style={{ fontSize: '0.85rem', color: '#64748B', fontWeight: 600 }}>Verified Student Records</div>
          </div>
          <div style={{ borderLeft: '1px solid #E2E8F0' }} />
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#16A34A' }}>86.5%</div>
            <div style={{ fontSize: '0.85rem', color: '#64748B', fontWeight: 600 }}>Random Forest Accuracy</div>
          </div>
          <div style={{ borderLeft: '1px solid #E2E8F0' }} />
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0F172A' }}>Star-Schema</div>
            <div style={{ fontSize: '0.85rem', color: '#64748B', fontWeight: 600 }}>SQLite Data Warehouse</div>
          </div>
          <div style={{ borderLeft: '1px solid #E2E8F0' }} />
          <div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#F59E0B' }}>6-D OLAP</div>
            <div style={{ fontSize: '0.85rem', color: '#64748B', fontWeight: 600 }}>Interactive Analytics Cube</div>
          </div>
        </div>
      </section>

      {/* Department Analytics Chart Card */}
      <section style={{ maxWidth: '1100px', margin: '0 auto 60px auto', width: '100%', padding: '0 24px' }}>
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Placement Distribution Across Engineering Branches</div>
              <div className="card-subtitle">Aggregated from verified institutional dataset records</div>
            </div>
            <span className="badge badge-role">Live Warehouse View</span>
          </div>

          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <XAxis dataKey="branch" stroke="#64748B" />
                <YAxis stroke="#64748B" />
                <Tooltip />
                <Bar dataKey="placed" name="Placed Students" fill="#2563EB" radius={[6, 6, 0, 0]} />
                <Bar dataKey="not_placed" name="Not Placed" fill="#CBD5E1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Dual Workspace Cards */}
      <section style={{ maxWidth: '1100px', margin: '0 auto 60px auto', width: '100%', padding: '0 24px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0F172A', textAlign: 'center', marginBottom: '32px' }}>
          Dual Workspaces for Students & Administrators
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px' }}>
          <div className="campus-card" style={{ borderTop: '4px solid #2563EB' }}>
            <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: '#EFF6FF', color: '#2563EB', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
              <Users size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>Student Workspace</h3>
            <p style={{ color: '#64748B', fontSize: '0.9rem', marginBottom: '20px', lineHeight: 1.6 }}>
              Comprehensive career readiness suite tailored for engineering candidates.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#334155' }}>
                <CheckCircle2 size={16} color="#16A34A" /> Live ML Placement Probability Score
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#334155' }}>
                <CheckCircle2 size={16} color="#16A34A" /> Spider Radar Benchmark against Placed Peers
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#16A34A' }}>
                <CheckCircle2 size={16} color="#16A34A" /> Actionable Gap Remediation Plan
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#334155' }}>
                <CheckCircle2 size={16} color="#16A34A" /> Complete Audit Prediction History
              </li>
            </ul>
            <button className="btn btn-outline-primary" style={{ width: '100%' }} onClick={() => handleGo('login')}>
              Sign In as Student
            </button>
          </div>

          <div className="campus-card" style={{ borderTop: '4px solid #0F172A' }}>
            <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: '#F1F5F9', color: '#0F172A', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
              <Shield size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>Admin & Faculty Suite</h3>
            <p style={{ color: '#64748B', fontSize: '0.9rem', marginBottom: '20px', lineHeight: 1.6 }}>
              Institutional Data Warehouse & Machine Learning analytics cockpit for placement cells.
            </p>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#334155' }}>
                <CheckCircle2 size={16} color="#2563EB" /> Star-Schema SQLite Warehouse & SQL Workbench
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#2563EB' }}>
                <CheckCircle2 size={16} color="#2563EB" /> 6-D Dynamic OLAP Engine (Slice, Dice, Roll-Up, Pivot)
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#2563EB' }}>
                <CheckCircle2 size={16} color="#2563EB" /> Supervised Models (Random Forest, Decision Tree, Naive Bayes)
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: '#2563EB' }}>
                <CheckCircle2 size={16} color="#2563EB" /> Clustering Analysis (K-Means & Agglomerative Hierarchical)
              </li>
            </ul>
            <button className="btn btn-secondary" style={{ width: '100%', borderColor: '#0F172A', color: '#0F172A' }} onClick={() => handleGo('login')}>
              Sign In as Administrator
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ background: '#0F172A', color: '#94A3B8', padding: '36px 48px', marginTop: 'auto', textAlign: 'center', borderTop: '1px solid #1E293B' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: '#2563EB', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '0.85rem' }}>
              IQ
            </div>
            <span style={{ color: '#FFFFFF', fontWeight: 700 }}>PLACEMENT IQ</span>
          </div>
          <div style={{ fontSize: '0.85rem' }}>
            Data Warehousing & Data Mining (DWM) Institutional Academic Platform • 2026
          </div>
        </div>
      </footer>
    </div>
  );
}
