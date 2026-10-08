import React, { useState, useEffect } from 'react';
import { Target, CheckCircle2, AlertTriangle, ArrowRight, Sparkles, TrendingUp } from 'lucide-react';

const DEFAULT_PROFILE = {
  cgpa: 8.2,
  backlogs: 0,
  attendance_percentage: 88,
  dsa_questions_solved: 240,
  leetcode_questions_solved: 160,
  hackerrank_questions_solved: 80,
  coding_skill_score: 8.2,
  projects_count: 3,
  internships_count: 1,
  hackathons_count: 2,
  github_repos: 8,
  aptitude_score: 76,
  communication_score: 8.0,
  mock_interview_score: 8.0,
  placement_training: 'Yes',
  branch: 'CSE',
  gender: 'Male',
  age: 21
};

export default function PlacementPrediction({ user, onNavigate }) {
  const [profile, setProfile] = useState(DEFAULT_PROFILE);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    fetch(`/api/student/profile/${encodeURIComponent(studentEmail)}`)
      .then(res => res.json())
      .then(data => {
        if (data.profile && Object.keys(data.profile).length > 0) {
          setProfile(prev => ({ ...prev, ...data.profile }));
        }
      })
      .catch(console.error);
  }, [user]);

  const handlePredict = async () => {
    setLoading(true);
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    try {
      const res = await fetch('/api/student/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: studentEmail, data: profile })
      });
      const data = await res.json();
      setPrediction(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const isPlaced = (prediction?.status === 'Placed') || (prediction?.prediction === 1) || (Number(prediction?.probability) >= 0.5);
  const prob = prediction ? (Number(prediction.probability) * 100).toFixed(1) : null;
  const rawImprovements = prediction?.all_improvements || prediction?.top_improvements || prediction?.recommendations || [];

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Real-Time Placement Assessment Engine</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Evaluate your placement likelihood based on institutional analytics and benchmarks derived from 15,000+ candidate records.
        </p>
      </div>

      {/* Action Card */}
      <div className="campus-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: '#EFF6FF', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Sparkles size={22} color="var(--primary)" />
          </div>
          <div>
            <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--navy)' }}>Automated Placement Assessment</div>
            <div style={{ fontSize: '0.82rem', color: '#64748B' }}>Analyzes your current academics, coding milestones, and co-curricular credentials</div>
          </div>
        </div>

        <button className="btn btn-primary" style={{ padding: '12px 28px', fontSize: '0.95rem' }} onClick={handlePredict} disabled={loading}>
          <Target size={18} /> {loading ? 'Evaluating Readiness...' : 'Calculate Placement Readiness'}
        </button>
      </div>

      {/* Prediction Result Card */}
      {prediction && (
        <div style={{
          background: isPlaced ? 'var(--success-soft)' : 'var(--error-soft)',
          border: `1px solid ${isPlaced ? 'var(--success-border)' : 'var(--error-border)'}`,
          borderRadius: '16px',
          padding: '36px',
          textAlign: 'center',
          marginBottom: '28px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
        }}>
          <span style={{
            display: 'inline-block',
            fontSize: '0.82rem',
            fontWeight: 800,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: isPlaced ? 'var(--success)' : 'var(--error)',
            background: isPlaced ? '#DCFCE7' : '#FEE2E2',
            padding: '4px 14px',
            borderRadius: '999px',
            marginBottom: '12px'
          }}>
            OFFICIAL PLACEMENT READINESS ASSESSMENT
          </span>

          <div style={{ fontSize: '3rem', fontWeight: 900, color: isPlaced ? 'var(--success)' : 'var(--error)', lineHeight: 1.1, marginBottom: '8px' }}>
            {isPlaced ? 'PLACED' : 'NEEDS PREPARATION'}
          </div>

          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--navy)', marginBottom: '8px' }}>
            {prob}% Placement Probability Score
          </div>

          <p style={{ color: '#475569', maxWidth: '600px', margin: '0 auto', fontSize: '0.95rem' }}>
            {isPlaced
              ? 'Congratulations! Your current academic standing, competitive coding milestones, and practical projects place you comfortably within the successfully placed alumni cohort.'
              : 'Your evaluated credentials fall below benchmark medians in specific technical or co-curricular areas. Review the targeted recommendations below to elevate your placement profile.'}
          </p>

          <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <button className="btn btn-secondary" onClick={() => onNavigate('plan')}>
              View Detailed Improvement Plan <ArrowRight size={16} />
            </button>
            <button className="btn btn-secondary" onClick={() => onNavigate('skills')}>
              View Skill Radar Benchmarks
            </button>
          </div>
        </div>
      )}

      {/* Target Improvements */}
      {rawImprovements.length > 0 && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div>
              <div className="card-title">Empirical Gaps Identified</div>
              <div className="card-subtitle">Key metrics where your current numbers differ from placed cohort medians</div>
            </div>
            <button className="btn btn-secondary" onClick={() => onNavigate('plan')}>
              Explore Remediation Roadmap <ArrowRight size={16} />
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
            {rawImprovements.slice(0, 4).map((rec, i) => (
              <div key={i} style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 800, color: 'var(--navy)', fontSize: '1rem' }}>
                    {rec.title || rec.feature || 'Competency Domain'}
                  </span>
                  <span className="badge" style={{
                    background: rec.priority === 'High' ? 'var(--error-soft)' : 'var(--warning-soft)',
                    color: rec.priority === 'High' ? 'var(--error)' : 'var(--warning)',
                    border: `1px solid ${rec.priority === 'High' ? 'var(--error-border)' : 'var(--warning-border)'}`
                  }}>
                    {rec.priority || 'Medium'} Priority
                  </span>
                </div>

                <div style={{ fontSize: '0.85rem', color: '#64748B', marginBottom: '10px' }}>
                  Your score: <strong style={{ color: '#0F172A' }}>{rec.student_val ?? rec.current ?? '—'} {rec.unit || ''}</strong> • Placed Median: <strong style={{ color: 'var(--primary)' }}>{rec.benchmark_val ?? rec.median ?? '—'} {rec.unit || ''}</strong>
                </div>

                <p style={{ fontSize: '0.88rem', color: '#334155', lineHeight: 1.5 }}>
                  {rec.advice || rec.actionable_recommendation}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
