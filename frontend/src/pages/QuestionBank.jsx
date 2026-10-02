import React, { useEffect, useState } from 'react';
import { Plus, FileUp, ChevronLeft, ChevronRight } from 'lucide-react';
import api from '../api/axios';

export default function QuestionBank() {
  const [questions, setQuestions] = useState([]);
  const [summary, setSummary] = useState({
    total_questions: 0,
    mcq_count: 0,
    tf_count: 0,
    short_count: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestionData();
  }, []);

  const fetchQuestionData = async () => {
    try {
      setLoading(true);
      const [qRes, sRes] = await Promise.all([
        api.get('questions/'),
        api.get('questions/summary/')
      ]);
      setQuestions(qRes.data.results || qRes.data);
      setSummary(sRes.data);
    } catch (err) {
      console.error('Failed to load questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeClass = (type) => {
    switch (type) {
      case 'CHOICE':
        return 'badge badge-choice';
      case 'TRUE_FALSE':
        return 'badge badge-true_false';
      case 'SHORT_ANSWER':
        return 'badge badge-short_answer';
      default:
        return 'badge badge-active';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '2.4fr 1fr', gap: '24px', alignItems: 'start' }}>
        {/* Left Question Table Card */}
        <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
          <div style={{ padding: '20px 24px', borderBottom: '1px solid #e2e8f0' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Question Bank</h2>
          </div>

          <div className="table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th style={{ width: '45%' }}>Question</th>
                  <th style={{ width: '20%' }}>Topic</th>
                  <th style={{ width: '15%' }}>Difficulty</th>
                  <th style={{ width: '20%' }}>Type</th>
                </tr>
              </thead>
              <tbody>
                {questions.length > 0 ? (
                  questions.map((q) => (
                    <tr key={q.id}>
                      <td style={{ color: '#1e293b', fontWeight: '500' }}>
                        {q.question_text.length > 55 ? `${q.question_text.substring(0, 55)}...` : q.question_text}
                      </td>
                      <td style={{ color: '#475569', fontSize: '13px' }}>{q.topic_name || 'General'}</td>
                      <td style={{ color: '#64748b', fontSize: '12px', fontWeight: '600' }}>{q.difficulty}</td>
                      <td>
                        <span className={getBadgeClass(q.question_type)}>{q.question_type}</span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
                      No questions available in the question bank.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Table Footer Pagination */}
          <div
            style={{
              padding: '16px 24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              gap: '16px',
              fontSize: '13px',
              color: '#64748b',
              borderTop: '1px solid #e2e8f0'
            }}
          >
            <span>Rows per page: 5</span>
            <span>1-{questions.length} of {summary.total_questions}</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button style={{ border: 'none', background: 'transparent', cursor: 'pointer' }}>
                <ChevronLeft size={18} color="#94a3b8" />
              </button>
              <button style={{ border: 'none', background: 'transparent', cursor: 'pointer' }}>
                <ChevronRight size={18} color="#94a3b8" />
              </button>
            </div>
          </div>
        </div>

        {/* Right Sidebar Card: Question Bank Summary */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Question Bank Summary</h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
              <span>Total Questions</span>
              <span style={{ background: '#324ed8', color: '#ffffff', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {summary.total_questions}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
              <span>Multiple Choice</span>
              <span style={{ background: '#eab308', color: '#ffffff', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {summary.mcq_count}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
              <span>True / False</span>
              <span style={{ background: '#06b6d4', color: '#ffffff', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {summary.tf_count}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
              <span>Short Answer</span>
              <span style={{ background: '#22c55e', color: '#ffffff', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {summary.short_count}
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '10px' }}>
            <button className="btn-primary" style={{ justifyContent: 'center' }}>
              <Plus size={16} />
              <span>+ Create Question</span>
            </button>
            <button
              className="btn-outline"
              style={{
                justifyContent: 'center',
                color: '#16a34a',
                borderColor: '#16a34a'
              }}
            >
              <FileUp size={16} />
              <span>Bulk Import Questions</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
