import React, { useEffect, useState } from 'react';
import { GraduationCap, TrendingUp, CheckCircle, AlertTriangle } from 'lucide-react';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function PerformanceInsights() {
  const [data, setData] = useState({
    exams_taken: 0,
    avg_score: 0.0,
    pass_rate: 0.0,
    weak_topics_count: 0,
    weak_topics: [],
    strong_topics: [],
    study_plan: []
  });

  useEffect(() => {
    fetchPerformanceData();
  }, []);

  const fetchPerformanceData = async () => {
    try {
      const res = await api.get('student/analytics/');
      setData(res.data);
    } catch (err) {
      console.error('Failed to load performance insights:', err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs
        items={[
          { label: 'Home', path: '/student/dashboard' },
          { label: 'Student', path: '/student/dashboard' },
          { label: 'Performance' }
        ]}
      />

      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Performance</h1>

      {/* AI Intelligence Header Card */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ padding: '12px', borderRadius: '12px', background: '#eef2ff' }}>
          <GraduationCap size={28} color="#324ed8" />
        </div>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#1e293b' }}>
            AI Performance Intelligence & Insights
          </h2>
          <p style={{ fontSize: '13px', color: '#64748b' }}>
            Track your overall learning trajectory, identify weak topics, and follow AI study recommendations.
          </p>
        </div>
      </div>

      {/* 4 KPI Stat Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        {/* Card 1 */}
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#e0e7ff' }}>
            <GraduationCap size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>
              EXAMS COMPLETED
            </span>
            <div style={{ fontSize: '26px', fontWeight: '800', color: '#1e293b' }}>
              {data.exams_taken}
            </div>
          </div>
        </div>

        {/* Card 2 */}
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#e0e7ff' }}>
            <TrendingUp size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>
              AVERAGE SCORE
            </span>
            <div style={{ fontSize: '26px', fontWeight: '800', color: '#324ed8' }}>
              {data.avg_score}%
            </div>
          </div>
        </div>

        {/* Card 3 */}
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#dcfce7' }}>
            <CheckCircle size={22} color="#16a34a" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>
              PASS RATE
            </span>
            <div style={{ fontSize: '26px', fontWeight: '800', color: '#16a34a' }}>
              {data.pass_rate}%
            </div>
          </div>
        </div>

        {/* Card 4 */}
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#fee2e2' }}>
            <AlertTriangle size={22} color="#dc2626" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b', textTransform: 'uppercase' }}>
              WEAK TOPICS
            </span>
            <div style={{ fontSize: '26px', fontWeight: '800', color: '#dc2626' }}>
              {data.weak_topics_count}
            </div>
          </div>
        </div>
      </div>

      {/* Two Columns: Strong Mastery vs Focus Areas */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Strong Topics */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>💪</span> Strong Mastery Topics
          </h3>
          {data.strong_topics && data.strong_topics.length > 0 ? (
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {data.strong_topics.map((t, idx) => (
                <span key={idx} className="badge badge-short_answer">{t}</span>
              ))}
            </div>
          ) : (
            <p style={{ fontSize: '13px', color: '#94a3b8' }}>
              Complete more exams to unlock strong topic badges.
            </p>
          )}
        </div>

        {/* Focus Areas & Weak Topics */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>⚠️</span> Focus Areas & Weak Topics
          </h3>
          {data.weak_topics && data.weak_topics.length > 0 ? (
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {data.weak_topics.map((wt, idx) => (
                <span key={idx} className="badge badge-danger">{wt}</span>
              ))}
            </div>
          ) : (
            <div>
              <span className="badge badge-short_answer" style={{ padding: '8px 16px', fontSize: '13px' }}>
                No Critical Weak Topics Found!
              </span>
            </div>
          )}
        </div>
      </div>

      {/* AI-Generated Study Action Plan */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🤖</span> AI-Generated Study Action Plan
        </h3>
        {data.study_plan && data.study_plan.length > 0 ? (
          <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '14px', color: '#475569' }}>
            {data.study_plan.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>
            Complete your first assessment to generate an AI study plan.
          </p>
        )}
      </div>
    </div>
  );
}
