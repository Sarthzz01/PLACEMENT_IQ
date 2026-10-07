import React, { useState } from 'react';
import { ArrowLeft, Lock, Mail, User, Shield, GraduationCap, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function LoginPage({ onLogin, onLoginSuccess, onBackHome, onNavigate, initialTab = 'login' }) {
  const [tab, setTab] = useState(initialTab);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('Student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const dispatchLogin = (userData) => {
    if (typeof onLogin === 'function') onLogin(userData);
    if (typeof onLoginSuccess === 'function') onLoginSuccess(userData);
  };

  const dispatchBack = () => {
    if (typeof onBackHome === 'function') onBackHome();
    if (typeof onNavigate === 'function') onNavigate('home');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to authenticate');
      }
      dispatchLogin(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Registration failed');
      }
      setSuccess('Account created successfully! Signing in...');
      setTimeout(() => {
        dispatchLogin(data.user);
      }, 700);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const quickFill = (userType) => {
    if (userType === 'student') {
      setEmail('student@college.com');
      setPassword('student123');
    } else {
      setEmail('admin@college.com');
      setPassword('admin123');
    }
  };

  return (
    <div style={{ background: '#F8FAFC', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div style={{ width: '100%', maxWidth: '440px' }}>
        <button
          onClick={dispatchBack}
          style={{ background: 'transparent', border: 'none', color: '#64748B', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.88rem', fontWeight: 600, cursor: 'pointer', marginBottom: '20px' }}
        >
          <ArrowLeft size={16} /> Back to Portal Overview
        </button>

        <div className="campus-card" style={{ padding: '32px' }}>
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '10px', background: '#2563EB', color: '#FFFFFF', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.25rem', boxShadow: '0 4px 12px rgba(37,99,235,0.4)', marginBottom: '12px' }}>
              IQ
            </div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0F172A' }}>PLACEMENT IQ</h2>
            <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Institutional Placement Intelligence Platform</p>
          </div>

          <div className="tabs-container" style={{ justifyContent: 'center', marginBottom: '24px' }}>
            <button
              className={`tab-btn ${tab === 'login' ? 'active' : ''}`}
              onClick={() => { setTab('login'); setError(''); setSuccess(''); }}
            >
              Sign In
            </button>
            <button
              className={`tab-btn ${tab === 'register' ? 'active' : ''}`}
              onClick={() => { setTab('register'); setError(''); setSuccess(''); }}
            >
              Register Candidate
            </button>
          </div>

          {error && (
            <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', color: '#DC2626', padding: '10px 14px', borderRadius: '8px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <AlertCircle size={16} /> {error}
            </div>
          )}

          {success && (
            <div style={{ background: '#F0FDF4', border: '1px solid #86EFAC', color: '#16A34A', padding: '10px 14px', borderRadius: '8px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <CheckCircle2 size={16} /> {success}
            </div>
          )}

          {tab === 'login' ? (
            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label className="form-label">Institutional Email</label>
                <input
                  type="email"
                  className="form-input"
                  required
                  placeholder="e.g. student@college.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  className="form-input"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: '11px', marginTop: '8px' }} disabled={loading}>
                {loading ? 'Authenticating...' : 'Sign In to Workspace'}
              </button>

              <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #F1F5F9' }}>
                <div style={{ fontSize: '0.78rem', color: '#64748B', fontWeight: 600, marginBottom: '8px', textAlign: 'center' }}>
                  QUICK LOGIN CREDENTIALS:
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ fontSize: '0.78rem', padding: '6px' }}
                    onClick={() => quickFill('student')}
                  >
                    Student Demo
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ fontSize: '0.78rem', padding: '6px' }}
                    onClick={() => quickFill('admin')}
                  >
                    Admin Demo
                  </button>
                </div>
              </div>
            </form>
          ) : (
            <form onSubmit={handleRegister}>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  className="form-input"
                  required
                  placeholder="e.g. John Doe"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Email Address</label>
                <input
                  type="email"
                  className="form-input"
                  required
                  placeholder="student@college.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  className="form-input"
                  required
                  placeholder="Create password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Account Role</label>
                <select
                  className="form-select"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                >
                  <option value="Student">Student Candidate</option>
                  <option value="Admin">Placement Officer / Admin</option>
                </select>
              </div>

              <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: '11px', marginTop: '8px' }} disabled={loading}>
                {loading ? 'Creating Account...' : 'Complete Registration'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
