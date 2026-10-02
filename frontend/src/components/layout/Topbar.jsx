import React from 'react';
import { Search, Bell, Menu, User as UserIcon } from 'lucide-react';
import { useSelector } from 'react-redux';

export default function Topbar({ onToggleSidebar }) {
  const { user } = useSelector((state) => state.auth);

  const displayName = user
    ? user.full_name || (user.first_name ? `${user.first_name} ${user.last_name}`.strip() : user.username)
    : 'User';

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button className="topbar-toggle" onClick={onToggleSidebar} title="Toggle Sidebar">
          <Menu size={18} />
        </button>

        <div className="search-bar">
          <Search size={18} color="#94a3b8" />
          <input
            type="text"
            placeholder="Search exams, subjects, or topics..."
          />
        </div>
      </div>

      <div className="topbar-right">
        <div className="notification-bell" title="Notifications">
          <Bell size={18} />
          <span className="notification-badge">4</span>
        </div>

        <div className="user-profile">
          <div className="user-avatar">
            {user?.profile_picture ? (
              <img
                src={user.profile_picture}
                alt="Avatar"
                style={{ width: '100%', height: '100%', borderRadius: '50%' }}
              />
            ) : (
              <UserIcon size={20} color="#64748b" />
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span className="user-name">{displayName}</span>
            <span style={{ fontSize: '10px', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>
              {user?.role || 'STUDENT'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
