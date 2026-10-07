import React, { useEffect, useState } from 'react';
import { Users, UserCheck, UserX, TrendingUp, Award, Clock, ArrowRight, ShieldCheck } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import KPICard from '../../components/KPICard';

export default function AdminDashboard({ user, onNavigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/overview')
      .then(res => res.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Loading institutional intelligence dashboard...</div>;

  const metrics = data?.metrics || {};
  const deptData = data?.dept_distribution || [];
  const activity = data?.recent_activity || [];

  const pieData = [
    { name: 'Placed', value: metrics.placed_students || 0, color: '#16A34A' },
    { name: 'Not Placed', value: metrics.not_placed_students || 0, color: '#DC2626' }
  ];

  return (
    <div>
      {/* Header title */}
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>
          Placement Intelligence Executive Dashboard
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Real-time institutional cohort analytics, predictive conversion benchmarks, and database activity streams.
        </p>
      </div>

      {/* KPI Cards Row */}
      <div className="kpi-grid">
        <KPICard
          title="Total Students"
          value={metrics.total_students ? metrics.total_students.toLocaleString() : '15,000'}
          subtitle="Unified candidate cohort"
          icon={<Users size={24} />}
          iconColor="blue"
        />
        <KPICard
          title="Placed Students"
          value={metrics.placed_students ? metrics.placed_students.toLocaleString() : '12,300'}
          subtitle="Model positive predictions"
          icon={<UserCheck size={24} />}
          iconColor="green"
        />
        <KPICard
          title="Not Placed"
          value={metrics.not_placed_students ? metrics.not_placed_students.toLocaleString() : '2,700'}
          subtitle="Target for training intervention"
          icon={<UserX size={24} />}
          iconColor="red"
        />
        <KPICard
          title="Placement Conversion"
          value={`${metrics.placement_rate || 82.0}%`}
          subtitle="Campus-wide conversion rate"
          icon={<TrendingUp size={24} />}
          iconColor="purple"
        />
        <KPICard
          title="Average CGPA"
          value={metrics.average_cgpa ? metrics.average_cgpa.toFixed(2) : '7.52'}
          subtitle="Academic cohort mean"
          icon={<Award size={24} />}
          iconColor="amber"
        />
      </div>

      {/* Main Analytics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        {/* Left: Department Distribution */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Placement Conversion by Engineering Discipline</div>
              <div className="card-subtitle">Placed vs. Not Placed distribution across branches</div>
            </div>
            <button className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 12px' }} onClick={() => onNavigate('olap')}>
              Explore OLAP
            </button>
          </div>

          <div style={{ height: '330px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deptData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <XAxis dataKey="branch" stroke="#64748B" tick={{ fontSize: 12 }} />
                <YAxis stroke="#64748B" />
                <Tooltip />
                <Bar dataKey="placed" name="Placed" fill="#2563EB" radius={[6, 6, 0, 0]} />
                <Bar dataKey="not_placed" name="Not Placed" fill="#CBD5E1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right: Overall Donut & Recent Activity */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Placement Ratio & Audit Stream</div>
              <div className="card-subtitle">Live database logs from SQLite warehouse</div>
            </div>
            <button className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 12px' }} onClick={() => onNavigate('students')}>
              Roster
            </button>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '160px', marginBottom: '16px' }}>
            <ResponsiveContainer width="60%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <span style={{ width: '12px', height: '12px', background: '#16A34A', borderRadius: '3px' }}></span>
                <span>Placed: <strong>{metrics.placement_rate}%</strong></span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: '12px', height: '12px', background: '#DC2626', borderRadius: '3px' }}></span>
                <span>Needs Help: <strong>{(100 - (metrics.placement_rate || 0)).toFixed(1)}%</strong></span>
              </div>
            </div>
          </div>

          <div style={{ borderTop: '1px solid #F1F5F9', paddingTop: '12px' }}>
            <div style={{ fontSize: '0.78rem', fontWeight: 700, textTransform: 'uppercase', color: '#64748B', marginBottom: '8px' }}>
              Recent SQLite Activity
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '130px', overflowY: 'auto' }}>
              {activity.slice(0, 4).map((act, idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', padding: '4px 0' }}>
                  <span style={{ color: '#0F172A', fontWeight: 600 }}>{act.event_type}</span>
                  <span style={{ color: '#64748B' }}>{act.timestamp ? act.timestamp.split(' ')[0] : 'Today'}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
