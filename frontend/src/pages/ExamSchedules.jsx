import React from 'react';
import Breadcrumbs from '../components/layout/Breadcrumbs';

export default function ExamSchedules() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'Exam Schedules' }]} />
      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Exam Schedules</h1>
      <div className="card">
        <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '8px' }}>Upcoming Scheduled Examinations</h3>
        <p style={{ fontSize: '14px', color: '#64748b' }}>Check your upcoming exam timetables and scheduled proctored sessions.</p>
      </div>
    </div>
  );
}
