import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import AppLayout from './components/layout/AppLayout';
import StudentDashboard from './pages/StudentDashboard';
import PerformanceInsights from './pages/PerformanceInsights';
import MyExams from './pages/MyExams';
import QuestionBank from './pages/QuestionBank';
import PublicExams from './pages/PublicExams';
import ExamSchedules from './pages/ExamSchedules';
import Rules from './pages/Rules';
import ProfileSettings from './pages/ProfileSettings';
import ExaminerDashboard from './pages/ExaminerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import ExamInstructions from './pages/ExamInstructions';
import ExamEngine from './pages/ExamEngine';
import ExamResult from './pages/ExamResult';
import Unauthorized from './pages/Unauthorized';
import { fetchProfile, loginUser } from './store/authSlice';
import './styles/theme.css';

function ProtectedRoute({ children, allowedRoles }) {
  const { user } = useSelector((state) => state.auth);

  if (allowedRoles && allowedRoles.length > 0 && user && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}

export default function App() {
  const dispatch = useDispatch();
  const { accessToken } = useSelector((state) => state.auth);

  useEffect(() => {
    if (accessToken) {
      dispatch(fetchProfile());
    } else {
      // Auto-authenticate as default student session if no token stored
      dispatch(loginUser({ username: 'student@smartexams.com', password: 'student123' }));
    }
  }, [accessToken, dispatch]);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/student/dashboard" replace />} />
          <Route path="unauthorized" element={<Unauthorized />} />

          {/* Student Routes */}
          <Route
            path="student/dashboard"
            element={
              <ProtectedRoute>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="student/performance"
            element={
              <ProtectedRoute>
                <PerformanceInsights />
              </ProtectedRoute>
            }
          />
          <Route path="my-exams" element={<MyExams />} />
          <Route path="question-bank" element={<QuestionBank />} />
          <Route path="public-exams" element={<PublicExams />} />
          <Route path="schedules" element={<ExamSchedules />} />
          <Route path="rules" element={<Rules />} />
          <Route path="profile" element={<ProfileSettings />} />

          {/* Exam Engine Routes */}
          <Route
            path="exam/:id/instructions"
            element={
              <ProtectedRoute>
                <ExamInstructions />
              </ProtectedRoute>
            }
          />
          <Route
            path="exam/:id/take/:attemptId"
            element={
              <ProtectedRoute>
                <ExamEngine />
              </ProtectedRoute>
            }
          />
          <Route
            path="exam/:id/result/:attemptId"
            element={
              <ProtectedRoute>
                <ExamResult />
              </ProtectedRoute>
            }
          />

          {/* Examiner Routes */}
          <Route
            path="examiner/dashboard"
            element={
              <ProtectedRoute allowedRoles={['EXAMINER', 'ADMIN']}>
                <ExaminerDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="examiner/exams"
            element={
              <ProtectedRoute allowedRoles={['EXAMINER', 'ADMIN']}>
                <MyExams />
              </ProtectedRoute>
            }
          />
          <Route
            path="examiner/analytics"
            element={
              <ProtectedRoute allowedRoles={['EXAMINER', 'ADMIN']}>
                <ExaminerDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="examiner/proctoring"
            element={
              <ProtectedRoute allowedRoles={['EXAMINER', 'ADMIN']}>
                <ExaminerDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="examiner/create-exam"
            element={
              <ProtectedRoute allowedRoles={['EXAMINER', 'ADMIN']}>
                <ExaminerDashboard />
              </ProtectedRoute>
            }
          />

          {/* Admin Routes */}
          <Route
            path="admin/dashboard"
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="admin/users"
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="admin/exams"
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="admin/audit-logs"
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
        </Route>

        <Route path="*" element={<Navigate to="/student/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
