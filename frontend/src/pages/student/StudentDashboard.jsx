import React, { useEffect, useState } from 'react';
import { Target, CheckCircle2, AlertCircle, Award, ArrowRight, TrendingUp, BookOpen, Clock } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import KPICard from '../../components/KPICard';

export default function StudentDashboard({ user, onNavigate }) {
  const [data, setData] = useState(null);
  const [radarData, setRadarData] = useState([]);
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    setLoading(true);

    Promise.all([
      fetch(`/api/student/dashboard/${encodeURIComponent(studentEmail)}`).then(r => r.json()),
      fetch(`/api/student/skills/${encodeURIComponent(studentEmail)}`).then(r => r.json()),
      fetch(`/api/student/plan/${encodeURIComponent(studentEmail)}`).then(r => r.json())
    ]).then(([dashData, skillData, planData]) => {
      setData(dashData);
      const rawPlan = planData?.plan?.all_improvements || planData?.plan?.top_improvements || (Array.isArray(planData?.plan) ? planData?.plan : []);
      const normalizedPlan = (rawPlan || []).map(p => ({
        area: p.area || p.title || p.feature || 'Competency Area',
        priority: p.priority || 'Medium',
        current_value: `${p.current_value ?? p.student_val ?? '—'} ${p.unit || ''}`.trim(),
        target_value: `${p.target_value ?? p.benchmark_val ?? '—'} ${p.unit || ''}`.trim(),
        actionable_recommendation: p.actionable_recommendation || p.advice || 'Continue deliberate practice.'
      }));
      setPlan(normalizedPlan);

      if (skillData?.student_scores && skillData?.benchmarks) {
        const categories = Object.keys(skillData.student_scores);
        const transformed = categories.map(cat => ({
          subject: cat,
          student: skillData.student_scores[cat],
          benchmark: skillData.benchmarks[cat]
        }));
        setRadarData(transformed);
      }
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [user]);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#64748B' }}>Loading placement workspace...</div>;
  }

  const latestPred = data?.latest_prediction;
  const isPlaced = (latestPred?.predicted_status === 'Placed') || (latestPred?.status === 'Placed') || (latestPred?.prediction === 1) || (Number(latestPred?.probability) >= 0.5);
  const prob = latestPred ? (Number(latestPred.probability) * 100).toFixed(1) : null;
  const cgpa = data?.profile?.cgpa || '7.5';

  return (
    <div>
      {/* Welcome Banner */}
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>
          Welcome back, {user?.name || 'Student'} 👋
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Here is your comprehensive placement readiness and competency intelligence overview.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <KPICard
          title="Placement Status"
          value={latestPred ? (isPlaced ? 'PLACED' : 'NOT PLACED') : 'PENDING'}
          subtitle={latestPred ? `${prob}% Model Confidence` : 'Run your first prediction'}
          icon={<Target size={24} />}
          iconColor={latestPred ? (isPlaced ? 'green' : 'red') : 'blue'}
        />
        <KPICard
          title="Profile Completeness"
          value={`${data?.completeness || 0}%`}
          subtitle={data?.completeness >= 85 ? 'Profile fully verified' : 'Update pending credentials'}
          icon={<CheckCircle2 size={24} />}
          iconColor={data?.completeness >= 85 ? 'green' : 'amber'}
        />
        <KPICard
          title="Cumulative CGPA"
          value={cgpa}
          subtitle="Out of 10.0 scale"
          icon={<Award size={24} />}
          iconColor="blue"
        />
        <KPICard
          title="Placement Readiness Index"
          value={`${data?.skill_score || 72}%`}
          subtitle="Composite competency score"
          icon={<TrendingUp size={24} />}
          iconColor="purple"
        />
      </div>

      {/* Main Charts & Status Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        {/* Left: Radar Chart */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Placement Readiness Overview</div>
              <div className="card-subtitle">Your competency scores vs. placed cohort benchmarks</div>
            </div>
            <button className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 12px' }} onClick={() => onNavigate('skills')}>
              Deep Dive
            </button>
          </div>

          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#E2E8F0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#0F172A', fontSize: 12, fontWeight: 600 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#CBD5E1" />
                <Radar name="Placed Cohort" dataKey="benchmark" stroke="#2563EB" fill="#2563EB" fillOpacity={0.15} />
                <Radar name="Your Profile" dataKey="student" stroke="#16A34A" fill="#16A34A" fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', fontSize: '0.82rem', marginTop: '10px' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#2563EB', fontWeight: 600 }}>
              <span style={{ width: '12px', height: '12px', background: '#2563EB', borderRadius: '3px' }}></span> Placed Benchmark
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#16A34A', fontWeight: 600 }}>
              <span style={{ width: '12px', height: '12px', background: '#16A34A', borderRadius: '3px' }}></span> Your Profile
            </span>
          </div>
        </div>

        {/* Right: Recent Prediction Status */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Latest Placement Prediction</div>
              <div className="card-subtitle">Output from trained institutional model</div>
            </div>
            <button className="btn btn-primary" style={{ fontSize: '0.8rem', padding: '6px 12px' }} onClick={() => onNavigate('prediction')}>
              Re-Calculate
            </button>
          </div>

          {latestPred ? (
            <div>
              <div style={{
                background: isPlaced ? 'var(--success-soft)' : 'var(--error-soft)',
                border: `1px solid ${isPlaced ? 'var(--success-border)' : 'var(--error-border)'}`,
                borderRadius: '12px',
                padding: '24px',
                textAlign: 'center',
                marginBottom: '20px'
              }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: isPlaced ? '#16A34A' : '#DC2626', marginBottom: '4px' }}>
                  PREDICTED OUTCOME
                </div>
                <div style={{ fontSize: '2.4rem', fontWeight: 900, color: isPlaced ? '#16A34A' : '#DC2626', marginBottom: '8px' }}>
                  {isPlaced ? 'PLACED' : 'NEEDS PREPARATION'}
                </div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#0F172A' }}>
                  {prob}% Probability
                </div>
                <div style={{ fontSize: '0.85rem', color: '#64748B', marginTop: '4px' }}>
                  Evaluated with {latestPred.model_name || 'Random Forest'} Classifier
                </div>
              </div>

              {data?.recent_feedback && data.recent_feedback.length > 0 && (
                <div style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '10px', padding: '14px' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 700, textTransform: 'uppercase', color: '#0F172A', marginBottom: '6px' }}>
                    Placement Cell Notes
                  </div>
                  <div style={{ fontSize: '0.88rem', color: '#334155' }}>
                    "{data.recent_feedback[0].notes}"
                  </div>
                  <div style={{ fontSize: '0.74rem', color: '#64748B', marginTop: '4px' }}>
                    Reviewed by {data.recent_feedback[0].admin_name} • {data.recent_feedback[0].timestamp}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: '#64748B' }}>
              <Target size={48} style={{ opacity: 0.3, marginBottom: '12px' }} />
              <h4>No prediction generated yet</h4>
              <p style={{ fontSize: '0.88rem', marginTop: '6px', marginBottom: '16px' }}>
                Run your first prediction against our verified machine learning models to unlock your personalized placement trajectory.
              </p>
              <button className="btn btn-primary" onClick={() => onNavigate('prediction')}>
                Generate Prediction Now
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Areas to Improve */}
      <div className="campus-card">
        <div className="campus-card-header">
          <div>
            <div className="card-title">Priority Areas to Improve</div>
            <div className="card-subtitle">Calculated gaps against historical median values of successfully placed students</div>
          </div>
          <button className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 12px' }} onClick={() => onNavigate('plan')}>
            View Full Action Plan
          </button>
        </div>

        {plan && plan.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
            {plan.slice(0, 3).map((item, idx) => (
              <div key={idx} style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '10px', padding: '18px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#0F172A' }}>{item.area}</span>
                  <span className="badge" style={{ background: item.priority === 'High' ? '#FEF2F2' : '#FFFBEB', color: item.priority === 'High' ? '#DC2626' : '#D97706' }}>
                    {item.priority} Priority
                  </span>
                </div>
                <div style={{ fontSize: '0.85rem', color: '#64748B', marginBottom: '8px' }}>
                  Your value: <strong style={{ color: '#0F172A' }}>{item.current_value}</strong> • Placed median: <strong style={{ color: '#2563EB' }}>{item.target_value}</strong>
                </div>
                <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.5 }}>
                  {item.actionable_recommendation}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ color: '#16A34A', display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 0' }}>
            <CheckCircle2 size={18} /> Excellent! Your profile currently meets or exceeds median benchmarks across all evaluated dimensions.
          </div>
        )}
      </div>
    </div>
  );
}
