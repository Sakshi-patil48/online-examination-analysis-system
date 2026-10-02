import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShieldAlert, Clock, HelpCircle, Award, CheckCircle, ArrowRight, AlertTriangle } from 'lucide-react';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function ExamInstructions() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [exam, setExam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchExamDetails();
  }, [id]);

  const fetchExamDetails = async () => {
    try {
      setLoading(true);
      const res = await api.get(`exams/${id}/`);
      setExam(res.data);
    } catch (err) {
      setError('Failed to load exam details.');
    } finally {
      setLoading(false);
    }
  };

  const handleStartExam = async () => {
    try {
      setLoading(true);
      const res = await api.post('attempts/start/', { exam_id: id });
      const attemptId = res.data.id;

      if (res.data.status === 'EVALUATED') {
        navigate(`/exam/${id}/result/${attemptId}`);
      } else {
        navigate(`/exam/${id}/take/${attemptId}`);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start exam attempt.');
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>Loading exam details...</div>;
  }

  if (error || !exam) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
        <h2 style={{ color: '#dc2626' }}>{error || 'Exam not found'}</h2>
        <button className="btn-primary" onClick={() => navigate('/my-exams')} style={{ marginTop: '16px' }}>
          Back to My Exams
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '900px', margin: '0 auto', width: '100%' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'My Exams', path: '/my-exams' }, { label: exam.title }]} />

      <h1 style={{ fontSize: '26px', fontWeight: '800', color: '#1e293b' }}>{exam.title}</h1>

      {/* Main Details Card */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span className="badge badge-active">{exam.subject_name || 'General Subject'}</span>
          <span style={{ fontSize: '13px', fontWeight: '600', color: '#324ed8' }}>Join Code: {exam.join_code}</span>
        </div>

        <p style={{ fontSize: '14px', color: '#475569', lineHeight: '1.6' }}>{exam.description}</p>

        {/* 4 Stats Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', borderTop: '1px solid #e2e8f0', borderBottom: '1px solid #e2e8f0', padding: '16px 0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Clock size={20} color="#324ed8" />
            <div>
              <span style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700' }}>Duration</span>
              <div style={{ fontSize: '15px', fontWeight: '700', color: '#1e293b' }}>{exam.duration_minutes} Mins</div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <HelpCircle size={20} color="#324ed8" />
            <div>
              <span style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700' }}>Total Questions</span>
              <div style={{ fontSize: '15px', fontWeight: '700', color: '#1e293b' }}>{exam.questions_count || 5} Questions</div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Award size={20} color="#324ed8" />
            <div>
              <span style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700' }}>Total Marks</span>
              <div style={{ fontSize: '15px', fontWeight: '700', color: '#1e293b' }}>{exam.total_marks} Marks</div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <CheckCircle size={20} color="#16a34a" />
            <div>
              <span style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: '700' }}>Passing Score</span>
              <div style={{ fontSize: '15px', fontWeight: '700', color: '#16a34a' }}>{exam.pass_percentage}%</div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#1e293b', marginBottom: '8px' }}>Exam Instructions</h3>
          <p style={{ fontSize: '14px', color: '#475569', background: '#f8fafc', padding: '14px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            {exam.instructions}
          </p>
        </div>

        {/* Pre-Exam Warning Box */}
        <div style={{ background: '#fef3c7', border: '1px solid #fde68a', borderRadius: '12px', padding: '16px', display: 'flex', gap: '12px' }}>
          <AlertTriangle size={24} color="#d97706" style={{ flexShrink: 0 }} />
          <div style={{ fontSize: '13px', color: '#92400e', lineHeight: '1.5' }}>
            <strong>Important Rules before starting:</strong>
            <ul style={{ paddingLeft: '18px', marginTop: '6px' }}>
              <li>Once you click <strong>START EXAM</strong>, the timer begins immediately on the server.</li>
              <li>Your answers are saved automatically as you navigate between questions.</li>
              <li>Do not refresh or close your browser tab during the active session.</li>
              {exam.proctoring_enabled && <li>Proctoring security is enabled: Fullscreen exit and tab switches will be logged.</li>}
            </ul>
          </div>
        </div>

        <button className="btn-primary" onClick={handleStartExam} style={{ justifyContent: 'center', padding: '14px', fontSize: '16px' }}>
          <span>START EXAM NOW</span>
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
