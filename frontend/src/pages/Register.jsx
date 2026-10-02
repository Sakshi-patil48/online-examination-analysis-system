import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { GraduationCap, UserPlus, Lock, User, Mail, AlertCircle, ShieldCheck } from 'lucide-react';
import { registerUser, loginUser } from '../store/authSlice';

export default function Register() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('STUDENT');
  const [validationError, setValidationError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setValidationError('');

    if (password !== confirmPassword) {
      setValidationError('Passwords do not match.');
      return;
    }

    if (password.length < 8) {
      setValidationError('Password must be at least 8 characters long.');
      return;
    }

    const payload = {
      username: email,
      email,
      full_name: fullName,
      password,
      confirm_password: confirmPassword,
      role
    };

    const res = await dispatch(registerUser(payload));
    if (registerUser.fulfilled.match(res)) {
      // Auto login after successful registration
      const loginRes = await dispatch(loginUser({ username: email, password }));
      if (loginUser.fulfilled.match(loginRes)) {
        if (role === 'EXAMINER') {
          navigate('/examiner/dashboard');
        } else {
          navigate('/student/dashboard');
        }
      } else {
        navigate('/login');
      }
    }
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
          maxWidth: '480px',
          padding: '40px 32px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}
      >
        {/* Brand Header */}
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
          <h1 style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>Create SmartExams Account</h1>
          <p style={{ fontSize: '13px', color: '#64748b', textAlign: 'center' }}>
            Register to take assessments or manage proctored examinations.
          </p>
        </div>

        {(error || validationError) && (
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
            <span>{validationError || error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '4px', display: 'block' }}>
              Full Name
            </label>
            <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
              <User size={16} color="#94a3b8" />
              <input
                type="text"
                required
                placeholder="John Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '4px', display: 'block' }}>
              Email Address
            </label>
            <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
              <Mail size={16} color="#94a3b8" />
              <input
                type="email"
                required
                placeholder="name@domain.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '4px', display: 'block' }}>
                Password
              </label>
              <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
                <Lock size={16} color="#94a3b8" />
                <input
                  type="password"
                  required
                  placeholder="Min 8 chars"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '4px', display: 'block' }}>
                Confirm Password
              </label>
              <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
                <Lock size={16} color="#94a3b8" />
                <input
                  type="password"
                  required
                  placeholder="Repeat pass"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569', marginBottom: '4px', display: 'block' }}>
              Select Account Role
            </label>
            <div className="join-input-group" style={{ border: '1px solid #e2e8f0' }}>
              <ShieldCheck size={16} color="#94a3b8" />
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{ border: 'none', outline: 'none', width: '100%', fontSize: '14px', background: 'transparent' }}
              >
                <option value="STUDENT">Student / Examinee</option>
                <option value="EXAMINER">Examiner / Teacher</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center', padding: '12px', marginTop: '8px' }}
          >
            <UserPlus size={18} />
            <span>{loading ? 'Registering Account...' : 'Register Account'}</span>
          </button>

          <div style={{ textAlign: 'center', marginTop: '8px', fontSize: '13px', color: '#64748b' }}>
            Already have an account?{' '}
            <Link to="/login" style={{ color: '#324ed8', fontWeight: '600', textDecoration: 'none' }}>
              Sign In Here
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
