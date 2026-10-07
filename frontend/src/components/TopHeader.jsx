import React from 'react';
import { Search, Bell } from 'lucide-react';

export default function TopHeader({ title, subtitle }) {

  return (
    <header className="top-header">
      <div>
        <h1 style={{ fontSize: '1.35rem', fontWeight: 800, color: 'var(--navy)' }}>{title}</h1>
        {subtitle && <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}>{subtitle}</p>}
      </div>

      <div className="header-right">
        <div className="search-bar">
          <Search size={16} />
          <input type="text" placeholder="Search analytics, students, metrics..." />
        </div>

        <div style={{ color: 'var(--text-muted)', cursor: 'pointer', padding: '6px' }} title="Notifications">
          <Bell size={20} />
        </div>
      </div>
    </header>
  );
}
