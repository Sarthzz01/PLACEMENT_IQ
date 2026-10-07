import React, { useEffect, useState } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

export default function SkillAnalysis({ user }) {
  const [skillData, setSkillData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    setLoading(true);
    fetch(`/api/student/skills/${encodeURIComponent(studentEmail)}`)
      .then(r => r.json())
      .then(d => {
        setSkillData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [user]);

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Loading skill diagnostics...</div>;

  const categories = skillData?.student_scores ? Object.keys(skillData.student_scores) : [];
  const radarData = categories.map(cat => ({
    subject: cat,
    student: skillData.student_scores[cat],
    benchmark: skillData.benchmarks[cat]
  }));

  const barData = categories.map(cat => ({
    name: cat,
    Student: skillData.student_scores[cat],
    PlacedBenchmark: skillData.benchmarks[cat]
  }));

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Skill & Domain Analysis</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Multidimensional competency assessment benchmarking your credentials against successfully placed alumni.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Comprehensive Spider Radar Benchmark</div>
            <span className="badge badge-role">Multi-Axis Profile</span>
          </div>
          <div style={{ height: '340px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#E2E8F0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#0F172A', fontSize: 11, fontWeight: 600 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#CBD5E1" />
                <Radar name="Placed Benchmark" dataKey="benchmark" stroke="#2563EB" fill="#2563EB" fillOpacity={0.15} />
                <Radar name="Your Profile" dataKey="student" stroke="#16A34A" fill="#16A34A" fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Direct Competency Score Comparison</div>
            <span className="badge badge-role">Bar Metrics</span>
          </div>
          <div style={{ height: '340px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} layout="vertical" margin={{ left: 25, right: 20 }}>
                <XAxis type="number" stroke="#64748B" />
                <YAxis dataKey="name" type="category" stroke="#64748B" width={110} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="PlacedBenchmark" name="Placed Benchmark" fill="#2563EB" radius={[0, 4, 4, 0]} />
                <Bar dataKey="Student" name="Your Profile" fill="#16A34A" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
