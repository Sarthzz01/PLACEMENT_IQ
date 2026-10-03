import streamlit as st
import pandas as pd
from src.auth import require_student
from src.preprocessing import load_data
from src.database import get_student_profile, is_student_profile_completed
from src.recommendations import generate_recommendations
from src.ui import css, hero, render_top_navbar

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Targeted Placement Improvement Plan",
    "Personalized, data-driven roadmap to bridge performance gaps identified between your candidate profile and placed cohort benchmarks.",
    tag="Actionable Readiness"
)

# Check if student profile is completed
if not is_student_profile_completed(email):
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 44px 30px; margin: 24px 0; border: 1.5px dashed rgba(52, 211, 153, 0.45); border-radius: 20px;">
        <div style="font-size: 3.5rem; margin-bottom: 14px;">🎯</div>
        <h2 style="color: #f8fafc; font-size: 1.6rem; font-weight: 800; margin-bottom: 10px;">
            Improvement Roadmap Locked
        </h2>
        <p style="color: #94a3b8; font-size: 1.02rem; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.6;">
            A targeted preparation roadmap computes the exact statistical gaps between your recorded profile metrics and placed alumni medians. Please complete your profile to unlock your personalized plan.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📝 Complete My Profile to Unlock Roadmap", type="primary", use_container_width=True):
            st.switch_page("pages/2_Student_Profile.py")
    st.stop()

profile = get_student_profile(email) or {}
df = load_data()
rec_data = generate_recommendations(profile, df)

# Readiness Tier Banner
readiness = rec_data["readiness_level"]
tier_color = "#34d399" if "High" in readiness else ("#fbbf24" if "Moderate" in readiness else "#fb7185")

st.markdown(f"""
<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.09); border-radius: 18px; padding: 24px 28px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-size: 1.15rem; font-weight: 800; color: #f8fafc;">Candidate Readiness Assessment</span>
        <span style="padding: 6px 16px; border-radius: 9999px; font-weight: 800; font-size: 0.9rem; background: rgba(255,255,255,0.08); color: {tier_color}; border: 1px solid {tier_color};">
            ⚡ {readiness}
        </span>
    </div>
    <p style="color: #94a3b8; font-size: 0.92rem; margin: 0; line-height: 1.6;">
        Evaluated against 15,000 university records. The actionable items below highlight the exact numerical gaps between your recorded competencies and the median values of successful campus placements.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------- SECTION 1: TOP ACTIONABLE GAPS -----------------
st.markdown("### 🎯 Priority Weak Areas & Gap Analysis")
st.caption("Derived directly from dataset statistical medians and percentiles:")

gaps = rec_data["all_improvements"]

if gaps:
    for idx, g in enumerate(gaps, 1):
        p_badge = "badge-danger" if g["priority"] in ["Critical", "High"] else "badge-warning"
        gap_text = f"+{g['gap']} {g['unit']}" if g['gap'] > 0 else f"{g['gap']} {g['unit']}"
        percentile_txt = f" &bull; Campus Standing: <b>{g['percentile']}th percentile</b>" if "percentile" in g else ""
        
        card_html = (
            f'<div class="glass-card" style="margin-bottom: 18px; padding: 22px; border-radius: 16px;">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">'
            f'<div>'
            f'<span style="font-size: 0.8rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">'
            f'Action Item {idx} &bull; {g["category"]}'
            f'</span>'
            f'<h3 style="margin: 4px 0 0 0; color: #38bdf8; font-size: 1.25rem; font-weight: 700;">{g["title"]}</h3>'
            f'</div>'
            f'<span class="badge-pill {p_badge}">{g["priority"]} Priority</span>'
            f'</div>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 18px; padding: 12px 18px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin-bottom: 14px; font-size: 0.9rem; color: #cbd5e1;">'
            f'<div>Your Current Value: <b style="color: #f8fafc;">{g["student_val"]}</b></div>'
            f'<div>Placed Benchmark Median: <b style="color: #38bdf8;">{g["benchmark_val"]}</b></div>'
            f'<div>Estimated Deficit / Gap: <b style="color: #fb7185;">{gap_text}</b></div>'
            f'{percentile_txt}'
            f'</div>'
            f'<div style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.6; border-left: 3px solid #38bdf8; padding: 10px 14px; background: rgba(56, 189, 248, 0.05); border-radius: 0 8px 8px 0;">'
            f'<b style="color: #38bdf8;">Actionable Recommendation:</b> {g["advice"]}'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.success("🌟 Congratulations! You have no critical gaps below the campus placed cohort median.")

# ----------------- SECTION 2: SUMMARY TABLE & EXPORT -----------------
if gaps:
    st.markdown("### 📋 Structured Gap Analysis Table")
    gap_table_data = []
    for g in gaps:
        gap_table_data.append({
            "Competency Area": g["title"],
            "Category": g["category"],
            "Your Value": g["student_val"],
            "Placed Median": g["benchmark_val"],
            "Deficit": f"{g['gap']} {g['unit']}",
            "Priority": g["priority"]
        })
    df_gap = pd.DataFrame(gap_table_data)
    st.dataframe(df_gap, use_container_width=True)

    csv_data = df_gap.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download My Personalized Action Plan (CSV)",
        data=csv_data,
        file_name=f"placement_action_plan_{user_id.lower()}.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ----------------- SECTION 3: REINFORCING STRENGTHS -----------------
st.markdown("### 🌟 Current Profile Strengths")
st.caption("Areas where your profile meets or exceeds campus placed benchmarks:")

strengths = rec_data.get("strengths", [])
if strengths:
    cols = st.columns(min(3, len(strengths)))
    for idx, s in enumerate(strengths):
        with cols[idx % len(cols)]:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 14px; padding: 16px; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #34d399; font-size: 0.95rem; margin-bottom: 4px;">✓ {s['title']}</div>
                <div style="font-size: 0.82rem; color: #cbd5e1;">{s['detail']}</div>
            </div>
            """, unsafe_allow_html=True)
