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
import Login from './pages/Login';
import Register from './pages/Register';
import { fetchProfile } from './store/authSlice';
import './styles/theme.css';

function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

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
    }
  }, [accessToken, dispatch]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route path="unauthorized" element={<Unauthorized />} />

          {/* Student Routes */}
          <Route
            path="student/dashboard"
            element={
              <ProtectedRoute allowedRoles={['STUDENT']}>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="student/performance"
            element={
              <ProtectedRoute allowedRoles={['STUDENT']}>
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
              <ProtectedRoute allowedRoles={['STUDENT', 'EXAMINER', 'ADMIN']}>
                <ExamInstructions />
              </ProtectedRoute>
            }
          />
          <Route
            path="exam/:id/take/:attemptId"
            element={
              <ProtectedRoute allowedRoles={['STUDENT', 'EXAMINER', 'ADMIN']}>
                <ExamEngine />
              </ProtectedRoute>
            }
          />
          <Route
            path="exam/:id/result/:attemptId"
            element={
              <ProtectedRoute allowedRoles={['STUDENT', 'EXAMINER', 'ADMIN']}>
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

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
