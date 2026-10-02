import React, { useEffect, useState } from 'react';
import { Search, ChevronLeft, ChevronRight, Play, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function MyExams() {
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExamsAndAttempts();
  }, []);

  const fetchExamsAndAttempts = async () => {
    try {
      setLoading(true);
      const [eRes, aRes] = await Promise.all([
        api.get('exams/my_exams/'),
        api.get('attempts/')
      ]);
      setExams(eRes.data);
      setAttempts(aRes.data.results || aRes.data);
    } catch (err) {
      console.error('Failed to fetch exams/attempts:', err);
    } finally {
      setLoading(false);
    }
  };

  const getExamAttempt = (examId) => {
    return attempts.find((a) => a.exam === examId);
  };

  const filteredExams = exams.filter(
    (e) =>
      e.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (e.description && e.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs
        items={[
          { label: 'Home', path: '/student/dashboard' },
          { label: 'My Exams' }
        ]}
      />

      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>My Exams</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '2.4fr 1fr', gap: '24px', alignItems: 'start' }}>
        {/* Left Exams Table Card */}
        <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
          <div style={{ padding: '20px 24px', borderBottom: '1px solid #e2e8f0' }}>
            <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Exams</h2>
          </div>

          <div className="table-container">
            <table className="custom-table">
              <thead>
                <tr>
                  <th style={{ width: '30%' }}>Title</th>
                  <th style={{ width: '40%' }}>Description</th>
                  <th style={{ width: '15%' }}>Status</th>
                  <th style={{ width: '15%' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredExams.length > 0 ? (
                  filteredExams.map((exam) => {
                    const attempt = getExamAttempt(exam.id);
                    let actionText = 'Start Exam';
                    let actionIcon = Play;
                    let actionHandler = () => navigate(`/exam/${exam.id}/instructions`);

                    if (attempt) {
                      if (attempt.status === 'EVALUATED' || attempt.status === 'SUBMITTED') {
                        actionText = 'View Result';
                        actionIcon = Eye;
                        actionHandler = () => navigate(`/exam/${exam.id}/result/${attempt.id}`);
                      } else if (attempt.status === 'IN_PROGRESS') {
                        actionText = 'Continue';
                        actionIcon = Play;
                        actionHandler = () => navigate(`/exam/${exam.id}/take/${attempt.id}`);
                      }
                    }

                    const ActionIcon = actionIcon;

                    return (
                      <tr key={exam.id}>
                        <td style={{ fontWeight: '600', color: '#1e293b' }}>{exam.title}</td>
                        <td style={{ color: '#64748b', fontSize: '13px' }}>
                          {exam.description && exam.description.length > 55
                            ? `${exam.description.substring(0, 55)}...`
                            : exam.description || '-'}
                        </td>
                        <td>
                          {attempt ? (
                            <span className={`badge ${attempt.status === 'EVALUATED' ? 'badge-short_answer' : 'badge-active'}`}>
                              {attempt.status}
                            </span>
                          ) : (
                            <span className="badge badge-active">{exam.status || 'Active'}</span>
                          )}
                        </td>
                        <td>
                          <button
                            className="btn-primary"
                            onClick={actionHandler}
                            style={{ padding: '6px 12px', fontSize: '12px' }}
                          >
                            <ActionIcon size={14} />
                            <span>{actionText}</span>
                          </button>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan="4" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
                      No exams found.
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
            <span>1-{filteredExams.length} of {filteredExams.length}</span>
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

        {/* Right Sidebar Elements */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Top Search Pill */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '9999px',
              padding: '10px 18px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
            }}
          >
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ border: 'none', outline: 'none', width: '100%', fontSize: '14px' }}
            />
            <Search size={18} color="#94a3b8" />
          </div>

          {/* Exam Details Summary Card */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#1e293b' }}>Exam Details</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
                <span>Number of exams</span>
                <span style={{ background: '#e0e7ff', color: '#324ed8', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {exams.length}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
                <span>Conducted</span>
                <span style={{ background: '#e0e7ff', color: '#324ed8', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {attempts.filter(a => a.status === 'EVALUATED').length}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
                <span>Scheduled</span>
                <span style={{ background: '#e0e7ff', color: '#324ed8', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  0
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', color: '#475569' }}>
                <span>Live</span>
                <span style={{ background: '#e0e7ff', color: '#324ed8', fontWeight: '700', borderRadius: '50%', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {exams.filter(e => e.status === 'LIVE').length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
