import React, { useEffect, useState } from 'react';
import { Shield, Users, FileText, AlertTriangle } from 'lucide-react';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_users: 0,
    total_students: 0,
    total_examiners: 0,
    total_exams: 0,
    total_attempts: 0,
    total_proctor_flags: 0
  });

  useEffect(() => {
    api.get('admin/stats/').then(res => setStats(res.data)).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/admin/dashboard' }, { label: 'Admin Portal' }]} />
      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>System Administration Overview</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#e0e7ff', borderRadius: '50%' }}>
            <Users size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>TOTAL USERS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>{stats.total_users}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#dcfce7', borderRadius: '50%' }}>
            <Shield size={22} color="#16a34a" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>EXAMINERS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#16a34a' }}>{stats.total_examiners}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#e0e7ff', borderRadius: '50%' }}>
            <FileText size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>TOTAL EXAMS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>{stats.total_exams}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#fee2e2', borderRadius: '50%' }}>
            <AlertTriangle size={22} color="#dc2626" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>PROCTOR FLAGS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#dc2626' }}>{stats.total_proctor_flags}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
