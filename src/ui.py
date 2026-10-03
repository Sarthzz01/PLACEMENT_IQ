import streamlit as st
from .config import DISPLAY_NAMES

def label(c): 
    return DISPLAY_NAMES.get(c, c.replace('_', ' ').title())

def css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --bg-main: #070d17;
        --bg-surface: rgba(15, 23, 42, 0.72);
        --bg-surface-elevated: rgba(30, 41, 59, 0.75);
        --border-glass: rgba(148, 163, 184, 0.12);
        --border-glow: rgba(99, 102, 241, 0.35);
        --primary: #6366f1;
        --primary-glow: rgba(99, 102, 241, 0.25);
        --secondary: #8b5cf6;
        --accent-cyan: #06b6d4;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
        --accent-amber: #f59e0b;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #111a36 0%, #070d17 50%, #0c081e 100%) !important;
        color: var(--text-primary);
        min-height: 100vh;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #091122 0%, #0f172a 60%, #15102a 100%) !important;
        border-right: 1px solid var(--border-glass) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }

    /* Top Banner / Navbar */
    .app-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 26px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 18px;
        margin-bottom: 24px;
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.38);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 800;
        font-size: 1.35rem;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.01em;
    }

    .nav-role-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .role-student {
        background: rgba(6, 182, 212, 0.16);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 0 16px rgba(6, 182, 212, 0.2);
    }

    .role-admin {
        background: rgba(139, 92, 246, 0.2);
        color: #c084fc;
        border: 1px solid rgba(192, 132, 252, 0.4);
        box-shadow: 0 0 16px rgba(139, 92, 246, 0.28);
    }

    /* Glass Cards */
    .glass-card {
        padding: 24px;
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 20px;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.38);
    }

    .glass-card-interactive {
        cursor: pointer;
    }
    
    .glass-card-interactive:hover {
        transform: translateY(-2px);
        border-color: rgba(129, 140, 248, 0.45);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(99, 102, 241, 0.18);
    }

    /* Hero Section */
    .hero-container {
        position: relative;
        padding: 34px 38px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.42) 0%, rgba(88, 28, 135, 0.38) 50%, rgba(15, 23, 42, 0.7) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(165, 180, 252, 0.25);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        margin-bottom: 26px;
        overflow: hidden;
    }

    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -20%;
        width: 140%;
        height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.14) 0%, transparent 60%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0 0 10px 0;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.02rem;
        line-height: 1.6;
        margin: 0;
        max-width: 860px;
    }

    /* Metric Tiles */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.78) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 16px 20px !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24) !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(99, 102, 241, 0.35) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(124, 58, 237, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    button[kind="secondary"] {
        background: rgba(30, 41, 59, 0.72) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #e2e8f0 !important;
        box-shadow: none !important;
    }

    button[kind="secondary"]:hover {
        background: rgba(51, 65, 85, 0.82) !important;
        border-color: rgba(148, 163, 184, 0.4) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.65);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 10px 20px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.35), rgba(124, 58, 237, 0.35)) !important;
        color: #ffffff !important;
        border: 1px solid rgba(129, 140, 248, 0.3) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }

    /* Badges & Pills */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 6px;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.16);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.16);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .badge-info {
        background: rgba(6, 182, 212, 0.16);
        color: #38bdf8;
        border: 1px solid rgba(6, 182, 212, 0.35);
    }

    .badge-danger {
        background: rgba(244, 63, 94, 0.16);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
    }

    /* Prediction Result Cards */
    .prediction-card {
        padding: 30px;
        border-radius: 22px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin: 18px 0;
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.38);
    }
    
    .prediction-placed {
        background: radial-gradient(circle at 50% 30%, rgba(16, 185, 129, 0.22) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-color: rgba(16, 185, 129, 0.45);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.25);
    }

    .prediction-unplaced {
        background: radial-gradient(circle at 50% 30%, rgba(244, 63, 94, 0.22) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-color: rgba(244, 63, 94, 0.45);
        box-shadow: 0 0 30px rgba(244, 63, 94, 0.25);
    }

    /* Code & monospace */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(30, 41, 59, 0.65) !important;
        color: #38bdf8 !important;
        padding: 2px 6px !important;
        border-radius: 6px !important;
        font-size: 0.88em !important;
    }
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle, tag="Student Placement Analytics & Intelligence Platform"):
    st.markdown(f"""
    <div class="hero-container">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            <span class="badge-pill badge-info">⚡ {tag}</span>
        </div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_top_navbar(role="Student", user_name="Guest User", user_id=""):
    role_class = "role-student" if role == "Student" else "role-admin"
    role_icon = "🎓" if role == "Student" else "🛡️"
    
    html = f"""
    <div class="app-navbar">
        <div class="nav-brand">
            <span>✨ PLACEMENT IQ</span>
            <span style="font-size: 0.78rem; color: #94a3b8; font-weight: 500;">| Analytics & Intelligence Platform</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="text-align: right;">
                <div style="font-weight: 700; font-size: 0.92rem; color: #f8fafc;">{user_name}</div>
                <div style="font-size: 0.78rem; color: #94a3b8;">{user_id if user_id else 'Session Active'}</div>
            </div>
            <span class="nav-role-badge {role_class}">
                {role_icon} {role} Portal
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def completion_gauge(percentage: int, missing_fields: list = None):
    """Render a visual profile completion bar with missing fields alert."""
    color = "#10b981" if percentage >= 85 else ("#38bdf8" if percentage >= 60 else "#f59e0b")
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 18px; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 0.95rem; color: #f8fafc;">Profile Completeness</span>
            <span style="font-weight: 800; font-size: 1.1rem; color: {color};">{percentage}% Complete</span>
        </div>
        <div style="width: 100%; height: 10px; background: rgba(30, 41, 59, 0.8); border-radius: 999px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, #38bdf8, {color}); border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if missing_fields:
        st.caption(f"⚠️ Recommendation: Fill out **{', '.join(missing_fields[:4])}** to reach 100% completeness.")
