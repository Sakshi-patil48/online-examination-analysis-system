import React from 'react';
import Breadcrumbs from '../components/layout/Breadcrumbs';

export default function Rules() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'Rules & Guidelines' }]} />
      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Examination Rules & Regulations</h1>
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b' }}>Proctoring & Anti-Cheating Policy</h3>
        <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '14px', color: '#475569' }}>
          <li>Exams must be completed in Fullscreen mode. Exiting fullscreen will flag your session.</li>
          <li>Tab switching or window blurring is logged immediately as a proctoring violation.</li>
          <li>Webcam access must be enabled throughout proctored sessions.</li>
          <li>Ensure a stable internet connection and clear lighting before launching your test.</li>
        </ul>
      </div>
    </div>
  );
}
