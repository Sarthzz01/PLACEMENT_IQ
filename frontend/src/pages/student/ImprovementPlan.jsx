import React, { useEffect, useState } from 'react';
import { Download, CheckCircle2, TrendingUp, AlertCircle, ArrowUpRight, Award, Compass } from 'lucide-react';

export default function ImprovementPlan({ user }) {
  const [plan, setPlan] = useState([]);
  const [strengths, setStrengths] = useState([]);
  const [readiness, setReadiness] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    setLoading(true);
    fetch(`/api/student/plan/${encodeURIComponent(studentEmail)}`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        const planData = data?.plan || {};
        const rawItems = planData.all_improvements || planData.top_improvements || (Array.isArray(planData) ? planData : (data?.items || []));
        
        const normalizedItems = (rawItems || []).map(item => ({
          area: item.title || item.area || item.feature || 'Competency Area',
          priority: item.priority || 'Medium',
          current_value: `${item.student_val ?? item.current_value ?? '—'} ${item.unit || ''}`.trim(),
          target_value: `${item.benchmark_val ?? item.target_value ?? '—'} ${item.unit || ''}`.trim(),
          actionable_recommendation: item.advice || item.actionable_recommendation || 'Continue deliberate practice.'
        }));

        setPlan(normalizedItems);
        setReadiness(planData.readiness_level || data?.readiness_level || 'Evaluated Readiness');
        setStrengths(planData.strengths || data?.strengths || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load improvement plan:', err);
        setLoading(false);
      });
  }, [user]);

  const downloadCSV = () => {
    if (!plan || plan.length === 0) return;
    const headers = ['Area', 'Priority', 'Current Value', 'Placed Target Median', 'Recommendation'];
    const rows = plan.map(p => [
      `"${p.area}"`,
      `"${p.priority}"`,
      `"${p.current_value}"`,
      `"${p.target_value}"`,
      `"${(p.actionable_recommendation || '').replace(/"/g, '""')}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    const safeName = (user?.name || user?.email || 'Student').replace(/\s+/g, '_');
    link.setAttribute('download', `improvement_plan_${safeName}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Synthesizing personalized improvement plan...</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Personalized Improvement Plan</h2>
            {readiness && (
              <span className="badge badge-role" style={{ fontSize: '0.8rem', padding: '4px 10px' }}>
                {readiness}
              </span>
            )}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', marginTop: '4px' }}>
            Prescriptive roadmap targeting competency bottlenecks to accelerate your placement eligibility.
          </p>
        </div>

        {plan.length > 0 && (
          <button className="btn btn-secondary" onClick={downloadCSV}>
            <Download size={16} /> Export Action Plan (CSV)
          </button>
        )}
      </div>

      {plan.length === 0 ? (
        <div className="campus-card" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <CheckCircle2 size={48} color="#16A34A" style={{ marginBottom: '16px' }} />
          <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
            All Competency Benchmarks Satisfied!
          </h3>
          <p style={{ color: '#64748B', maxWidth: '520px', margin: '0 auto' }}>
            Your current academic metrics, problem-solving counts, and practical projects already match or exceed the median profiles of successfully placed alumni.
          </p>
        </div>
      ) : (
        <div>
          {/* Priority Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px', marginBottom: '28px' }}>
            {plan.map((item, idx) => (
              <div key={idx} className="campus-card" style={{ borderLeft: `4px solid ${item.priority === 'High' ? 'var(--error)' : 'var(--warning)'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontWeight: 800, fontSize: '1.05rem', color: 'var(--navy)' }}>{item.area}</span>
                  <span className="badge" style={{
                    background: item.priority === 'High' ? 'var(--error-soft)' : 'var(--warning-soft)',
                    color: item.priority === 'High' ? 'var(--error)' : 'var(--warning)',
                    border: `1px solid ${item.priority === 'High' ? 'var(--error-border)' : 'var(--warning-border)'}`
                  }}>
                    {item.priority} Priority
                  </span>
                </div>

                <div style={{ background: '#F8FAFC', padding: '10px 14px', borderRadius: '8px', marginBottom: '14px', fontSize: '0.85rem', display: 'flex', justifyContent: 'space-between' }}>
                  <span>Your Current: <strong style={{ color: '#0F172A' }}>{item.current_value}</strong></span>
                  <span>Target Median: <strong style={{ color: 'var(--primary)' }}>{item.target_value}</strong></span>
                </div>

                <p style={{ fontSize: '0.88rem', color: '#334155', lineHeight: 1.6 }}>
                  {item.actionable_recommendation}
                </p>
              </div>
            ))}
          </div>

          {/* Structured Table */}
          <div className="campus-card" style={{ marginBottom: '28px' }}>
            <div className="campus-card-header">
              <div className="card-title">Structured Milestone Summary</div>
              <span className="badge badge-role">{plan.length} Actionable Items</span>
            </div>

            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Domain</th>
                    <th>Priority</th>
                    <th>Current Value</th>
                    <th>Target Value</th>
                    <th>Action Strategy</th>
                  </tr>
                </thead>
                <tbody>
                  {plan.map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 700, color: '#0F172A' }}>{row.area}</td>
                      <td>
                        <span className="badge" style={{
                          background: row.priority === 'High' ? 'var(--error-soft)' : 'var(--warning-soft)',
                          color: row.priority === 'High' ? 'var(--error)' : 'var(--warning)',
                          border: `1px solid ${row.priority === 'High' ? 'var(--error-border)' : 'var(--warning-border)'}`
                        }}>
                          {row.priority}
                        </span>
                      </td>
                      <td>{row.current_value}</td>
                      <td style={{ color: 'var(--primary)', fontWeight: 700 }}>{row.target_value}</td>
                      <td style={{ maxWidth: '400px' }}>{row.actionable_recommendation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Identified Strengths Section */}
      {strengths.length > 0 && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Award size={18} color="#16A34A" /> Recognized Core Strengths
            </div>
            <span className="badge" style={{ background: '#DCFCE7', color: '#16A34A', border: '1px solid #86EFAC' }}>
              Above Placed Cohort Medians
            </span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '14px', marginTop: '12px' }}>
            {strengths.map((s, idx) => (
              <div key={idx} style={{ background: '#F8FAFC', padding: '12px 16px', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
                <strong style={{ color: '#0F172A', display: 'block', fontSize: '0.92rem' }}>{s.title}</strong>
                <span style={{ fontSize: '0.82rem', color: '#16A34A', fontWeight: 600 }}>{s.detail}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
