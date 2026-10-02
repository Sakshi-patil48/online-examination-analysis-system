import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';
import { useSelector } from 'react-redux';

export default function Unauthorized() {
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);

  const handleBack = () => {
    if (user?.role === 'EXAMINER') {
      navigate('/examiner/dashboard');
    } else if (user?.role === 'ADMIN') {
      navigate('/admin/dashboard');
    } else {
      navigate('/student/dashboard');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: '16px', textAlign: 'center' }}>
      <div style={{ padding: '16px', borderRadius: '50%', background: '#fee2e2' }}>
        <ShieldAlert size={48} color="#dc2626" />
      </div>
      <h1 style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>Access Denied (HTTP 403)</h1>
      <p style={{ fontSize: '14px', color: '#64748b', maxWidth: '400px' }}>
        You do not have permission to view this resource. Your account role ({user?.role || 'Guest'}) is restricted from accessing this route.
      </p>
      <button className="btn-primary" onClick={handleBack} style={{ marginTop: '8px' }}>
        <ArrowLeft size={16} />
        <span>Return to Authorized Dashboard</span>
      </button>
    </div>
  );
}
