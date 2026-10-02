import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, FileCheck2, ShieldAlert, Plus, BarChart3 } from 'lucide-react';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function ExaminerDashboard() {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState({
    total_students: 0,
    total_attempts: 0,
    class_avg_score: 0,
    pass_rate: 0,
    highest_score: 0,
    lowest_score: 0
  });

  useEffect(() => {
    api.get('examiner/analytics/').then(res => setAnalytics(res.data)).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/examiner/dashboard' }, { label: 'Examiner Dashboard' }]} />
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Examiner Portal & Class Analytics</h1>
        <button className="btn-primary" onClick={() => navigate('/examiner/create-exam')}>
          <Plus size={16} />
          <span>+ Create New Exam</span>
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#e0e7ff', borderRadius: '50%' }}>
            <Users size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>TOTAL STUDENTS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>{analytics.total_students}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#e0e7ff', borderRadius: '50%' }}>
            <FileCheck2 size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>TOTAL ATTEMPTS</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#1e293b' }}>{analytics.total_attempts}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#dcfce7', borderRadius: '50%' }}>
            <BarChart3 size={22} color="#16a34a" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>CLASS AVG SCORE</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#16a34a' }}>{analytics.class_avg_score}%</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', background: '#fee2e2', borderRadius: '50%' }}>
            <ShieldAlert size={22} color="#dc2626" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>CLASS PASS RATE</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#dc2626' }}>{analytics.pass_rate}%</div>
          </div>
        </div>
      </div>
    </div>
  );
}
