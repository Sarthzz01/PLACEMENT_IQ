import React, { useEffect, useState } from 'react';
import { Save, CheckCircle2, User, BookOpen, Code, Briefcase, Award, FileCheck } from 'lucide-react';

export default function StudentProfile({ user }) {
  const [profile, setProfile] = useState({
    age: 21,
    gender: 'Male',
    branch: 'CSE',
    cgpa: 7.8,
    backlogs: 0,
    attendance_percentage: 85,
    dsa_questions_solved: 120,
    leetcode_questions_solved: 80,
    hackerrank_score: 65,
    coding_skill_score: 75,
    projects_count: 3,
    internships_completed: 1,
    hackathons_participated: 2,
    github_repos_count: 6,
    aptitude_score: 78,
    communication_score: 80,
    mock_interview_score: 75,
    placement_training_enrolled: 1,
    certifications_count: 2,
    extracurricular_activities: 1
  });

  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    fetch(`/api/student/profile/${encodeURIComponent(studentEmail)}`)
      .then(res => res.json())
      .then(data => {
        if (data.profile) {
          setProfile(prev => ({ ...prev, ...data.profile }));
        }
      })
      .catch(console.error);
  }, [user]);

  const handleChange = (field, val) => {
    setProfile(prev => ({ ...prev, [field]: val }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMsg('');

    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    try {
      const res = await fetch('/api/student/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: studentEmail, data: profile })
      });
      const data = await res.json();
      setMsg('Profile saved and synced with Data Warehouse!');
      setTimeout(() => setMsg(''), 4000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>My Placement Profile</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Keep your academic, competitive programming, and co-curricular credentials up to date.
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          <Save size={18} /> {saving ? 'Saving...' : 'Save & Sync Profile'}
        </button>
      </div>

      {msg && (
        <div style={{ background: '#F0FDF4', border: '1px solid #86EFAC', color: '#16A34A', padding: '12px 18px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px', fontWeight: 600 }}>
          <CheckCircle2 size={18} /> {msg}
        </div>
      )}

      <form onSubmit={handleSave}>
        {/* Card 1: Personal & Demographics */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><User size={18} /></div>
              <div className="card-title">1. Personal & Demographics</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Age</label>
              <input type="number" className="form-input" value={profile.age} onChange={e => handleChange('age', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Gender</label>
              <select className="form-select" value={profile.gender} onChange={e => handleChange('gender', e.target.value)}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Engineering Branch</label>
              <select className="form-select" value={profile.branch} onChange={e => handleChange('branch', e.target.value)}>
                <option value="CSE">Computer Science & Engineering (CSE)</option>
                <option value="IT">Information Technology (IT)</option>
                <option value="ECE">Electronics & Communication (ECE)</option>
                <option value="ENTC">Electronics & Telecomm (ENTC)</option>
                <option value="Mechanical">Mechanical Engineering</option>
                <option value="Civil">Civil Engineering</option>
              </select>
            </div>
          </div>
        </div>

        {/* Card 2: Academic Record */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><BookOpen size={18} /></div>
              <div className="card-title">2. Academic Record</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Cumulative CGPA (0 - 10.0)</label>
              <input type="number" step="0.01" max="10" min="0" className="form-input" value={profile.cgpa} onChange={e => handleChange('cgpa', parseFloat(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Active Academic Backlogs</label>
              <input type="number" min="0" className="form-input" value={profile.backlogs} onChange={e => handleChange('backlogs', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Attendance Percentage (%)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.attendance_percentage} onChange={e => handleChange('attendance_percentage', parseFloat(e.target.value) || 0)} />
            </div>
          </div>
        </div>

        {/* Card 3: Coding & Problem Solving */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Code size={18} /></div>
              <div className="card-title">3. Coding & Problem Solving Platforms</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">DSA Problems Solved</label>
              <input type="number" min="0" className="form-input" value={profile.dsa_problems_solved} onChange={e => handleChange('dsa_problems_solved', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">LeetCode Problems Solved</label>
              <input type="number" min="0" className="form-input" value={profile.leetcode_problems_solved} onChange={e => handleChange('leetcode_problems_solved', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">HackerRank Score (0 - 100)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.hackerrank_score} onChange={e => handleChange('hackerrank_score', parseFloat(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Coding Skill Assessment (0 - 100)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.coding_skill_score} onChange={e => handleChange('coding_skill_score', parseFloat(e.target.value) || 0)} />
            </div>
          </div>
        </div>

        {/* Card 4: Projects & Experience */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Briefcase size={18} /></div>
              <div className="card-title">4. Projects & Professional Experience</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Completed Technical Projects</label>
              <input type="number" min="0" className="form-input" value={profile.projects_count} onChange={e => handleChange('projects_count', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Internships Completed</label>
              <input type="number" min="0" className="form-input" value={profile.internships_completed} onChange={e => handleChange('internships_completed', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Hackathons Participated</label>
              <input type="number" min="0" className="form-input" value={profile.hackathons_participated} onChange={e => handleChange('hackathons_participated', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Public GitHub Repositories</label>
              <input type="number" min="0" className="form-input" value={profile.github_repos_count} onChange={e => handleChange('github_repos_count', parseInt(e.target.value) || 0)} />
            </div>
          </div>
        </div>

        {/* Card 5: Soft Skills & Aptitude */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Award size={18} /></div>
              <div className="card-title">5. Soft Skills & Aptitude Evaluations</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Quantitative Aptitude Score (0 - 100)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.aptitude_score} onChange={e => handleChange('aptitude_score', parseFloat(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Communication Score (0 - 100)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.communication_score} onChange={e => handleChange('communication_score', parseFloat(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Mock Interview Score (0 - 100)</label>
              <input type="number" max="100" min="0" className="form-input" value={profile.mock_interview_score} onChange={e => handleChange('mock_interview_score', parseFloat(e.target.value) || 0)} />
            </div>
          </div>
        </div>

        {/* Card 6: Placement Preparation */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><FileCheck size={18} /></div>
              <div className="card-title">6. Placement Training & Credentials</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Placement Training Program</label>
              <select className="form-select" value={profile.placement_training_enrolled} onChange={e => handleChange('placement_training_enrolled', parseInt(e.target.value) || 0)}>
                <option value={1}>Enrolled / Completed</option>
                <option value={0}>Not Enrolled</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Industry Certifications</label>
              <input type="number" min="0" className="form-input" value={profile.certifications_count} onChange={e => handleChange('certifications_count', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label">Extracurricular Engagement</label>
              <select className="form-select" value={profile.extracurricular_activities} onChange={e => handleChange('extracurricular_activities', parseInt(e.target.value) || 0)}>
                <option value={1}>Active Participation</option>
                <option value={0}>No Participation</option>
              </select>
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'right', marginTop: '20px' }}>
          <button type="submit" className="btn btn-primary" style={{ padding: '12px 28px', fontSize: '1rem' }} disabled={saving}>
            <Save size={18} /> {saving ? 'Saving Profile...' : 'Save & Sync Profile'}
          </button>
        </div>
      </form>
    </div>
  );
}
