import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Award, CheckCircle, XCircle, HelpCircle, Clock, ArrowRight, LayoutDashboard, TrendingUp, Sparkles } from 'lucide-react';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function ExamResult() {
  const { id: examId, attemptId } = useParams();
  const navigate = useNavigate();

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResult();
  }, [attemptId]);

  const fetchResult = async () => {
    try {
      setLoading(true);
      const res = await api.get(`attempts/${attemptId}/result/`);
      setResult(res.data);
    } catch (err) {
      setError('Failed to load exam evaluation result.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>Evaluating results & loading analytics...</div>;
  }

  if (error || !result) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
        <h2 style={{ color: '#dc2626' }}>{error || 'Result not found'}</h2>
        <button className="btn-primary" onClick={() => navigate('/student/dashboard')} style={{ marginTop: '16px' }}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'My Exams', path: '/my-exams' }, { label: 'Result Overview' }]} />

      {/* Main Score Header Card */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '32px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <span style={{ fontSize: '13px', fontWeight: '700', color: '#324ed8', textTransform: 'uppercase' }}>
            Official Exam Score Card
          </span>
          <h1 style={{ fontSize: '26px', fontWeight: '800', color: '#1e293b' }}>{result.exam_title}</h1>
          <p style={{ fontSize: '13px', color: '#64748b' }}>Examinee: {result.student_name}</p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '38px', fontWeight: '800', color: '#324ed8' }}>
              {result.total_score} / {result.max_possible_score}
            </div>
            <div style={{ fontSize: '14px', fontWeight: '700', color: '#64748b' }}>
              Overall Score ({result.percentage}%)
            </div>
          </div>

          <div>
            <span
              className={`badge ${result.is_passed ? 'badge-short_answer' : 'badge-danger'}`}
              style={{ fontSize: '16px', padding: '10px 24px' }}
            >
              {result.is_passed ? 'PASSED ✓' : 'FAILED ✗'}
            </span>
          </div>
        </div>
      </div>

      {/* 4 KPI Stat Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#dcfce7' }}>
            <CheckCircle size={22} color="#16a34a" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>CORRECT</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#16a34a' }}>{result.correct_count}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#fee2e2' }}>
            <XCircle size={22} color="#dc2626" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>INCORRECT</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#dc2626' }}>{result.incorrect_count}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#f1f5f9' }}>
            <HelpCircle size={22} color="#64748b" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>UNANSWERED</span>
            <div style={{ fontSize: '24px', fontWeight: '800', color: '#64748b' }}>{result.unanswered_count}</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '12px', borderRadius: '50%', background: '#e0e7ff' }}>
            <Clock size={22} color="#324ed8" />
          </div>
          <div>
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#64748b' }}>TIME SPENT</span>
            <div style={{ fontSize: '20px', fontWeight: '800', color: '#1e293b' }}>
              {Math.floor(result.time_spent_seconds / 60)}m {result.time_spent_seconds % 60}s
            </div>
          </div>
        </div>
      </div>

      {/* Topic Breakdown Card */}
      {result.topic_breakdown && result.topic_breakdown.length > 0 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Topic Mastery Breakdown</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {result.topic_breakdown.map((tb, idx) => (
              <div key={idx}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: '600', marginBottom: '4px' }}>
                  <span>{tb.topic}</span>
                  <span>{tb.accuracy}%</span>
                </div>
                <div style={{ height: '8px', background: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${tb.accuracy}%`,
                      backgroundColor: tb.accuracy >= 70 ? '#16a34a' : '#324ed8'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Itemized Question Review Section */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Itemized Question & AI Evaluation Review</h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {result.answers && result.answers.map((ans, idx) => (
            <div
              key={ans.id}
              style={{
                border: '1px solid #e2e8f0',
                borderRadius: '12px',
                padding: '20px',
                backgroundColor: ans.is_correct ? '#f8fdf9' : '#fffdfd',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13px', fontWeight: '700', color: '#324ed8' }}>
                  Question {idx + 1} [{ans.question_type}]
                </span>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span style={{ fontSize: '12px', fontWeight: '600', color: '#64748b' }}>
                    Score: {ans.score_obtained} / {ans.marks}
                  </span>
                  <span className={`badge ${ans.is_correct ? 'badge-short_answer' : 'badge-danger'}`}>
                    {ans.is_correct ? 'Correct' : 'Incorrect'}
                  </span>
                </div>
              </div>

              <h4 style={{ fontSize: '15px', fontWeight: '600', color: '#1e293b' }}>{ans.question_text}</h4>

              {/* Your Answer vs Correct Answer */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '13px', marginTop: '4px' }}>
                <div style={{ background: '#ffffff', padding: '10px 14px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <span style={{ color: '#64748b', fontWeight: '600', display: 'block', marginBottom: '4px' }}>Your Answer:</span>
                  <span style={{ fontWeight: '600', color: ans.is_correct ? '#16a34a' : '#dc2626' }}>
                    {ans.selected_option || ans.short_answer_text || '(Unanswered)'}
                  </span>
                </div>

                <div style={{ background: '#ffffff', padding: '10px 14px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <span style={{ color: '#64748b', fontWeight: '600', display: 'block', marginBottom: '4px' }}>Reference Answer:</span>
                  <span style={{ fontWeight: '600', color: '#16a34a' }}>{ans.correct_answer}</span>
                </div>
              </div>

              {/* AI Short Answer Evaluation details if applicable */}
              {ans.question_type === 'SHORT_ANSWER' && ans.ai_explanation && (
                <div style={{ background: '#eef2ff', border: '1px solid #c7d2fe', padding: '12px 16px', borderRadius: '10px', fontSize: '13px', color: '#3730a3' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '700', marginBottom: '4px' }}>
                    <Sparkles size={16} />
                    <span>Evaluation Method: {ans.evaluation_method} (Confidence: {ans.ai_confidence || 85}%)</span>
                  </div>
                  <p>{ans.ai_explanation}</p>
                </div>
              )}

              {/* Explanation */}
              {ans.explanation && (
                <div style={{ fontSize: '12px', color: '#64748b', background: '#f8fafc', padding: '10px', borderRadius: '8px' }}>
                  <strong>Explanation:</strong> {ans.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Footer Navigation Buttons */}
      <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', marginBottom: '24px' }}>
        <button className="btn-outline" onClick={() => navigate('/student/dashboard')}>
          <LayoutDashboard size={18} />
          <span>Return to Dashboard</span>
        </button>

        <button className="btn-primary" onClick={() => navigate('/student/performance')}>
          <TrendingUp size={18} />
          <span>View Performance & Insights</span>
        </button>
      </div>
    </div>
  );
}
