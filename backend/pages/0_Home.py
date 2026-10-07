import streamlit as st
import pandas as pd
import plotly.express as px
from src.preprocessing import load_data, get_dataset_counts
from src.ui import css
from src.visualizations import base

css()

# Load actual dataset to populate real metrics (never hard-code fake numbers)
df = load_data()
counts = get_dataset_counts()
total_students = len(df)
placed_students = int(df["placement_prediction"].sum())
placement_rate = (placed_students / total_students) * 100
avg_cgpa = df["cgpa"].mean()
avg_attendance = df["attendance_percentage"].mean()

# ----------------- TOP LANDING NAVBAR -----------------
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 34px; height: 34px; border-radius: 8px; background: #2563EB; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-weight: 800; font-size: 1.05rem; box-shadow: 0 2px 8px rgba(37,99,235,0.35);">
            IQ
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #0F172A; letter-spacing: -0.02em;">PLACEMENT IQ</div>
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 500;">CAMPUS INTELLIGENCE PLATFORM</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 20px; font-size: 0.88rem; font-weight: 600; color: #475569;">
        <span style="color: #2563EB;">Home</span>
        <span>Features</span>
        <span>How It Works</span>
        <span>About</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- HERO SECTION -----------------
st.markdown("""
<div style="text-align: center; padding: 36px 20px 24px 20px; max-width: 920px; margin: 0 auto;">
    <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 9999px; background: #EFF6FF; border: 1px solid #BFDBFE; color: #2563EB; font-size: 0.82rem; font-weight: 700; margin-bottom: 18px;">
        🎓 STUDENT PLACEMENT ANALYTICS & INTELLIGENCE PLATFORM
    </div>
    <h1 style="font-size: 3rem; font-weight: 900; line-height: 1.18; letter-spacing: -0.03em; margin: 0 0 16px 0; color: #0F172A;">
        Understand Your Placement Readiness.<br>
        <span style="color: #2563EB;">Improve Your Skills. Prepare with Confidence.</span>
    </h1>
    <p style="font-size: 1.12rem; color: #64748B; max-width: 740px; margin: 0 auto 30px auto; line-height: 1.65;">
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
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/0_Login.py")
with btn_col3:
    if st.button("✨ Create Account", use_container_width=True):
        st.session_state.active_auth_tab = "register"
        st.switch_page("pages/0_Login.py")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

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

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# ----------------- HOW IT WORKS -----------------
st.markdown("## 🧭 How It Works")
st.markdown("From profile creation to interview readiness in six guided steps:")

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #2563EB; margin-bottom: 6px;">01</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Create Your Account</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Sign up in seconds with your institutional email and engineering branch. No setup fee or administrative approval needed.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #2563EB; margin-bottom: 6px;">02</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Enter Your Profile</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Fill in your placement parameters (CGPA, DSA questions, internships, certifications) or paste your GitHub and LeetCode links.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #2563EB; margin-bottom: 6px;">03</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Analyze Your Skills</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Benchmark your competency radar against historical placed student cohorts from your engineering department.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

s4, s5, s6 = st.columns(3)
with s4:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #16A34A; margin-bottom: 6px;">04</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Get Placement Prediction</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Receive your live model-based probability estimation (Random Forest, Decision Tree, Naive Bayes) with key drivers.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s5:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #F59E0B; margin-bottom: 6px;">05</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Improve Weak Areas</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Get mathematically grounded improvement recommendations with exact numerical gaps compared to placed student medians.
        </p>
    </div>
    """, unsafe_allow_html=True)

with s6:
    st.markdown("""
    <div class="campus-card" style="height: 100%;">
        <div style="font-size: 1.6rem; font-weight: 900; color: #2563EB; margin-bottom: 6px;">06</div>
        <h4 style="margin: 0 0 6px 0; color: #0F172A;">Track Progress</h4>
        <p style="color: #64748B; font-size: 0.88rem; line-height: 1.6; margin: 0;">
            Log multiple assessments over the semester, monitor your readiness progression, and receive personalized feedback from TPO admins.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# ----------------- DUAL PORTAL ARCHITECTURE -----------------
st.markdown("## 👥 Tailored Portals for Students & Administrators")

col_stu, col_adm = st.columns(2, gap="large")

with col_stu:
    st.markdown("""
    <div class="campus-card" style="border-top: 4px solid #2563EB; height: 100%;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span style="font-size: 1.5rem;">🎓</span>
            <h3 style="margin: 0; color: #2563EB;">For Students</h3>
        </div>
        <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
            Designed specifically to guide undergraduate candidates through their campus placement preparation journey:
        </p>
        <ul style="color: #64748B; font-size: 0.88rem; line-height: 1.7; padding-left: 20px;">
            <li><b>Automated Link Parsing:</b> Extract repo count and solved challenge stats from your GitHub and LeetCode profiles.</li>
            <li><b>Instant ML Prediction:</b> Calculate your placement probability without confusing ML jargon.</li>
            <li><b>Data-Driven Gap Analysis:</b> Discover your numerical deficit vs. placed candidate medians in DSA, Aptitude, and Projects.</li>
            <li><b>Targeted Action Plan:</b> Concrete steps to raise your profile strength before company recruitment drives begin.</li>
            <li><b>Historical Progress Audit:</b> Track your prediction evolution in a persistent SQLite timeline.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_adm:
    st.markdown("""
    <div class="campus-card" style="border-top: 4px solid #0F172A; height: 100%;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span style="font-size: 1.5rem;">🛡️</span>
            <h3 style="margin: 0; color: #0F172A;">For Administrators & TPO Leads</h3>
        </div>
        <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
            Enterprise-grade Data Warehousing and Data Mining tools to monitor campus-wide recruitment readiness:
        </p>
        <ul style="color: #64748B; font-size: 0.88rem; line-height: 1.7; padding-left: 20px;">
            <li><b>Star-Schema Data Warehouse:</b> 1 central fact table (<code>FactPlacement</code>) and 5 relational dimensions.</li>
            <li><b>Dynamic OLAP Engine:</b> Interactive Query Builder, Slice, Dice, 2D Roll-Up, Drill-Down, Pivot, and Drill-Across.</li>
            <li><b>Supervised ML Suite:</b> Tune Decision Tree, Random Forest, and Naive Bayes classifiers with comprehensive metrics.</li>
            <li><b>Continuous Regression:</b> Predict candidate aptitude and skill scores via SLR and MLR equations.</li>
            <li><b>Cohort Clustering:</b> Segment cohorts with K-Means and Agglomerative Hierarchical dendrograms.</li>
            <li><b>Unified Analytics:</b> Seamlessly blend the 15,000 baseline records with incoming student registrations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# ----------------- INTERACTIVE VISUAL ANALYTICS PREVIEW -----------------
st.markdown("### 📈 Campus Placement Distribution by Department")
st.caption("Interactive preview from the active placement dataset:")

dept_df = df.groupby(["branch", "placement_status"]).size().reset_index(name="Student Count")
fig_dept = px.bar(
    dept_df, x="branch", y="Student Count", color="placement_status", barmode="group",
    color_discrete_map={"Placed": "#16A34A", "Not Placed": "#64748B"}
)
fig_dept = base(fig_dept, "Placement Distribution by Engineering Branch")
st.plotly_chart(fig_dept, use_container_width=True)

# ----------------- CALL TO ACTION BANNER -----------------
st.markdown("""
<div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border: 1px solid #BFDBFE; border-radius: 14px; padding: 34px 24px; text-align: center; margin: 30px 0 20px 0;">
    <h2 style="margin: 0 0 8px 0; font-size: 1.85rem; color: #0F172A; font-weight: 800;">
        Ready to Discover Your Placement Readiness?
    </h2>
    <p style="color: #475569; font-size: 1rem; max-width: 620px; margin: 0 auto 20px auto; line-height: 1.6;">
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
<div style="border-top: 1px solid #E2E8F0; padding-top: 20px; margin-top: 36px; text-align: center; color: #64748B; font-size: 0.82rem;">
    <b>PLACEMENT IQ</b> &bull; Student Placement Analytics & Intelligence Platform<br>
    Data Warehousing & Data Mining (DWM) Academic Engineering Project &bull; Built with Streamlit, Scikit-Learn & SQLite
</div>
""", unsafe_allow_html=True)
