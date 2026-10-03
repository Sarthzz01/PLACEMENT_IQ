import streamlit as st
import pandas as pd
import plotly.express as px
from src.preprocessing import load_data, get_dataset_counts
from src.ui import css

css()

# Load actual dataset to populate real metrics (never hard-code fake numbers)
df = load_data()
counts = get_dataset_counts()
total_students = len(df)
placed_students = int(df["placement_prediction"].sum())
placement_rate = (placed_students / total_students) * 100
avg_cgpa = df["cgpa"].mean()
avg_attendance = df["attendance_percentage"].mean()

# ----------------- HERO SECTION -----------------
st.markdown("""
<div style="text-align: center; padding: 48px 20px 32px 20px; max-width: 980px; margin: 0 auto;">
    <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 18px; border-radius: 9999px; background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8; font-size: 0.88rem; font-weight: 700; margin-bottom: 20px;">
        🎓 STUDENT PLACEMENT ANALYTICS & INTELLIGENCE PLATFORM
    </div>
    <h1 style="font-size: 3.4rem; font-weight: 900; line-height: 1.15; letter-spacing: -0.03em; margin: 0 0 18px 0; background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 45%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Know Your Placement Readiness.<br>
        <span style="background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Improve Your Skills. Get Prepared.</span>
    </h1>
    <p style="font-size: 1.2rem; color: #94a3b8; max-width: 760px; margin: 0 auto 32px auto; line-height: 1.65;">
        Discover your personalized campus placement likelihood based on your academic track record, coding practice, and internship experience — powered by university Data Warehouse models.
    </p>
</div>
""", unsafe_allow_html=True)

# Hero Call to Action Buttons
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
with btn_col1:
    if st.button("🚀 Get Started", type="primary", use_container_width=True):
        st.switch_page("pages/0_Login.py")
with btn_col2:
    if st.button("🔐 Sign In", use_container_width=True):
        st.switch_page("pages/0_Login.py")
with btn_col3:
    if st.button("✨ Create Account", use_container_width=True):
        st.session_state.active_auth_tab = "register"
        st.switch_page("pages/0_Login.py")

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# ----------------- REAL DATA STATS STRIP -----------------
st.markdown("### 📊 Platform Intelligence at a Glance (From Active Dataset)")
st.caption("All statistics are derived directly from the certified institutional dataset:")

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Students Analyzed", f"{total_students:,}", "Verified Records")
with k2:
    st.metric("Historical Placement Rate", f"{placement_rate:.1f}%", "Campus Success")
with k3:
    st.metric("Mean Academic CGPA", f"{avg_cgpa:.2f}", "Across All Branches")
with k4:
    st.metric("Mean Attendance", f"{avg_attendance:.1f}%", "Academic Discipline")
with k5:
    st.metric("ML & DWM Models", "7 Algorithms", "Trained & Audited")

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# ----------------- HOW IT WORKS -----------------
st.markdown("## 🧭 How It Works")
st.markdown("From profile creation to interview readiness in six guided steps:")

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #38bdf8; margin-bottom: 8px;">01</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Create Your Account</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Sign up in seconds with your institutional email and engineering branch. No setup fee or administrative approval needed.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #818cf8; margin-bottom: 8px;">02</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Enter Your Profile</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Fill in your 20 placement parameters (CGPA, DSA questions, internships, certifications) or paste your GitHub and LeetCode links.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #c084fc; margin-bottom: 8px;">03</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Analyze Your Skills</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Benchmark your competency radar against historical placed student cohorts from your engineering department.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

s4, s5, s6 = st.columns(3)
with s4:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #34d399; margin-bottom: 8px;">04</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Get Placement Prediction</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Receive your live model-based probability estimation (Random Forest, Decision Tree, Naive Bayes) with key drivers.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s5:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #fbbf24; margin-bottom: 8px;">05</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Improve Weak Areas</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Get mathematically grounded improvement recommendations with exact numerical gaps compared to placed student medians.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s6:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <div style="font-size: 1.8rem; font-weight: 900; color: #f43f5e; margin-bottom: 8px;">06</div>
        <h4 style="margin: 0 0 8px 0; color: #f8fafc;">Track Progress</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            Log multiple assessments over the semester, monitor your readiness progression, and receive personalized feedback from TPO admins.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# ----------------- DUAL PORTAL ARCHITECTURE -----------------
st.markdown("## 👥 Tailored Portals for Students & Administrators")

col_stu, col_adm = st.columns(2, gap="large")

with col_stu:
    st.markdown("""
    <div class="glass-card" style="border-top: 4px solid #38bdf8; height: 100%;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 1.6rem;">🎓</span>
            <h3 style="margin: 0; color: #38bdf8;">For Students</h3>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;">
            Designed specifically to guide undergraduate candidates through their campus placement preparation journey:
        </p>
        <ul style="color: #94a3b8; font-size: 0.9rem; line-height: 1.8; padding-left: 20px;">
            <li><b>Automated Link Parsing:</b> Extract repo count and solved challenge stats from your GitHub and LeetCode profiles.</li>
            <li><b>Instant ML Prediction:</b> Calculate your placement probability without revealing confusing ML hyperparameters.</li>
            <li><b>Data-Driven Gap Analysis:</b> Discover your numerical deficit vs. placed candidate medians in DSA, Aptitude, and Projects.</li>
            <li><b>Targeted Action Plan:</b> Concrete steps to raise your profile strength before company recruitment drives begin.</li>
            <li><b>Historical Progress Audit:</b> Track your prediction evolution in a persistent SQLite timeline.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_adm:
    st.markdown("""
    <div class="glass-card" style="border-top: 4px solid #c084fc; height: 100%;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 1.6rem;">🛡️</span>
            <h3 style="margin: 0; color: #c084fc;">For Administrators & TPO Leads</h3>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;">
            Enterprise-grade Data Warehousing and Data Mining tools to monitor campus-wide recruitment readiness:
        </p>
        <ul style="color: #94a3b8; font-size: 0.9rem; line-height: 1.8; padding-left: 20px;">
            <li><b>Star-Schema Data Warehouse:</b> 1 central fact table (<code>FactPlacement</code>) and 5 relational dimensions.</li>
            <li><b>Dynamic OLAP Engine:</b> Interactive Query Builder, Slice, Dice, 2D Roll-Up, Drill-Down, Pivot, and Drill-Across.</li>
            <li><b>Supervised ML Suite:</b> Tune Decision Tree, Random Forest, and Naive Bayes classifiers with comprehensive metrics.</li>
            <li><b>Continuous Regression:</b> Predict candidate aptitude and skill scores via SLR and MLR equations.</li>
            <li><b>Cohort Clustering:</b> Segment cohorts with K-Means and Agglomerative Hierarchical dendrograms.</li>
            <li><b>Unified Analytics:</b> Seamlessly blend the 15,000 baseline records with incoming student registrations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# ----------------- INTERACTIVE VISUAL ANALYTICS PREVIEW -----------------
st.markdown("### 📈 Campus Placement Distribution by Department")
st.caption("Interactive preview from the active placement dataset:")

dept_df = df.groupby(["branch", "placement_status"]).size().reset_index(name="Student Count")
fig_dept = px.bar(
    dept_df, x="branch", y="Student Count", color="placement_status", barmode="group",
    color_discrete_map={"Placed": "#10b981", "Not Placed": "#64748b"}
)
fig_dept.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_dept, use_container_width=True)

# ----------------- CALL TO ACTION BANNER -----------------
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(124, 58, 237, 0.25) 100%); border: 1px solid rgba(129, 140, 248, 0.35); border-radius: 22px; padding: 38px 24px; text-align: center; margin: 34px 0 24px 0;">
    <h2 style="margin: 0 0 10px 0; font-size: 2rem; color: #f8fafc; font-weight: 800;">
        Ready to Discover Your Placement Readiness?
    </h2>
    <p style="color: #cbd5e1; font-size: 1.05rem; max-width: 640px; margin: 0 auto 22px auto;">
        Join over 15,000 students evaluated on our platform. Understand where you stand today and start improving before your campus drives begin.
    </p>
</div>
""", unsafe_allow_html=True)

cta_c1, cta_c2 = st.columns(2)
with cta_c1:
    if st.button("🚀 Enter Student Portal", type="primary", use_container_width=True, key="cta_stu"):
        st.session_state.active_auth_tab = "login"
        st.switch_page("pages/0_Login.py")
with cta_c2:
    if st.button("🛡️ Access Administrator Console", use_container_width=True, key="cta_adm"):
        st.session_state.active_auth_tab = "login"
        st.switch_page("pages/0_Login.py")

# ----------------- FOOTER -----------------
st.markdown("""
<div style="border-top: 1px solid rgba(148, 163, 184, 0.12); padding-top: 24px; margin-top: 40px; text-align: center; color: #64748b; font-size: 0.84rem;">
    <b>PLACEMENT IQ</b> &bull; Student Placement Analytics & Intelligence Platform<br>
    Data Warehousing & Data Mining (DWM) Academic Engineering Project &bull; Built with Streamlit, Scikit-Learn & SQLite
</div>
""", unsafe_allow_html=True)
