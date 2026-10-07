import streamlit as st
from .config import DISPLAY_NAMES

def label(c): 
    return DISPLAY_NAMES.get(c, c.replace('_', ' ').title())

def css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-page: #F8FAFC;
        --bg-card: #FFFFFF;
        --bg-sidebar: #0F172A;
        --primary: #2563EB;
        --primary-hover: #1D4ED8;
        --primary-light: #DBEAFE;
        --primary-soft: #EFF6FF;
        --navy: #0F172A;
        --navy-light: #1E293B;
        --border: #E2E8F0;
        --border-hover: #CBD5E1;
        --text-main: #0F172A;
        --text-body: #334155;
        --text-muted: #64748B;
        --success: #16A34A;
        --success-light: #DCFCE7;
        --warning: #F59E0B;
        --warning-light: #FEF3C7;
        --danger: #DC2626;
        --danger-light: #FEE2E2;
        --shadow-card: 0 1px 3px rgba(15, 23, 42, 0.05), 0 4px 12px rgba(15, 23, 42, 0.02);
        --shadow-hover: 0 4px 16px rgba(37, 99, 235, 0.08), 0 1px 3px rgba(15, 23, 42, 0.05);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: var(--text-body);
    }

    /* Streamlit Main App Canvas */
    .stApp {
        background-color: var(--bg-page) !important;
        color: var(--text-main) !important;
        min-height: 100vh;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1440px !important;
    }

    /* Specifically hide ONLY the Streamlit Deploy Button */
    [data-testid="stDeployButton"],
    .stDeployButton,
    .stAppDeployButton,
    [data-testid="stToolbar"] .stDeployButton,
    button:has([data-testid="stDeployButtonIcon"]) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        position: absolute !important;
    }

    /* Ensure Header is transparent and allows sidebar toggle interaction */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 99999 !important;
    }

    /* Ensure Sidebar Minimize and Maximize Arrow Controls are ALWAYS visible at top left */
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stExpandSidebarButton"],
    div:has(> [data-testid="stExpandSidebarButton"]),
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button,
    header [data-testid="collapsedControl"],
    header [data-testid="stSidebarCollapsedControl"],
    button[aria-label*="sidebar" i],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[aria-label="Collapse sidebar"],
    button[aria-label="Expand sidebar"] {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
        z-index: 100000 !important;
    }

    /* Sidebar Header & Collapse Controls */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        padding: 5px 8px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebar"] [data-testid="stSidebarHeader"] button:hover {
        background: rgba(255, 255, 255, 0.14) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }

    /* Expand button when sidebar is collapsed */
    [data-testid="stExpandSidebarButton"],
    [data-testid="collapsedControl"] button,
    header [data-testid="stSidebarCollapsedControl"] button {
        background: #0F172A !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="collapsedControl"] button:hover {
        background: #2563EB !important;
        border-color: #2563EB !important;
    }

    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="collapsedControl"] button svg {
        fill: currentColor !important;
        color: inherit !important;
    }

    /* ----------------- DARK NAVY SIDEBAR ----------------- */
    [data-testid="stSidebar"] {
        background: #0F172A !important;
        border-right: 1px solid #1E293B !important;
        box-shadow: 2px 0 14px rgba(15, 23, 42, 0.1);
        width: 255px !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] .stCaption {
        color: #94A3B8 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #1E293B !important;
        margin: 12px 0 !important;
    }

    /* Sidebar Navigation Links */
    [data-testid="stSidebarNav"] {
        padding-top: 4px;
    }

    /* Group titles in sidebar */
    [data-testid="stSidebarNavSeparator"],
    [data-testid="stSidebarNav"] span:has(+ ul),
    div[data-testid="stSidebarNav"] > div > span {
        color: #64748B !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 14px 14px 4px 14px !important;
        display: block !important;
    }

    /* Sidebar links */
    [data-testid="stSidebarNavLink"],
    [data-testid="stSidebarNav"] a,
    [data-testid="stSidebarNavItems"] a {
        border-radius: 10px !important;
        margin: 3px 8px !important;
        padding: 9px 14px !important;
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all 0.15s ease !important;
        background: transparent !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebarNavLink"]:hover,
    [data-testid="stSidebarNav"] a:hover,
    [data-testid="stSidebarNavItems"] a:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #FFFFFF !important;
    }

    /* Active Sidebar Nav Item -> Blue rounded rectangle #2563EB */
    [data-testid="stSidebarNavLink"][aria-current="page"],
    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNavItems"] a[aria-current="page"],
    [data-testid="stSidebarNavLink"].active,
    [data-testid="stSidebarNav"] a.active {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
    }

    [data-testid="stSidebarNavLink"][aria-current="page"] span,
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #FFFFFF !important;
    }

    /* Clean Material Symbols inside sidebar links */
    [data-testid="stSidebar"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarNav"] span[data-testid="stIconMaterial"] {
        font-size: 1.2rem !important;
        margin-right: 10px !important;
        color: inherit !important;
        vertical-align: middle !important;
    }

    [data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarNav"] a[aria-current="page"] [data-testid="stIconMaterial"] {
        color: #FFFFFF !important;
    }

    /* ----------------- TOP HEADER / NAVBAR ----------------- */
    .app-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 22px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .nav-brand-title {
        font-weight: 800;
        font-size: 1.15rem;
        color: #0F172A;
        letter-spacing: -0.02em;
    }

    .nav-brand-subtitle {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
    }

    .nav-search-box {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 6px 14px;
        width: 280px;
        color: #64748B;
        font-size: 0.85rem;
    }

    .nav-role-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }

    .role-student {
        background: #EFF6FF;
        color: #2563EB;
        border: 1px solid #BFDBFE;
    }

    .role-admin {
        background: #F8FAFC;
        color: #0F172A;
        border: 1px solid #CBD5E1;
    }

    .user-avatar-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #EFF6FF;
        color: #2563EB;
        font-weight: 700;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1.5px solid #DBEAFE;
    }

    /* ----------------- CARDS (WHITE, ROUNDED, SUBTLE BORDER) ----------------- */
    .glass-card,
    .campus-card {
        padding: 22px 24px;
        border-radius: 12px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 12px rgba(15, 23, 42, 0.02);
        transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 20px;
        color: #334155;
    }

    .glass-card:hover,
    .campus-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.07);
    }

    .campus-card-flat {
        padding: 18px 20px;
        border-radius: 10px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }

    /* ----------------- HERO BANNER ----------------- */
    .hero-container {
        position: relative;
        padding: 26px 32px;
        border-radius: 14px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 60%, #EFF6FF 100%);
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 4px 12px rgba(15, 23, 42, 0.02);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 4px 0 8px 0;
        letter-spacing: -0.025em;
        color: #0F172A;
    }

    .hero-subtitle {
        color: #64748B;
        font-size: 0.98rem;
        line-height: 1.6;
        margin: 0;
        max-width: 860px;
    }

    /* ----------------- METRIC KPI TILES ----------------- */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #CBD5E1 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* ----------------- BUTTONS ----------------- */
    .stButton>button {
        border-radius: 8px !important;
        border: 1px solid transparent !important;
        background: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 8px 18px !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05), 0 2px 6px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.15s ease !important;
    }

    .stButton>button:hover {
        background: #1D4ED8 !important;
        box-shadow: 0 3px 10px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    button[kind="secondary"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
    }

    button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #2563EB !important;
        color: #2563EB !important;
    }

    /* ----------------- INPUTS, SELECTS, FORMS ----------------- */
    input[type="text"],
    input[type="password"],
    input[type="number"],
    textarea,
    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        font-size: 0.9rem !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    }

    input:focus,
    textarea:focus,
    div[data-baseweb="select"]:focus-within > div {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ----------------- TABS ----------------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #F1F5F9;
        padding: 4px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.15s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #2563EB !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
    }

    /* ----------------- EXPANDERS ----------------- */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
    }

    details[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
        margin-bottom: 14px;
    }

    /* ----------------- BADGES & PILLS ----------------- */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 700;
        margin-right: 6px;
    }
    
    .badge-success {
        background: #F0FDF4;
        color: #16A34A;
        border: 1px solid #BBF7D0;
    }

    .badge-warning {
        background: #FFFBEB;
        color: #D97706;
        border: 1px solid #FDE68A;
    }

    .badge-info {
        background: #EFF6FF;
        color: #2563EB;
        border: 1px solid #BFDBFE;
    }

    .badge-danger {
        background: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
    }

    /* ----------------- PREDICTION RESULT CARDS ----------------- */
    .prediction-card {
        padding: 28px 24px;
        border-radius: 14px;
        text-align: center;
        margin: 18px 0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }
    
    .prediction-placed {
        background: #F0FDF4;
        border: 1.5px solid #86EFAC;
    }

    .prediction-unplaced {
        background: #FEF2F2;
        border: 1.5px solid #FECACA;
    }

    /* ----------------- CODE & MONOSPACE ----------------- */
    code {
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
        background: #F1F5F9 !important;
        color: #0F172A !important;
        padding: 2px 6px !important;
        border-radius: 5px !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 0.85em !important;
    }

    /* ----------------- DATAFRAMES & TABLES ----------------- */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background: #FFFFFF !important;
    }

    /* Headings hierarchy */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.015em;
    }
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle, tag="Student Placement Analytics & Intelligence Platform"):
    """Render a clean Campus Blue hero / title banner."""
    st.markdown(f"""
    <div class="hero-container">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span class="badge-pill badge-info">🎓 {tag}</span>
        </div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_top_navbar(role="Student", user_name="Guest User", user_id=""):
    """Render modern Campus Blue top header bar matching the reference style."""
    role_class = "role-student" if role == "Student" else "role-admin"
    role_label = "Student" if role == "Student" else "Administrator"
    
    # Calculate user initials
    parts = user_name.strip().split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")) if parts else "U"
    initials = initials.upper()

    html = f"""
    <div class="app-navbar">
        <div class="nav-brand">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #2563EB; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-weight: 800; font-size: 1rem; box-shadow: 0 2px 6px rgba(37,99,235,0.3);">
                IQ
            </div>
            <div>
                <div class="nav-brand-title">PLACEMENT IQ</div>
                <div class="nav-brand-subtitle">Campus Placement Intelligence</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
            <div class="nav-search-box" style="display: none;">
                <span>🔍</span>
                <span>Search students, metrics...</span>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 700; font-size: 0.9rem; color: #0F172A;">{user_name}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{user_id if user_id else role_label}</div>
            </div>
            <div class="user-avatar-circle">
                {initials}
            </div>
            <span class="nav-role-badge {role_class}">
                {role_label}
            </span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def completion_gauge(percentage: int, missing_fields: list = None):
    """Render a visual profile completion bar with missing fields alert in Campus Blue style."""
    color = "#16A34A" if percentage >= 85 else ("#2563EB" if percentage >= 60 else "#F59E0B")
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 22px; margin-bottom: 18px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 0.92rem; color: #0F172A;">Profile Completeness</span>
            <span style="font-weight: 800; font-size: 1rem; color: {color};">{percentage}% Complete</span>
        </div>
        <div style="width: 100%; height: 8px; background: #F1F5F9; border-radius: 999px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; background: {color}; border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if missing_fields:
        st.caption(f"💡 Recommendation: Fill out **{', '.join(missing_fields[:4])}** to reach 100% completeness.")

def render_academic_justification(
    title: str,
    algorithm_name: str,
    why_used: list,
    institutional_impact: str,
    dwm_concept: str = None
):
    """
    Render a clean Campus Blue academic and institutional justification card
    at the end of administrative data mining, warehouse, and machine learning tasks.
    Uses st.html / unindented HTML to prevent Markdown parser code block misinterpretation.
    """
    items_html = "".join([
        f'<div style="margin-bottom: 10px; display: flex; align-items: flex-start; gap: 8px;">'
        f'<div style="color: #2563EB; font-weight: 800; font-size: 1rem; line-height: 1.4;">•</div>'
        f'<div><span style="color: #0F172A; font-weight: 700; font-size: 0.9rem;">{h}: </span>'
        f'<span style="color: #334155; font-size: 0.88rem; line-height: 1.6;">{desc}</span></div>'
        f'</div>'
        for h, desc in why_used
    ])
    
    concept_html = (
        f'<div style="margin-top: 14px; padding-top: 12px; border-top: 1px dashed #E2E8F0; font-size: 0.82rem; color: #64748B;">'
        f'<strong style="color: #0F172A;">DWM Curricular Concept:</strong> {dwm_concept}'
        f'</div>'
    ) if dwm_concept else ""

    html = (
        f'<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px 26px; margin-top: 28px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);">'
        f'<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 12px;">'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<span style="background: #EFF6FF; color: #2563EB; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; border: 1px solid #BFDBFE;">PROJECT JUSTIFICATION</span>'
        f'<span style="font-size: 1.1rem; font-weight: 800; color: #0F172A;">{title}</span>'
        f'</div>'
        f'<span style="font-size: 0.82rem; color: #64748B; font-weight: 600;">{algorithm_name}</span>'
        f'</div>'
        f'<div style="margin-bottom: 16px;">'
        f'<div style="font-size: 0.86rem; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 12px;">Why We Use This in Placement IQ:</div>'
        f'{items_html}'
        f'</div>'
        f'<div style="background: #F8FAFC; border-left: 3px solid #2563EB; border-radius: 0 8px 8px 0; padding: 12px 18px; margin-bottom: 6px;">'
        f'<div style="font-size: 0.8rem; font-weight: 700; color: #0F172A; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px;">🏛️ Institutional Impact & Administrative Value:</div>'
        f'<div style="font-size: 0.86rem; color: #475569; line-height: 1.6;">{institutional_impact}</div>'
        f'</div>'
        f'{concept_html}'
        f'</div>'
    )
    
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)
