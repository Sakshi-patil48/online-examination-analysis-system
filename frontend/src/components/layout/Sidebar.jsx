import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  GraduationCap,
  Plus,
  LayoutDashboard,
  TrendingUp,
  FileCheck2,
  BookOpen,
  Share2,
  Calendar,
  FileText,
  User,
  LogOut,
  Users,
  ShieldAlert,
  BarChart3
} from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/authSlice';

export default function Sidebar({ onCreateExamClick }) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const role = user?.role || 'STUDENT';

  let navItems = [];

  if (role === 'EXAMINER') {
    navItems = [
      { name: 'Dashboard', path: '/examiner/dashboard', icon: LayoutDashboard },
      { name: 'My Exams', path: '/examiner/exams', icon: FileCheck2 },
      { name: 'Question Bank', path: '/question-bank', icon: BookOpen },
      { name: 'Exam Schedules', path: '/schedules', icon: Calendar },
      { name: 'Student Analytics', path: '/examiner/analytics', icon: BarChart3 },
      { name: 'Proctoring Audit', path: '/examiner/proctoring', icon: ShieldAlert },
    ];
  } else if (role === 'ADMIN') {
    navItems = [
      { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
      { name: 'User Management', path: '/admin/users', icon: Users },
      { name: 'Exam Overview', path: '/admin/exams', icon: FileCheck2 },
      { name: 'Audit Logs', path: '/admin/audit-logs', icon: FileText },
    ];
  } else {
    // STUDENT
    navItems = [
      { name: 'Analytics Dashboard', path: '/student/dashboard', icon: LayoutDashboard },
      { name: 'Performance & Insights', path: '/student/performance', icon: TrendingUp },
      { name: 'My Exams', path: '/my-exams', icon: FileCheck2 },
      { name: 'Question Bank', path: '/question-bank', icon: BookOpen },
      { name: 'Public Exams', path: '/public-exams', icon: Share2 },
      { name: 'Exam Schedules', path: '/schedules', icon: Calendar },
      { name: 'Rules', path: '/rules', icon: FileText },
    ];
  }

  return (
    <aside className="sidebar">
      {/* Logo Brand Header */}
      <div className="sidebar-brand">
        <div className="sidebar-logo-icon">
          <GraduationCap size={22} color="#2a3b8f" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline' }}>
          <span className="sidebar-title">SmartExams</span>
          <span className="sidebar-version">v1.0</span>
        </div>
      </div>

      {/* Create Exam Button for Examiners/Admins */}
      {role !== 'STUDENT' && (
        <button className="sidebar-create-btn" onClick={onCreateExamClick}>
          <Plus size={18} />
          <span>Create Exam</span>
        </button>
      )}

      {/* Navigation Section */}
      <div className="sidebar-section-title">NAVIGATION</div>
      <ul className="sidebar-menu">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `sidebar-item ${isActive ? 'active' : ''}`
                }
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </NavLink>
            </li>
          );
        })}
      </ul>

      {/* Profile Settings Section */}
      <div className="sidebar-section-title" style={{ marginTop: '32px' }}>
        PROFILE SETTINGS
      </div>
      <ul className="sidebar-menu">
        <li>
          <NavLink
            to="/profile"
            className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}
          >
            <User size={18} />
            <span>Profile Settings</span>
          </NavLink>
        </li>
        <li>
          <div
            className="sidebar-item"
            onClick={() => dispatch(logout())}
            style={{ cursor: 'pointer' }}
          >
            <LogOut size={18} />
            <span>Logout</span>
          </div>
        </li>
      </ul>
    </aside>
  );
}
