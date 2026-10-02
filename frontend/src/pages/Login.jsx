import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { GraduationCap, LogIn, Lock, User, AlertCircle } from 'lucide-react';
import { loginUser } from '../store/authSlice';

export default function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);

  const [username, setUsername] = useState('student@smartexams.com');
  const [password, setPassword] = useState('student123');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(loginUser({ username, password }));
    if (loginUser.fulfilled.match(result)) {
      const role = result.payload.user?.role;
      if (role === 'EXAMINER') {
        navigate('/examiner/dashboard');
      } else if (role === 'ADMIN') {
        navigate('/admin/dashboard');
      } else {
        navigate('/student/dashboard');
      }
    }
  };

  const handleQuickDemo = (demoEmail, demoPass) => {
    setUsername(demoEmail);
    setPassword(demoPass);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#f1f4f9',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}
    >
      <div
        className="card"
        style={{
          width: '100%',
          maxWidth: '440px',
          padding: '40px 32px',
          display: 'flex',
          flexDirection: 'column',
          gap: '24px'
        }}
      >
        {/* Brand Logo */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '56px',
              height: '56px',
              borderRadius: '50%',
              backgroundColor: '#2a3b8f',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <GraduationCap size={32} color="#ffffff" />
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>SmartExams</h1>
          <p style={{ fontSize: '13px', color: '#64748b', textAlign: 'center' }}>
            AI-Powered Examination & Performance Platform
          </p>
        </div>

        {/* Demo Quick Logins */}
        <div
          style={{
            background: '#eef2ff',
            padding: '12px',
            borderRadius: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
        >
          <span style={{ fontSize: '11px', fontWeight: '700', color: '#3730a3', textTransform: 'uppercase' }}>
            Quick Demo Credentials:
          </span>
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => handleQuickDemo('student@smartexams.com', 'student123')}
              style={{
                fontSize: '11px',
                padding: '5px 10px',
                borderRadius: '6px',
                border: '1px solid #c7d2fe',
                background: '#ffffff',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              🎓 Student
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemo('teacher@smartexams.com', 'teacher123')}
              style={{
                fontSize: '11px',
                padding: '5px 10px',
                borderRadius: '6px',
                border: '1px solid #c7d2fe',
                background: '#ffffff',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              👩‍🏫 Teacher
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemo('admin@smartexams.com', 'admin123')}
              style={{
                fontSize: '11px',
                padding: '5px 10px',
                borderRadius: '6px',
                border: '1px solid #c7d2fe',
                background: '#ffffff',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              🛡️ Admin
            </button>
          </div>
        </div>

        {error && (
          <div
            style={{
              padding: '10px 14px',
              backgroundColor: '#fee2e2',
              color: '#dc2626',
              borderRadius: '8px',
              fontSize: '13px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '6px', display: 'block' }}>
              Username / Email
            </label>
            <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
              <User size={16} color="#94a3b8" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter email or username"
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '6px', display: 'block' }}>
              Password
            </label>
            <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
              <Lock size={16} color="#94a3b8" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px' }}>
            <span style={{ color: '#94a3b8' }}>Forgot Password? (Contact Admin)</span>
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center', padding: '12px', marginTop: '4px' }}
          >
            <LogIn size={18} />
            <span>{loading ? 'Authenticating...' : 'Sign In'}</span>
          </button>

          <div style={{ textAlign: 'center', marginTop: '8px', fontSize: '13px', color: '#64748b' }}>
            Don't have an account?{' '}
            <Link to="/register" style={{ color: '#324ed8', fontWeight: '600', textDecoration: 'none' }}>
              Register Here
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
