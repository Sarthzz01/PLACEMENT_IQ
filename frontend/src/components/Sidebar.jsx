import React from 'react';
import {
  LayoutDashboard,
  Users,
  User,
  Target,
  Radar,
  TrendingUp,
  History,
  Database,
  Layers,
  BarChart3,
  GitBranch,
  CircleDot,
  Network,
  ArrowLeftRight,
  FileText,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Cpu
} from 'lucide-react';

export default function Sidebar({
  user,
  currentRole,
  currentTab,
  currentPage,
  setCurrentTab,
  onNavigate,
  onLogout,
  collapsed,
  setCollapsed,
  onToggleCollapse,
}) {
  const isStudent = (user?.role === 'Student') || (currentRole === 'Student');
  const active = currentTab || currentPage || 'dashboard';

  const handleNav = (id) => {
    if (typeof setCurrentTab === 'function') setCurrentTab(id);
    if (typeof onNavigate === 'function') onNavigate(id);
  };

  const toggleCollapse = () => {
    if (typeof setCollapsed === 'function') setCollapsed(!collapsed);
    if (typeof onToggleCollapse === 'function') onToggleCollapse();
  };

  const studentNav = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={19} /> },
    { id: 'profile', label: 'My Profile', icon: <User size={19} /> },
    { id: 'prediction', label: 'Placement Prediction', icon: <Target size={19} /> },
    { id: 'skills', label: 'Skill Analysis', icon: <Radar size={19} /> },
    { id: 'plan', label: 'Improvement Plan', icon: <TrendingUp size={19} /> },
    { id: 'history', label: 'Prediction History', icon: <History size={19} /> },
  ];

  const adminNavAnalytics = [
    { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={19} /> },
    { id: 'students', label: 'Students Roster', icon: <Users size={19} /> },
    { id: 'warehouse', label: 'Data Warehouse', icon: <Database size={19} /> },
    { id: 'olap', label: 'OLAP Analytics', icon: <Layers size={19} /> },
    { id: 'mining', label: 'Data Mining', icon: <BarChart3 size={19} /> },
  ];

  const adminNavML = [
    { id: 'classification', label: 'Classification', icon: <GitBranch size={19} /> },
    { id: 'regression', label: 'Regression', icon: <TrendingUp size={19} /> },
    { id: 'kmeans', label: 'K-Means', icon: <CircleDot size={19} /> },
    { id: 'agglomerative', label: 'Agglomerative', icon: <Network size={19} /> },
    { id: 'cluster_compare', label: 'Cluster Comparison', icon: <ArrowLeftRight size={19} /> },
  ];

  const adminNavExports = [
    { id: 'predictor', label: 'Prediction Center', icon: <Cpu size={19} /> },
    { id: 'reports', label: 'Reports & Exports', icon: <FileText size={19} /> },
    { id: 'settings', label: 'Settings', icon: <Settings size={19} /> },
  ];

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div className="brand-badge">IQ</div>
          {!collapsed && (
            <div className="brand-info">
              <span className="brand-name">PLACEMENT IQ</span>
              <span className="brand-sub">CAMPUS PLATFORM</span>
            </div>
          )}
        </div>
        <button
          className="sidebar-toggle-btn"
          onClick={toggleCollapse}
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        {isStudent ? (
          <div>
            {!collapsed && <div className="nav-section-title">Student Workspace</div>}
            {studentNav.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${active === item.id ? 'active' : ''}`}
                onClick={() => handleNav(item.id)}
                title={collapsed ? item.label : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {!collapsed && <span>{item.label}</span>}
              </div>
            ))}
          </div>
        ) : (
          <div>
            {!collapsed && <div className="nav-section-title">Executive Analytics</div>}
            {adminNavAnalytics.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${active === item.id ? 'active' : ''}`}
                onClick={() => handleNav(item.id)}
                title={collapsed ? item.label : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {!collapsed && <span>{item.label}</span>}
              </div>
            ))}

            {!collapsed && <div className="nav-section-title" style={{ marginTop: '12px' }}>Machine Learning Suite</div>}
            {adminNavML.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${active === item.id ? 'active' : ''}`}
                onClick={() => handleNav(item.id)}
                title={collapsed ? item.label : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {!collapsed && <span>{item.label}</span>}
              </div>
            ))}

            {!collapsed && <div className="nav-section-title" style={{ marginTop: '12px' }}>Predictor & Governance</div>}
            {adminNavExports.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${active === item.id ? 'active' : ''}`}
                onClick={() => handleNav(item.id)}
                title={collapsed ? item.label : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {!collapsed && <span>{item.label}</span>}
              </div>
            ))}
          </div>
        )}
      </nav>

      <div className="sidebar-footer">
        {!collapsed && user && (
          <div className="user-mini-card" style={{ marginBottom: '10px' }}>
            <div className="user-mini-avatar">
              {user.name ? user.name[0].toUpperCase() : 'U'}
            </div>
            <div style={{ overflow: 'hidden' }}>
              <div style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.85rem', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                {user.name}
              </div>
              <div style={{ color: '#94A3B8', fontSize: '0.72rem', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                {user.role}
              </div>
            </div>
          </div>
        )}
        <div
          className="nav-item"
          style={{ color: '#F87171' }}
          onClick={onLogout}
          title="Sign Out"
        >
          <span className="nav-icon"><LogOut size={19} /></span>
          {!collapsed && <span>Sign Out</span>}
        </div>
      </div>
    </aside>
  );
}
