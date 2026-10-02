import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Clock, ShieldAlert, CheckCircle, Bookmark, ArrowLeft, ArrowRight, Save, Send } from 'lucide-react';
import api from '../api/axios';

export default function ExamEngine() {
  const { id: examId, attemptId } = useParams();
  const navigate = useNavigate();

  const [attemptState, setAttemptState] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // { [question_id]: { selected_option, short_answer_text, is_marked_for_review } }
  const [remainingSeconds, setRemainingSeconds] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState('Saved ✓');
  const [showSubmitModal, setShowSubmitModal] = useState(false);

  const timerRef = useRef(null);

  useEffect(() => {
    fetchAttemptState();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [attemptId]);

  const fetchAttemptState = async () => {
    try {
      setLoading(true);
      const res = await api.get(`attempts/${attemptId}/attempt_state/`);
      const data = res.data;

      if (data.status === 'EVALUATED' || data.status === 'SUBMITTED') {
        navigate(`/exam/${examId}/result/${attemptId}`);
        return;
      }

      setAttemptState(data);
      setQuestions(data.questions || []);
      setUserAnswers(data.saved_answers || {});
      setRemainingSeconds(data.remaining_seconds || 0);

      // Start countdown timer
      startTimer(data.remaining_seconds);
    } catch (err) {
      console.error('Failed to fetch attempt state:', err);
    } finally {
      setLoading(false);
    }
  };

  const startTimer = (seconds) => {
    if (timerRef.current) clearInterval(timerRef.current);
    let sec = seconds;
    timerRef.current = setInterval(() => {
      sec -= 1;
      setRemainingSeconds(sec);
      if (sec <= 0) {
        clearInterval(timerRef.current);
        handleAutoSubmit();
      }
    }, 1000);
  };

  const formatTimer = (sec) => {
    if (sec <= 0) return '00:00:00';
    const hrs = Math.floor(sec / 3600);
    const mins = Math.floor((sec % 3600) / 60);
    const secs = sec % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const currentQuestion = questions[currentIndex] || null;

  const currentAnswer = currentQuestion ? (userAnswers[currentQuestion.id] || {
    selected_option: '',
    short_answer_text: '',
    is_marked_for_review: false
  }) : {};

  const handleOptionChange = (optionId) => {
    const updated = {
      ...currentAnswer,
      selected_option: optionId
    };
    saveAnswerToBackend(currentQuestion.id, updated);
  };

  const handleTextChange = (text) => {
    const updated = {
      ...currentAnswer,
      short_answer_text: text
    };
    saveAnswerToBackend(currentQuestion.id, updated);
  };

  const toggleMarkForReview = () => {
    const updated = {
      ...currentAnswer,
      is_marked_for_review: !currentAnswer.is_marked_for_review
    };
    saveAnswerToBackend(currentQuestion.id, updated);
  };

  const saveAnswerToBackend = async (questionId, ansObj) => {
    setUserAnswers(prev => ({ ...prev, [questionId]: ansObj }));
    setSaveStatus('Saving...');
    setSaving(true);
    try {
      await api.post(`attempts/${attemptId}/save_answer/`, {
        question_id: questionId,
        selected_option: ansObj.selected_option,
        short_answer_text: ansObj.short_answer_text,
        is_marked_for_review: ansObj.is_marked_for_review
      });
      setSaveStatus('Saved ✓');
    } catch (err) {
      setSaveStatus('Save Failed ⚠️');
    } finally {
      setSaving(false);
    }
  };

  const handleAutoSubmit = async () => {
    try {
      await api.post(`attempts/${attemptId}/submit/`, { time_spent_seconds: attemptState?.duration_minutes * 60 });
      navigate(`/exam/${examId}/result/${attemptId}`);
    } catch (err) {
      console.error('Auto submit failed:', err);
    }
  };

  const handleConfirmSubmit = async () => {
    try {
      setLoading(true);
      await api.post(`attempts/${attemptId}/submit/`, {
        time_spent_seconds: (attemptState?.duration_minutes * 60) - remainingSeconds
      });
      navigate(`/exam/${examId}/result/${attemptId}`);
    } catch (err) {
      alert('Failed to submit exam. Please try again.');
      setLoading(false);
    }
  };

  // Helper stats for palette
  const getQuestionStatus = (qId) => {
    const ans = userAnswers[qId];
    if (!ans) return 'UNANSWERED';
    if (ans.is_marked_for_review) return 'MARKED';
    if (ans.selected_option || (ans.short_answer_text && ans.short_answer_text.trim())) return 'ANSWERED';
    return 'UNANSWERED';
  };

  const answeredCount = questions.filter(q => {
    const a = userAnswers[q.id];
    return a && (a.selected_option || (a.short_answer_text && a.short_answer_text.trim()));
  }).length;

  const markedCount = questions.filter(q => userAnswers[q.id]?.is_marked_for_review).length;
  const unansweredCount = questions.length - answeredCount;

  if (loading || !currentQuestion) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>Loading examination engine...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', minHeight: 'calc(100vh - 100px)' }}>
      {/* Top Engine Bar */}
      <div
        style={{
          background: '#2a3b8f',
          color: '#ffffff',
          padding: '16px 24px',
          borderRadius: '16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          boxShadow: '0 4px 18px rgba(0, 0, 0, 0.08)'
        }}
      >
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: '700' }}>{attemptState?.exam_title}</h2>
          <span style={{ fontSize: '12px', color: '#c2cdfb' }}>Attempt ID: #{attemptId}</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <span style={{ fontSize: '12px', color: '#e0e7ff', background: 'rgba(255,255,255,0.15)', padding: '4px 10px', borderRadius: '9999px' }}>
            {saveStatus}
          </span>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#ffffff', color: '#324ed8', padding: '8px 16px', borderRadius: '9999px', fontWeight: '700', fontSize: '16px' }}>
            <Clock size={18} />
            <span>{formatTimer(remainingSeconds)}</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Left Question Box / Right Palette */}
      <div style={{ display: 'grid', gridTemplateColumns: '2.4fr 1fr', gap: '24px', flex: 1 }}>
        {/* Left Question Box */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '28px' }}>
          <div>
            {/* Header info */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0', paddingBottom: '16px', marginBottom: '20px' }}>
              <div>
                <span style={{ fontSize: '13px', fontWeight: '700', color: '#324ed8', textTransform: 'uppercase' }}>
                  Question {currentIndex + 1} of {questions.length}
                </span>
                <span className="badge badge-active" style={{ marginLeft: '12px' }}>{currentQuestion.difficulty}</span>
              </div>
              <span style={{ fontSize: '13px', fontWeight: '600', color: '#64748b' }}>
                {currentQuestion.marks} {currentQuestion.marks === 1 ? 'Mark' : 'Marks'}
              </span>
            </div>

            {/* Question Text */}
            <h3 style={{ fontSize: '17px', fontWeight: '600', color: '#1e293b', lineHeight: '1.6', marginBottom: '24px' }}>
              {currentQuestion.question_text}
            </h3>

            {/* Options Input */}
            {(currentQuestion.question_type === 'CHOICE' || currentQuestion.question_type === 'TRUE_FALSE') && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {currentQuestion.options.map((opt) => {
                  const isSelected = currentAnswer.selected_option === opt.id;
                  return (
                    <div
                      key={opt.id}
                      onClick={() => handleOptionChange(opt.id)}
                      style={{
                        padding: '14px 18px',
                        borderRadius: '12px',
                        border: isSelected ? '2px solid #324ed8' : '1px solid #e2e8f0',
                        backgroundColor: isSelected ? '#eef2ff' : '#ffffff',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        transition: 'all 0.15s ease'
                      }}
                    >
                      <div
                        style={{
                          width: '20px',
                          height: '20px',
                          borderRadius: '50%',
                          border: isSelected ? '6px solid #324ed8' : '2px solid #94a3b8',
                          backgroundColor: '#ffffff'
                        }}
                      />
                      <span style={{ fontSize: '14px', fontWeight: isSelected ? '600' : '400', color: '#1e293b' }}>
                        {opt.text}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}

            {currentQuestion.question_type === 'SHORT_ANSWER' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569' }}>
                  Write your detailed short answer below (evaluated by AI & model criteria):
                </label>
                <textarea
                  rows="6"
                  placeholder="Type your response here..."
                  value={currentAnswer.short_answer_text || ''}
                  onChange={(e) => handleTextChange(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '14px',
                    borderRadius: '12px',
                    border: '1px solid #cbd5e1',
                    fontFamily: 'inherit',
                    fontSize: '14px'
                  }}
                />
              </div>
            )}
          </div>

          {/* Bottom Navigation Buttons */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '24px', borderTop: '1px solid #e2e8f0', marginTop: '24px' }}>
            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                className="btn-outline"
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex(currentIndex - 1)}
                style={{ opacity: currentIndex === 0 ? 0.5 : 1 }}
              >
                <ArrowLeft size={16} />
                <span>Previous</span>
              </button>

              <button
                className="btn-outline"
                disabled={currentIndex === questions.length - 1}
                onClick={() => setCurrentIndex(currentIndex + 1)}
                style={{ opacity: currentIndex === questions.length - 1 ? 0.5 : 1 }}
              >
                <span>Next</span>
                <ArrowRight size={16} />
              </button>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                className="btn-outline"
                onClick={toggleMarkForReview}
                style={{
                  color: currentAnswer.is_marked_for_review ? '#ca8a04' : '#64748b',
                  borderColor: currentAnswer.is_marked_for_review ? '#ca8a04' : '#cbd5e1',
                  backgroundColor: currentAnswer.is_marked_for_review ? '#fef9c3' : 'transparent'
                }}
              >
                <Bookmark size={16} />
                <span>{currentAnswer.is_marked_for_review ? 'Marked ✓' : 'Mark for Review'}</span>
              </button>

              <button className="btn-primary" onClick={() => setShowSubmitModal(true)} style={{ backgroundColor: '#16a34a' }}>
                <Send size={16} />
                <span>Submit Exam</span>
              </button>
            </div>
          </div>
        </div>

        {/* Right Sidebar Question Palette */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b' }}>Question Palette</h3>

          {/* Palette Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '10px' }}>
            {questions.map((q, index) => {
              const status = getQuestionStatus(q.id);
              const isCurrent = index === currentIndex;

              let bg = '#f1f5f9';
              let color = '#475569';
              let border = '1px solid #cbd5e1';

              if (status === 'ANSWERED') {
                bg = '#dcfce7';
                color = '#15803d';
                border = '1px solid #86efac';
              } else if (status === 'MARKED') {
                bg = '#fef9c3';
                color = '#a16207';
                border = '1px solid #fde047';
              }

              if (isCurrent) {
                border = '2.5px solid #324ed8';
              }

              return (
                <button
                  key={q.id}
                  onClick={() => setCurrentIndex(index)}
                  style={{
                    height: '40px',
                    borderRadius: '8px',
                    backgroundColor: bg,
                    color: color,
                    border: border,
                    fontWeight: '700',
                    fontSize: '13px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  {index + 1}
                </button>
              );
            })}
          </div>

          {/* Legend Summary */}
          <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '16px', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#15803d', fontWeight: '600' }}>● Answered:</span>
              <span style={{ fontWeight: '700' }}>{answeredCount}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#a16207', fontWeight: '600' }}>● Marked for Review:</span>
              <span style={{ fontWeight: '700' }}>{markedCount}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#64748b', fontWeight: '600' }}>● Unanswered:</span>
              <span style={{ fontWeight: '700' }}>{unansweredCount}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Submission Confirmation Modal */}
      {showSubmitModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}
        >
          <div className="card" style={{ maxWidth: '440px', width: '100%', padding: '32px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <h3 style={{ fontSize: '20px', fontWeight: '800', color: '#1e293b' }}>Confirm Exam Submission</h3>
            
            <p style={{ fontSize: '14px', color: '#475569', lineHeight: '1.5' }}>
              Are you sure you want to submit your examination now?
            </p>

            <div style={{ background: '#f8fafc', padding: '14px', borderRadius: '10px', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Answered Questions:</span>
                <strong style={{ color: '#16a34a' }}>{answeredCount}</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Unanswered Questions:</span>
                <strong style={{ color: '#dc2626' }}>{unansweredCount}</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Marked for Review:</span>
                <strong style={{ color: '#ca8a04' }}>{markedCount}</strong>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '8px' }}>
              <button className="btn-outline" onClick={() => setShowSubmitModal(false)}>
                Cancel
              </button>
              <button className="btn-primary" onClick={handleConfirmSubmit} style={{ backgroundColor: '#16a34a' }}>
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
