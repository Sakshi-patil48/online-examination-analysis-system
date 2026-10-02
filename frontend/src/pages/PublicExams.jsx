import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function PublicExams() {
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);

  useEffect(() => {
    api.get('exams/public/').then(res => setExams(res.data)).catch(console.error);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'Public Exams' }]} />
      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Public Exams</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
        {exams.map((exam) => (
          <div key={exam.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-active">{exam.subject_name || 'General'}</span>
              <span style={{ fontSize: '12px', color: '#64748b' }}>⏱️ {exam.duration_minutes} mins</span>
            </div>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b' }}>{exam.title}</h3>
            <p style={{ fontSize: '13px', color: '#64748b' }}>{exam.description}</p>
            <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '12px', fontWeight: '600', color: '#324ed8' }}>Code: {exam.join_code}</span>
              <button className="btn-primary" onClick={() => navigate(`/exam/${exam.id}/instructions`)}>
                Take Exam
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
