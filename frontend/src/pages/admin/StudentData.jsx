import React, { useEffect, useState } from 'react';
import { Search, Filter, MessageSquare, CheckCircle2, User, Eye, Send, ExternalLink, Globe, Code } from 'lucide-react';

export default function StudentData({ user }) {
  const [students, setStudents] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState('');
  const [branchFilter, setBranchFilter] = useState('All');
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [feedbackNotes, setFeedbackNotes] = useState('');
  const [feedbackStatus, setFeedbackStatus] = useState('Reviewed');
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/students')
      .then(r => r.json())
      .then(d => {
        setStudents(d.students || []);
        setFiltered(d.students || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    let res = students;
    if (search.trim()) {
      const q = search.toLowerCase();
      res = res.filter(s => (s.name && s.name.toLowerCase().includes(q)) || (s.email && s.email.toLowerCase().includes(q)));
    }
    if (branchFilter !== 'All') {
      res = res.filter(s => s.branch === branchFilter);
    }
    setFiltered(res);
  }, [search, branchFilter, students]);

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    if (!selectedStudent) return;
    try {
      await fetch('/api/admin/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_email: selectedStudent.email,
          admin_name: user?.name || 'Prof. Shruti Agrawal',
          status: feedbackStatus,
          notes: feedbackNotes
        })
      });
      setMsg('Feedback saved to student records!');
      setFeedbackNotes('');
      setTimeout(() => setMsg(''), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Loading student directory...</div>;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Student Candidate Directory</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Inspect candidate profiles, evaluate readiness scores, and transmit official placement cell counseling notes.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="campus-card" style={{ padding: '16px 20px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#64748B' }} />
          <input
            type="text"
            className="form-input"
            style={{ paddingLeft: '36px' }}
            placeholder="Search candidate by name or institutional email..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={16} color="#64748B" />
          <select
            className="form-select"
            style={{ width: '180px' }}
            value={branchFilter}
            onChange={e => setBranchFilter(e.target.value)}
          >
            <option value="All">All Disciplines</option>
            <option value="CSE">Computer Science (CSE)</option>
            <option value="IT">Information Technology (IT)</option>
            <option value="ECE">Electronics (ECE)</option>
            <option value="ENTC">Telecommunication (ENTC)</option>
            <option value="Mechanical">Mechanical</option>
            <option value="Civil">Civil</option>
          </select>
        </div>

        <span className="badge badge-role">{filtered.length} Candidates</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: selectedStudent ? '1fr 380px' : '1fr', gap: '20px' }}>
        {/* Table */}
        <div className="campus-card" style={{ padding: 0, overflow: 'hidden' }}>
          <div className="table-container" style={{ border: 'none' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Email</th>
                  <th>Branch</th>
                  <th>CGPA</th>
                  <th>DSA Count</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((s, i) => {
                  const isPlaced = s.latest_prediction === 1;
                  return (
                    <tr key={i} style={{ background: selectedStudent?.email === s.email ? '#EFF6FF' : 'transparent' }}>
                      <td style={{ fontWeight: 700, color: '#0F172A' }}>{s.name}</td>
                      <td style={{ color: '#64748B', fontSize: '0.82rem' }}>{s.email}</td>
                      <td>{s.branch || 'CSE'}</td>
                      <td style={{ fontWeight: 600 }}>{s.cgpa || '7.5'}</td>
                      <td>{s.dsa_questions_solved ?? s.dsa_problems_solved ?? '—'}</td>
                      <td>
                        <span className={`badge ${isPlaced ? 'badge-placed' : 'badge-not-placed'}`}>
                          {isPlaced ? 'PLACED' : 'NEEDS PREP'}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '5px 10px', fontSize: '0.78rem' }}
                          onClick={() => setSelectedStudent(s)}
                        >
                          <Eye size={14} /> Review
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Drawer for Selected Student */}
        {selectedStudent && (
          <div className="campus-card" style={{ height: 'fit-content', position: 'sticky', top: '80px' }}>
            <div className="campus-card-header">
              <div>
                <div className="card-title">{selectedStudent.name}</div>
                <div className="card-subtitle">{selectedStudent.email}</div>
              </div>
              <button
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: '#64748B' }}
                onClick={() => setSelectedStudent(null)}
              >
                ✕
              </button>
            </div>

            <div style={{ marginBottom: '16px', fontSize: '0.85rem', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div><strong>Branch:</strong> {selectedStudent.branch || 'Computer Science'}</div>
              <div><strong>CGPA:</strong> {selectedStudent.cgpa || '7.8'}</div>
              <div><strong>DSA Problems:</strong> {selectedStudent.dsa_questions_solved ?? selectedStudent.dsa_problems_solved ?? 120}</div>
              <div><strong>LeetCode Solved:</strong> {selectedStudent.leetcode_questions_solved ?? selectedStudent.leetcode_problems_solved ?? '—'}</div>
              <div><strong>Public Repos:</strong> {selectedStudent.github_repos ?? selectedStudent.github_repos_count ?? '—'}</div>
              <div><strong>Projects Count:</strong> {selectedStudent.projects_count || 3}</div>
              <div><strong>Internships:</strong> {selectedStudent.internships_completed || 1}</div>
            </div>

            {/* Profile Links */}
            {(selectedStudent.leetcode_url || selectedStudent.github_url || selectedStudent.portfolio_url) && (
              <div style={{ marginBottom: '16px', padding: '10px 12px', background: '#F8FAFC', borderRadius: '8px', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#475569', marginBottom: '8px' }}>Verified Profile Links:</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {selectedStudent.leetcode_url && (
                    <a 
                      href={selectedStudent.leetcode_url.startsWith('http') ? selectedStudent.leetcode_url : `https://leetcode.com/u/${selectedStudent.leetcode_url}`} 
                      target="_blank" 
                      rel="noreferrer"
                      style={{ fontSize: '0.78rem', color: '#D97706', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}
                    >
                      <Code size={14} /> LeetCode Profile <ExternalLink size={12} />
                    </a>
                  )}
                  {selectedStudent.github_url && (
                    <a 
                      href={selectedStudent.github_url.startsWith('http') ? selectedStudent.github_url : `https://github.com/${selectedStudent.github_url}`} 
                      target="_blank" 
                      rel="noreferrer"
                      style={{ fontSize: '0.78rem', color: '#0F172A', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}
                    >
                      <Globe size={14} /> GitHub Profile <ExternalLink size={12} />
                    </a>
                  )}
                  {selectedStudent.portfolio_url && (
                    <a 
                      href={selectedStudent.portfolio_url.startsWith('http') ? selectedStudent.portfolio_url : `https://${selectedStudent.portfolio_url}`} 
                      target="_blank" 
                      rel="noreferrer"
                      style={{ fontSize: '0.78rem', color: '#2563EB', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}
                    >
                      <ExternalLink size={14} /> Portfolio / Website
                    </a>
                  )}
                </div>
              </div>
            )}

            {msg && (
              <div style={{ background: '#F0FDF4', color: '#16A34A', padding: '8px 12px', borderRadius: '6px', fontSize: '0.8rem', marginBottom: '12px' }}>
                {msg}
              </div>
            )}

            <form onSubmit={handleFeedbackSubmit}>
              <div className="form-group">
                <label className="form-label">Review Status</label>
                <select className="form-select" value={feedbackStatus} onChange={e => setFeedbackStatus(e.target.value)}>
                  <option value="Reviewed">Reviewed & Verified</option>
                  <option value="Needs Coding Training">Recommend Coding Training</option>
                  <option value="Eligible For Dream Drives">Fast-Track For Dream Drives</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Counseling Notes</label>
                <textarea
                  className="form-textarea"
                  rows={3}
                  placeholder="Provide targeted guidance for candidate dashboard..."
                  value={feedbackNotes}
                  onChange={e => setFeedbackNotes(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: '9px' }}>
                <Send size={15} /> Save & Deliver Notes
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
