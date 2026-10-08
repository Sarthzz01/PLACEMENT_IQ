import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import TopHeader from './components/TopHeader';

// Public Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';

// Student Pages
import StudentDashboard from './pages/student/StudentDashboard';
import StudentProfile from './pages/student/StudentProfile';
import PlacementPrediction from './pages/student/PlacementPrediction';
import SkillAnalysis from './pages/student/SkillAnalysis';
import ImprovementPlan from './pages/student/ImprovementPlan';
import PredictionHistory from './pages/student/PredictionHistory';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import StudentData from './pages/admin/StudentData';
import DataWarehouse from './pages/admin/DataWarehouse';
import OLAPAnalytics from './pages/admin/OLAPAnalytics';
import DataMining from './pages/admin/DataMining';
import ClassificationPage from './pages/admin/ClassificationPage';
import RegressionPage from './pages/admin/RegressionPage';
import KMeansPage from './pages/admin/KMeansPage';
import AgglomerativePage from './pages/admin/AgglomerativePage';
import ClusterComparisonPage from './pages/admin/ClusterComparisonPage';
import PredictionCenter from './pages/admin/PredictionCenter';
import ReportsPage from './pages/admin/ReportsPage';
import SettingsPage from './pages/admin/SettingsPage';

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('placementiq_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [currentPage, setCurrentPage] = useState(() => {
    try {
      const savedUser = localStorage.getItem('placementiq_user');
      if (savedUser) {
        return 'dashboard';
      }
    } catch {}
    return 'home';
  });

  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    if (user) {
      localStorage.setItem('placementiq_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('placementiq_user');
    }
  }, [user]);

  const handleLogin = (loggedUser) => {
    setUser(loggedUser);
    setCurrentPage('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentPage('home');
  };

  // If viewing public landing page or login page
  if (!user && (currentPage === 'home' || currentPage === 'login')) {
    if (currentPage === 'login') {
      return (
        <LoginPage
          onLogin={handleLogin}
          onLoginSuccess={handleLogin}
          onBackHome={() => setCurrentPage('home')}
          onNavigate={setCurrentPage}
        />
      );
    }
    return (
      <HomePage
        onGoToLogin={(tab) => setCurrentPage('login')}
        onNavigate={setCurrentPage}
      />
    );
  }

  // If user navigated to home while logged in
  if (currentPage === 'home') {
    return (
      <HomePage
        onGoToLogin={() => setCurrentPage('dashboard')}
        onNavigate={setCurrentPage}
        user={user}
        onLogout={handleLogout}
      />
    );
  }

  // Fallback role
  const effectiveRole = user?.role || 'Student';

  // Helper to normalize tab IDs
  const activeTab = currentPage.replace(/^(student-|admin-)/, '');

  const getHeaderInfo = (tab, role) => {
    const titles = {
      dashboard: role === 'Admin' ? 'Executive Placement Dashboard' : 'Student Placement Dashboard',
      profile: 'Candidate Profile & Credentials',
      prediction: role === 'Admin' ? 'Placement Inference Center' : 'Placement Readiness Assessment',
      predict: role === 'Admin' ? 'Placement Inference Center' : 'Placement Readiness Assessment',
      skills: 'Cohort Skill Gap Benchmarks',
      plan: 'Actionable Career Roadmap',
      history: 'Prediction Audit Trail',
      students: 'Registered Student Roster',
      warehouse: 'Star Schema Data Warehouse',
      olap: 'Multi-Dimensional OLAP Analytics',
      mining: 'Data Mining & Pattern Discovery',
      classification: 'Supervised Classification Suite',
      regression: 'Continuous Skill Regression',
      kmeans: 'K-Means Partitioning Clustering',
      agglomerative: 'Hierarchical Agglomerative Clustering',
      cluster_compare: 'Cluster Algorithm Benchmark',
      comparison: 'Cluster Algorithm Benchmark',
      predictor: 'Prediction Inference Center',
      reports: 'Intelligence Export & Reports',
      settings: 'System Governance & Settings'
    };
    return {
      title: titles[tab] || (role === 'Admin' ? 'Executive Intelligence Suite' : 'Student Workspace'),
      subtitle: role === 'Admin'
        ? 'Data Warehousing & Machine Learning University Platform'
        : 'Campus Placement Readiness & Career Analytics'
    };
  };

  const renderActivePage = () => {
    if (effectiveRole === 'Student') {
      switch (activeTab) {
        case 'dashboard':
          return <StudentDashboard user={user} onNavigate={setCurrentPage} />;
        case 'profile':
          return <StudentProfile user={user} />;
        case 'prediction':
        case 'predict':
          return <PlacementPrediction user={user} onNavigate={setCurrentPage} />;
        case 'skills':
          return <SkillAnalysis user={user} />;
        case 'plan':
          return <ImprovementPlan user={user} />;
        case 'history':
          return <PredictionHistory user={user} />;
        default:
          return <StudentDashboard user={user} onNavigate={setCurrentPage} />;
      }
    } else {
      switch (activeTab) {
        case 'dashboard':
          return <AdminDashboard user={user} onNavigate={setCurrentPage} />;
        case 'students':
          return <StudentData user={user} />;
        case 'warehouse':
          return <DataWarehouse />;
        case 'olap':
          return <OLAPAnalytics />;
        case 'mining':
          return <DataMining />;
        case 'classification':
          return <ClassificationPage />;
        case 'regression':
          return <RegressionPage />;
        case 'kmeans':
          return <KMeansPage />;
        case 'agglomerative':
          return <AgglomerativePage />;
        case 'cluster_compare':
        case 'comparison':
          return <ClusterComparisonPage />;
        case 'predictor':
        case 'predict':
          return <PredictionCenter user={user} />;
        case 'reports':
          return <ReportsPage />;
        case 'settings':
          return <SettingsPage />;
        default:
          return <AdminDashboard user={user} onNavigate={setCurrentPage} />;
      }
    }
  };

  const headerInfo = getHeaderInfo(activeTab, effectiveRole);

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-main)' }}>
      {/* Sidebar */}
      <Sidebar
        user={user}
        currentRole={effectiveRole}
        currentTab={activeTab}
        currentPage={activeTab}
        setCurrentTab={setCurrentPage}
        onNavigate={setCurrentPage}
        onLogout={handleLogout}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content Area */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          minWidth: 0,
          transition: 'margin-left 0.2s ease',
        }}
      >
        <TopHeader
          user={user}
          title={headerInfo.title}
          subtitle={headerInfo.subtitle}
          onLogout={handleLogout}
          onNavigate={setCurrentPage}
        />

        <main style={{ flex: 1, padding: '32px', overflowY: 'auto' }}>
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
}
