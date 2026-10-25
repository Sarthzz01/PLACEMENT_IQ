import React, { useEffect, useState } from 'react';
import { Download, CheckCircle2, TrendingUp, AlertCircle, ArrowUpRight, Award, Compass, Filter, Target, Sparkles } from 'lucide-react';

export default function ImprovementPlan({ user, onNavigate }) {
  const [plan, setPlan] = useState([]);
  const [strengths, setStrengths] = useState([]);
  const [readiness, setReadiness] = useState('');
  const [loading, setLoading] = useState(true);
  const [lastPrediction, setLastPrediction] = useState(null);
  const [priorityFilter, setPriorityFilter] = useState('ALL'); // 'ALL' | 'CRITICAL_HIGH' | 'MEDIUM'

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    setLoading(true);

    // 1. Check if there is a recent prediction stored in localStorage from PlacementPrediction
    let cachedPrediction = null;
    try {
      const cachedStr = localStorage.getItem(`placementiq_latest_prediction_${studentEmail}`);
      if (cachedStr) {
        cachedPrediction = JSON.parse(cachedStr);
        setLastPrediction(cachedPrediction);
      }
    } catch (e) {
      console.error('Error reading cached prediction:', e);
    }

    fetch(`/api/student/plan/${encodeURIComponent(studentEmail)}`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        const planData = data?.plan || data || {};
        
        // Prioritize full improvements list from recent prediction or backend plan
        const rawItems = (cachedPrediction?.all_improvements && cachedPrediction.all_improvements.length > 0)
          ? cachedPrediction.all_improvements
          : (data?.all_improvements || planData.all_improvements || planData.top_improvements || (Array.isArray(planData) ? planData : (data?.items || [])));

        const normalizedItems = (rawItems || []).map(item => ({
          area: item.title || item.area || item.feature || 'Competency Area',
          priority: item.priority || 'Medium',
          category: item.category || 'General',
          current_value: `${item.student_val ?? item.current_value ?? '—'} ${item.unit || ''}`.trim(),
          target_value: `${item.benchmark_val ?? item.target_value ?? '—'} ${item.unit || ''}`.trim(),
          gap: item.gap ?? null,
          actionable_recommendation: item.advice || item.actionable_recommendation || 'Continue deliberate practice.'
        }));

        setPlan(normalizedItems);
        setReadiness(cachedPrediction?.readiness_level || planData.readiness_level || data?.readiness_level || 'Evaluated Readiness');
        setStrengths(
          (cachedPrediction?.strengths && cachedPrediction.strengths.length > 0)
            ? cachedPrediction.strengths
            : (data?.strengths || planData.strengths || [])
        );
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load improvement plan:', err);
        // Resilient fallback to cached prediction data if available
        if (cachedPrediction && (cachedPrediction.all_improvements || cachedPrediction.top_improvements)) {
          const rawItems = cachedPrediction.all_improvements || cachedPrediction.top_improvements || [];
          const normalizedItems = rawItems.map(item => ({
            area: item.title || item.area || item.feature || 'Competency Area',
            priority: item.priority || 'Medium',
            category: item.category || 'General',
            current_value: `${item.student_val ?? item.current_value ?? '—'} ${item.unit || ''}`.trim(),
            target_value: `${item.benchmark_val ?? item.target_value ?? '—'} ${item.unit || ''}`.trim(),
            gap: item.gap ?? null,
            actionable_recommendation: item.advice || item.actionable_recommendation || 'Continue deliberate practice.'
          }));
          setPlan(normalizedItems);
          setReadiness(cachedPrediction.readiness_level || 'Evaluated Readiness');
          setStrengths(cachedPrediction.strengths || []);
        }
        setLoading(false);
      });
  }, [user]);

  const downloadCSV = () => {
    if (!plan || plan.length === 0) return;
    const headers = ['Area', 'Priority', 'Category', 'Current Value', 'Placed Target Median', 'Recommendation'];
    const rows = plan.map(p => [
      `"${p.area}"`,
      `"${p.priority}"`,
      `"${p.category || 'General'}"`,
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

  const filteredPlan = plan.filter(item => {
    if (priorityFilter === 'CRITICAL_HIGH') {
      return item.priority === 'Critical' || item.priority === 'High';
    }
    if (priorityFilter === 'MEDIUM') {
      return item.priority === 'Medium' || item.priority === 'Low';
    }
    return true;
  });

  const criticalHighCount = plan.filter(i => i.priority === 'Critical' || i.priority === 'High').length;
  const mediumCount = plan.filter(i => i.priority === 'Medium' || i.priority === 'Low').length;

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Synthesizing personalized improvement plan...</div>;

  return (
    <div>
      {/* Header Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Personalized Improvement Plan</h2>
            {readiness && (
              <span className="badge badge-role" style={{ fontSize: '0.8rem', padding: '4px 10px' }}>
                {readiness}
              </span>
            )}
            {plan.length > 0 && (
              <span className="badge" style={{ background: '#EFF6FF', color: 'var(--primary)', border: '1px solid #BFDBFE', fontSize: '0.8rem', padding: '4px 10px' }}>
                All {plan.length} Gaps Tracked
              </span>
            )}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', marginTop: '4px' }}>
            Prescriptive roadmap targeting all empirical deficits identified in your placement assessment.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {onNavigate && (
            <button className="btn btn-secondary" onClick={() => onNavigate('prediction')}>
              <Target size={16} /> Re-Evaluate Readiness
            </button>
          )}
          {plan.length > 0 && (
            <button className="btn btn-secondary" onClick={downloadCSV}>
              <Download size={16} /> Export Action Plan (CSV)
            </button>
          )}
        </div>
      </div>

      {/* Sync Banner if recent assessment is recorded */}
      {lastPrediction && (
        <div style={{
          background: '#EFF6FF',
          border: '1px solid #BFDBFE',
          borderRadius: '12px',
          padding: '14px 18px',
          marginBottom: '24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: '#DBEAFE', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Compass size={20} color="#2563EB" />
            </div>
            <div>
              <div style={{ fontWeight: 700, color: '#1E40AF', fontSize: '0.92rem' }}>
                Active Prediction Sync: Showing All {plan.length} Improvements
              </div>
              <div style={{ fontSize: '0.82rem', color: '#3B82F6' }}>
                Derived directly from your latest placement assessment ({lastPrediction.probability_percent || Math.round((lastPrediction.probability || 0) * 100)}% Score • {lastPrediction.status || 'Evaluated'}).
              </div>
            </div>
          </div>

          {onNavigate && (
            <button className="btn btn-secondary" style={{ fontSize: '0.82rem', padding: '6px 12px' }} onClick={() => onNavigate('prediction')}>
              View Assessment Summary
            </button>
          )}
        </div>
      )}

      {/* Priority Filter Bar */}
      {plan.length > 0 && (
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setPriorityFilter('ALL')}
            className={`btn ${priorityFilter === 'ALL' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.85rem', padding: '6px 16px' }}
          >
            All Improvements ({plan.length})
          </button>
          <button
            onClick={() => setPriorityFilter('CRITICAL_HIGH')}
            className={`btn ${priorityFilter === 'CRITICAL_HIGH' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.85rem', padding: '6px 16px' }}
          >
            Critical / High Priority ({criticalHighCount})
          </button>
          <button
            onClick={() => setPriorityFilter('MEDIUM')}
            className={`btn ${priorityFilter === 'MEDIUM' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.85rem', padding: '6px 16px' }}
          >
            Medium Priority ({mediumCount})
          </button>
        </div>
      )}

      {plan.length === 0 ? (
        <div className="campus-card" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <CheckCircle2 size={48} color="#16A34A" style={{ marginBottom: '16px' }} />
          <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#0F172A', marginBottom: '8px' }}>
            All Competency Benchmarks Satisfied!
          </h3>
          <p style={{ color: '#64748B', maxWidth: '520px', margin: '0 auto 20px auto' }}>
            Your current academic metrics, problem-solving counts, and practical projects already match or exceed the median profiles of successfully placed alumni.
          </p>
          {onNavigate && (
            <button className="btn btn-primary" onClick={() => onNavigate('prediction')}>
              <Target size={16} /> Run Placement Assessment
            </button>
          )}
        </div>
      ) : (
        <div>
          {/* Priority Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px', marginBottom: '28px' }}>
            {filteredPlan.map((item, idx) => {
              const isCriticalOrHigh = item.priority === 'Critical' || item.priority === 'High';
              return (
                <div
                  key={idx}
                  className="campus-card"
                  style={{
                    borderLeft: `4px solid ${isCriticalOrHigh ? 'var(--error)' : 'var(--warning)'}`,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between'
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <span style={{ fontWeight: 800, fontSize: '1.05rem', color: 'var(--navy)' }}>{item.area}</span>
                      <span className="badge" style={{
                        background: isCriticalOrHigh ? 'var(--error-soft)' : 'var(--warning-soft)',
                        color: isCriticalOrHigh ? 'var(--error)' : 'var(--warning)',
                        border: `1px solid ${isCriticalOrHigh ? 'var(--error-border)' : 'var(--warning-border)'}`
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
                </div>
              );
            })}
          </div>

          {/* Structured Table showing ALL items */}
          <div className="campus-card" style={{ marginBottom: '28px' }}>
            <div className="campus-card-header">
              <div className="card-title">Structured Milestone Summary</div>
              <span className="badge badge-role">All {filteredPlan.length} Actionable Items</span>
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
                  {filteredPlan.map((row, i) => {
                    const isCriticalOrHigh = row.priority === 'Critical' || row.priority === 'High';
                    return (
                      <tr key={i}>
                        <td style={{ fontWeight: 700, color: '#0F172A' }}>{row.area}</td>
                        <td>
                          <span className="badge" style={{
                            background: isCriticalOrHigh ? 'var(--error-soft)' : 'var(--warning-soft)',
                            color: isCriticalOrHigh ? 'var(--error)' : 'var(--warning)',
                            border: `1px solid ${isCriticalOrHigh ? 'var(--error-border)' : 'var(--warning-border)'}`
                          }}>
                            {row.priority}
                          </span>
                        </td>
                        <td>{row.current_value}</td>
                        <td style={{ color: 'var(--primary)', fontWeight: 700 }}>{row.target_value}</td>
                        <td style={{ maxWidth: '420px', lineHeight: 1.5 }}>{row.actionable_recommendation}</td>
                      </tr>
                    );
                  })}
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
