import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const navigate = useNavigate();

  const handleCreateExamClick = () => {
    navigate('/examiner/create-exam');
  };

  return (
    <div className="app-container">
      {sidebarOpen && <Sidebar onCreateExamClick={handleCreateExamClick} />}
      <div className="main-content">
        <Topbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        <main className="page-body">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
