import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import Breadcrumbs from '../components/layout/Breadcrumbs';
import api from '../api/axios';

export default function ProfileSettings() {
  const { user } = useSelector((state) => state.auth);
  const [firstName, setFirstName] = useState(user?.first_name || '');
  const [lastName, setLastName] = useState(user?.last_name || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [msg, setMsg] = useState('');

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await api.put('auth/profile/', { first_name: firstName, last_name: lastName, bio });
      setMsg('Profile updated successfully!');
    } catch (err) {
      setMsg('Failed to update profile.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Breadcrumbs items={[{ label: 'Home', path: '/student/dashboard' }, { label: 'Profile Settings' }]} />
      <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#1e293b' }}>Profile Settings</h1>
      <div className="card" style={{ maxWidth: '600px' }}>
        {msg && <div style={{ padding: '10px', background: '#dcfce7', color: '#16a34a', borderRadius: '8px', marginBottom: '16px' }}>{msg}</div>}
        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569' }}>Username</label>
            <input type="text" value={user?.username || ''} disabled style={{ width: '100%', padding: '10px', marginTop: '4px', borderRadius: '8px', border: '1px solid #e2e8f0', background: '#f8fafc' }} />
          </div>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569' }}>First Name</label>
            <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} style={{ width: '100%', padding: '10px', marginTop: '4px', borderRadius: '8px', border: '1px solid #e2e8f0' }} />
          </div>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569' }}>Last Name</label>
            <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} style={{ width: '100%', padding: '10px', marginTop: '4px', borderRadius: '8px', border: '1px solid #e2e8f0' }} />
          </div>
          <div>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#475569' }}>Bio</label>
            <textarea value={bio} onChange={(e) => setBio(e.target.value)} rows="3" style={{ width: '100%', padding: '10px', marginTop: '4px', borderRadius: '8px', border: '1px solid #e2e8f0' }} />
          </div>
          <button type="submit" className="btn-primary" style={{ width: 'fit-content' }}>Save Changes</button>
        </form>
      </div>
    </div>
  );
}
