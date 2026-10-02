import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Key, ArrowRight, GraduationCap, Clock, Award, AlertTriangle } from 'lucide-react';
import api from '../api/axios';

export default function StudentDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    exams_taken: 0,
    avg_score: 0.0,
    pass_rate: 0.0,
    weak_topics_count: 0,
    topic_mastery: [],
    active_sessions: []
  });
  const [joinCode, setJoinCode] = useState('');
  const [joinError, setJoinError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const res = await api.get('student/analytics/');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load dashboard analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleJoinExam = async (e) => {
    e.preventDefault();
    if (!joinCode.trim()) return;
    setJoinError('');
    try {
      const res = await api.post('exams/join/', { join_code: joinCode });
      navigate(`/exam/${res.data.id}/instructions`);
    } catch (err) {
      setJoinError(err.response?.data?.error || 'Invalid exam code. Please try again.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Banner Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        {/* Welcome Card */}
        <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '420px' }}>
            <h1 style={{ fontSize: '26px', fontWeight: '700', color: '#1e293b' }}>
              Hello Student! 👋
            </h1>
            <p style={{ fontSize: '14px', color: '#64748b', lineHeight: '1.6' }}>
              You have active exams available today. Keep building your knowledge and tracking performance!
            </p>
            <div style={{ display: 'flex', gap: '12px', marginTop: '4px' }}>
              <button className="btn-primary" onClick={() => navigate('/public-exams')}>
                Explore Exams
              </button>
              <button className="btn-outline" onClick={() => navigate('/student/performance')}>
                My Analytics
              </button>
            </div>
          </div>

          <div
            style={{
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              backgroundColor: '#eef2ff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <GraduationCap size={48} color="#324ed8" />
          </div>
        </div>

        {/* Enter Exam Join Code Card (Dark Royal Blue) */}
        <div className="dark-join-card">
          <h3>
            <Key size={18} color="#e0e7ff" />
            Enter Exam Join Code
          </h3>
          <p>Have a private exam code from your instructor? Enter it here to start.</p>

          <form onSubmit={handleJoinExam} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="join-input-group">
              <Key size={16} color="#94a3b8" />
              <input
                type="text"
                placeholder="e.g. EXAM-123"
                value={joinCode}
                onChange={(e) => setJoinCode(e.target.value)}
              />
            </div>
            {joinError && <span style={{ color: '#fca5a5', fontSize: '12px' }}>{joinError}</span>}
            <button type="submit" className="btn-join-white">
              <span>Join Exam</span>
              <ArrowRight size={16} />
            </button>
          </form>
        </div>
      </div>

      {/* Bottom Grid Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '24px' }}>
        {/* Card 1: Overall Exam Performance */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b' }}>Overall Exam Performance</h3>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>Cumulative results & pass record</p>
          </div>

          <div style={{ textAlign: 'center', padding: '20px 0' }}>
            <span style={{ fontSize: '42px', fontWeight: '800', color: '#324ed8' }}>
              {stats.avg_score}%
            </span>
            <p style={{ fontSize: '12px', color: '#64748b', fontWeight: '500' }}>Average Accuracy Rate</p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr 1fr',
              textAlign: 'center',
              borderTop: '1px solid #e2e8f0',
              paddingTop: '16px'
            }}
          >
            <div>
              <span style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>{stats.exams_taken}</span>
              <p style={{ fontSize: '11px', color: '#94a3b8' }}>Exams Taken</p>
            </div>
            <div style={{ borderLeft: '1px solid #e2e8f0', borderRight: '1px solid #e2e8f0' }}>
              <span style={{ fontSize: '18px', fontWeight: '700', color: '#16a34a' }}>{stats.pass_rate}%</span>
              <p style={{ fontSize: '11px', color: '#94a3b8' }}>Pass Rate</p>
            </div>
            <div>
              <span style={{ fontSize: '18px', fontWeight: '700', color: '#dc2626' }}>{stats.weak_topics_count}</span>
              <p style={{ fontSize: '11px', color: '#94a3b8' }}>Weak Topics</p>
            </div>
          </div>
        </div>

        {/* Card 2: Topic Mastery Index */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b' }}>Topic Mastery Index</h3>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>Evaluated accuracy breakdown</p>
          </div>

          {stats.topic_mastery && stats.topic_mastery.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '8px' }}>
              {stats.topic_mastery.map((tm, idx) => (
                <div key={idx}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: '600', marginBottom: '4px' }}>
                    <span>{tm.topic}</span>
                    <span>{tm.accuracy}%</span>
                  </div>
                  <div style={{ height: '8px', background: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                    <div
                      style={{
                        height: '100%',
                        width: `${tm.accuracy}%`,
                        backgroundColor: tm.accuracy >= 70 ? '#16a34a' : '#324ed8'
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '30px 10px', color: '#94a3b8', fontSize: '13px' }}>
              No topic mastery metrics recorded yet. Complete an exam attempt to populate your breakdown.
            </div>
          )}
        </div>

        {/* Card 3: Exam Schedule & Active Sessions */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🗓️</span> Exam Schedule & Active Sessions
            </h3>
            <p style={{ fontSize: '12px', color: '#94a3b8' }}>Available exam sessions</p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {stats.active_sessions && stats.active_sessions.length > 0 ? (
              stats.active_sessions.map((exam) => (
                <div
                  key={exam.id}
                  onClick={() => navigate(`/exam/${exam.id}/instructions`)}
                  style={{
                    border: '1.5px solid #e0e7ff',
                    borderRadius: '12px',
                    padding: '14px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    backgroundColor: '#fafbff'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '13px', fontWeight: '700', color: '#1e293b' }}>
                      {exam.title}
                    </span>
                    <span className="badge badge-active">Active</span>
                  </div>
                  <div style={{ fontSize: '11px', color: '#64748b', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span>⏰</span>
                    <span>Subject: {exam.subject_name || 'General'} | Code: {exam.join_code}</span>
                  </div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', padding: '20px', color: '#94a3b8', fontSize: '13px' }}>
                No active exam sessions scheduled right now.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
