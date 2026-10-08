import React, { useEffect, useState } from 'react';
import { 
  Save, CheckCircle2, User, BookOpen, Code, Briefcase, 
  Award, FileCheck, RefreshCw, Sparkles, AlertCircle, ExternalLink, Globe 
} from 'lucide-react';

export default function StudentProfile({ user }) {
  const [profile, setProfile] = useState({
    age: 21,
    gender: 'Male',
    branch: 'CSE',
    cgpa: 7.8,
    backlogs: 0,
    attendance_percentage: 85,
    dsa_questions_solved: 120,
    dsa_problems_solved: 120,
    leetcode_questions_solved: 80,
    leetcode_problems_solved: 80,
    hackerrank_score: 65,
    coding_skill_score: 75,
    projects_count: 3,
    internships_completed: 1,
    hackathons_participated: 2,
    github_repos_count: 6,
    github_repos: 6,
    aptitude_score: 78,
    communication_score: 80,
    mock_interview_score: 75,
    placement_training_enrolled: 1,
    certifications_count: 2,
    extracurricular_activities: 1,
    github_url: '',
    leetcode_url: '',
    hackerrank_url: '',
    portfolio_url: ''
  });

  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');
  
  // Live profile fetch states
  const [fetchingStats, setFetchingStats] = useState(false);
  const [fetchResult, setFetchResult] = useState(null);
  const [fetchError, setFetchError] = useState('');

  useEffect(() => {
    const studentEmail = user?.email || (typeof window !== 'undefined' ? localStorage.getItem('placementiq_user_email') : null) || 'aarav.sharma@college.edu';
    fetch(`/api/student/profile/${encodeURIComponent(studentEmail)}`)
      .then(res => res.json())
      .then(data => {
        if (data.profile) {
          setProfile(prev => {
            const p = { ...prev, ...data.profile };
            // Ensure alias consistency
            if (p.leetcode_questions_solved !== undefined) p.leetcode_problems_solved = p.leetcode_questions_solved;
            if (p.dsa_questions_solved !== undefined) p.dsa_problems_solved = p.dsa_questions_solved;
            if (p.github_repos !== undefined) p.github_repos_count = p.github_repos;
            return p;
          });
        }
      })
      .catch(console.error);
  }, [user]);

  const handleChange = (field, val) => {
    setProfile(prev => {
      const updated = { ...prev, [field]: val };
      if (field === 'leetcode_problems_solved') updated.leetcode_questions_solved = val;
      if (field === 'leetcode_questions_solved') updated.leetcode_problems_solved = val;
      if (field === 'dsa_problems_solved') updated.dsa_questions_solved = val;
      if (field === 'dsa_questions_solved') updated.dsa_problems_solved = val;
      if (field === 'github_repos_count') updated.github_repos = val;
      if (field === 'github_repos') updated.github_repos_count = val;
      return updated;
    });
  };

  const handleFetchLiveStats = async () => {
    if (!profile.leetcode_url?.trim() && !profile.github_url?.trim()) {
      setFetchError('Please provide at least a LeetCode profile URL or GitHub profile URL/handle first.');
      setTimeout(() => setFetchError(''), 4500);
      return;
    }

    setFetchingStats(true);
    setFetchError('');
    setFetchResult(null);

    try {
      const res = await fetch('/api/student/fetch-external-stats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          github_url: profile.github_url || '',
          leetcode_url: profile.leetcode_url || '',
          hackerrank_url: profile.hackerrank_url || ''
        })
      });

      const data = await res.json();
      if (data && data.success) {
        setFetchResult(data);
        
        // Auto-update profile state with fetched values
        setProfile(prev => {
          const next = { ...prev };
          const ext = data.extracted_values || {};
          
          if (ext.leetcode_questions_solved !== undefined) {
            next.leetcode_questions_solved = ext.leetcode_questions_solved;
            next.leetcode_problems_solved = ext.leetcode_problems_solved;
          }
          if (ext.dsa_questions_solved !== undefined) {
            next.dsa_questions_solved = Math.max(prev.dsa_questions_solved || 0, ext.dsa_questions_solved);
            next.dsa_problems_solved = next.dsa_questions_solved;
          }
          if (ext.github_repos !== undefined) {
            next.github_repos = ext.github_repos;
            next.github_repos_count = ext.github_repos_count;
          }
          if (ext.coding_skill_score !== undefined) {
            next.coding_skill_score = Math.max(prev.coding_skill_score || 0, ext.coding_skill_score);
          }
          return next;
        });

        setMsg('Successfully fetched & synchronized live metrics from your links!');
        setTimeout(() => setMsg(''), 5000);
      } else {
        const errorMsg = data.messages && data.messages.length > 0 
          ? data.messages.join('. ') 
          : 'Could not fetch metrics from the specified links. Please check the URLs or handles.';
        setFetchError(errorMsg);
      }
    } catch (err) {
      console.error(err);
      setFetchError('Unable to connect to external profile services. Please check your network connection.');
    } finally {
      setFetchingStats(false);
    }
  };

  const handleSave = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
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
      setMsg('Profile and verified developer credentials saved to Data Warehouse!');
      setTimeout(() => setMsg(''), 4500);
    } catch (err) {
      console.error(err);
      setMsg('Error saving profile. Please try again.');
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
            Keep your academic, competitive coding platforms, and developer portfolio verified and synchronized.
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

      {fetchError && (
        <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', color: '#DC2626', padding: '12px 18px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px', fontWeight: 600 }}>
          <AlertCircle size={18} /> {fetchError}
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

        {/* Card 3: Live Profile Links & Auto-Sync */}
        <div className="campus-card">
          <div className="campus-card-header" style={{ flexWrap: 'wrap', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}>
                <Sparkles size={18} />
              </div>
              <div>
                <div className="card-title">3. Developer Profiles & Live Metric Synchronization</div>
                <div className="card-subtitle">
                  Connect your competitive coding handles and repositories to automatically extract and verify your credentials.
                </div>
              </div>
            </div>
            <button
              type="button"
              className="btn btn-primary"
              style={{ padding: '8px 18px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px' }}
              onClick={handleFetchLiveStats}
              disabled={fetchingStats}
            >
              <RefreshCw size={14} className={fetchingStats ? 'spin' : ''} />
              {fetchingStats ? 'Fetching Live Data...' : '⚡ Fetch & Auto-Fill Stats'}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px', marginBottom: '14px' }}>
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .271 3.518c.28.653.693 1.25 1.213 1.761l3.593 3.535 2.115 2.078c.306.3.71.469 1.144.469h.034c.433 0 .84-.165 1.144-.469l2.42-2.378a1.37 1.37 0 0 0 0-1.95 1.407 1.407 0 0 0-1.97 0l-1.94 1.905-1.785-1.754-3.52-3.463a2.766 2.766 0 0 1-.61-1.018 2.87 2.87 0 0 1-.093-1.074 2.81 2.81 0 0 1 .53-1.32l3.435-3.676 4.957-5.32c.54-.58.51-1.49-.07-2.03A1.4 1.4 0 0 0 13.483 0zm4.27 10.428h-6.72a1.385 1.385 0 0 0-1.38 1.38c0 .762.618 1.38 1.38 1.38h6.72c.762 0 1.38-.618 1.38-1.38a1.385 1.385 0 0 0-1.38-1.38z" fill="#FFA116"/>
                </svg>
                <span>LeetCode Profile URL or Handle</span>
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. https://leetcode.com/u/neal_wu/ or neal_wu"
                value={profile.leetcode_url || ''}
                onChange={e => handleChange('leetcode_url', e.target.value)}
              />
              <span style={{ fontSize: '0.74rem', color: '#64748B' }}>Extracts verified solved count (Easy/Medium/Hard) and global rank.</span>
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#0F172A">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
                <span>GitHub Profile URL or Username</span>
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. https://github.com/torvalds or torvalds"
                value={profile.github_url || ''}
                onChange={e => handleChange('github_url', e.target.value)}
              />
              <span style={{ fontSize: '0.74rem', color: '#64748B' }}>Extracts verified public repositories, followers, and open source work.</span>
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Code size={15} color="#059669" />
                <span>HackerRank Profile URL or Handle</span>
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. https://www.hackerrank.com/username"
                value={profile.hackerrank_url || ''}
                onChange={e => handleChange('hackerrank_url', e.target.value)}
              />
              <span style={{ fontSize: '0.74rem', color: '#64748B' }}>Optional platform profile link for verification and campus audit.</span>
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Globe size={15} color="#2563EB" />
                <span>Portfolio / Personal LinkedIn Website</span>
              </label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. https://myportfolio.dev or LinkedIn URL"
                value={profile.portfolio_url || ''}
                onChange={e => handleChange('portfolio_url', e.target.value)}
              />
              <span style={{ fontSize: '0.74rem', color: '#64748B' }}>Personal projects portfolio, deployed web apps, or LinkedIn profile.</span>
            </div>
          </div>

          {/* Real-time Fetched Metrics Summary Banner */}
          {fetchResult && (
            <div style={{ background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '10px', padding: '16px', marginTop: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontWeight: 700, color: '#0F172A', fontSize: '0.92rem' }}>
                <CheckCircle2 size={18} color="#16A34A" /> Live Verified Credentials Extracted:
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '14px' }}>
                {fetchResult.leetcode && (
                  <div style={{ background: '#FFFFFF', border: '1px solid #FED7AA', padding: '14px', borderRadius: '8px', borderLeft: '4px solid #F97316' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <span style={{ fontWeight: 700, color: '#9A3412', fontSize: '0.86rem' }}>LeetCode: @{fetchResult.leetcode.username}</span>
                      {fetchResult.leetcode.ranking && (
                        <span style={{ fontSize: '0.72rem', color: '#C2410C', background: '#FFEDD5', padding: '2px 8px', borderRadius: '12px', fontWeight: 600 }}>
                          Rank #{fetchResult.leetcode.ranking.toLocaleString()}
                        </span>
                      )}
                    </div>
                    <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#7C2D12' }}>
                      {fetchResult.leetcode.total_solved} <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#9A3412' }}>Problems Solved</span>
                    </div>
                    <div style={{ display: 'flex', gap: '6px', marginTop: '6px', flexWrap: 'wrap' }}>
                      <span style={{ fontSize: '0.74rem', background: '#ECFDF5', color: '#047857', padding: '2px 6px', borderRadius: '4px', fontWeight: 600 }}>Easy: {fetchResult.leetcode.easy_solved}</span>
                      <span style={{ fontSize: '0.74rem', background: '#FEF3C7', color: '#B45309', padding: '2px 6px', borderRadius: '4px', fontWeight: 600 }}>Medium: {fetchResult.leetcode.medium_solved}</span>
                      <span style={{ fontSize: '0.74rem', background: '#FEE2E2', color: '#B91C1C', padding: '2px 6px', borderRadius: '4px', fontWeight: 600 }}>Hard: {fetchResult.leetcode.hard_solved}</span>
                    </div>
                  </div>
                )}

                {fetchResult.github && (
                  <div style={{ background: '#FFFFFF', border: '1px solid #E2E8F0', padding: '14px', borderRadius: '8px', borderLeft: '4px solid #0F172A' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <span style={{ fontWeight: 700, color: '#0F172A', fontSize: '0.86rem' }}>GitHub: @{fetchResult.github.username}</span>
                      <span style={{ fontSize: '0.72rem', color: '#475569', background: '#F1F5F9', padding: '2px 8px', borderRadius: '12px', fontWeight: 600 }}>
                        {fetchResult.github.followers} Followers
                      </span>
                    </div>
                    <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#0F172A' }}>
                      {fetchResult.github.public_repos} <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569' }}>Public Repositories</span>
                    </div>
                    <div style={{ fontSize: '0.76rem', color: '#64748B', marginTop: '6px' }}>
                      {fetchResult.github.name ? `Account: ${fetchResult.github.name}` : 'Public Open Source Profile'}
                    </div>
                  </div>
                )}
              </div>
              <div style={{ marginTop: '12px', fontSize: '0.82rem', color: '#16A34A', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={15} /> All corresponding metrics in Section 4 & Section 5 below have been automatically synchronized!
              </div>
            </div>
          )}
        </div>

        {/* Card 4: Coding & Problem Solving */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Code size={18} /></div>
              <div className="card-title">4. Coding & Problem Solving Platforms</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px' }}>
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>LeetCode Problems Solved</span>
                {profile.leetcode_url && <span style={{ fontSize: '0.74rem', color: '#2563EB', fontWeight: 700, background: '#EFF6FF', padding: '1px 8px', borderRadius: '10px' }}>⚡ Auto-Synced</span>}
              </label>
              <input type="number" min="0" className="form-input" value={profile.leetcode_problems_solved ?? profile.leetcode_questions_solved ?? 0} onChange={e => handleChange('leetcode_problems_solved', parseInt(e.target.value) || 0)} />
            </div>
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>DSA Problems Solved (Total)</span>
                {profile.leetcode_url && <span style={{ fontSize: '0.74rem', color: '#2563EB', fontWeight: 700, background: '#EFF6FF', padding: '1px 8px', borderRadius: '10px' }}>⚡ Auto-Calculated</span>}
              </label>
              <input type="number" min="0" className="form-input" value={profile.dsa_problems_solved ?? profile.dsa_questions_solved ?? 0} onChange={e => handleChange('dsa_problems_solved', parseInt(e.target.value) || 0)} />
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

        {/* Card 5: Projects & Experience */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Briefcase size={18} /></div>
              <div className="card-title">5. Projects & Professional Experience</div>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '18px' }}>
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
              <label className="form-label" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>Public GitHub Repositories</span>
                {profile.github_url && <span style={{ fontSize: '0.74rem', color: '#2563EB', fontWeight: 700, background: '#EFF6FF', padding: '1px 8px', borderRadius: '10px' }}>⚡ Auto-Synced</span>}
              </label>
              <input type="number" min="0" className="form-input" value={profile.github_repos_count ?? profile.github_repos ?? 0} onChange={e => handleChange('github_repos_count', parseInt(e.target.value) || 0)} />
            </div>
          </div>
        </div>

        {/* Card 6: Soft Skills & Aptitude */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><Award size={18} /></div>
              <div className="card-title">6. Soft Skills & Aptitude Evaluations</div>
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

        {/* Card 7: Placement Preparation */}
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ padding: '6px', background: '#EFF6FF', color: '#2563EB', borderRadius: '6px' }}><FileCheck size={18} /></div>
              <div className="card-title">7. Placement Training & Credentials</div>
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
