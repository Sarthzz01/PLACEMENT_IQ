import streamlit as st
import pandas as pd
import plotly.express as px
from src.auth import require_student
from src.database import get_student_prediction_history, get_student_feedback
from src.visualizations import base
from src.ui import css, hero, render_top_navbar

css()
require_student()

email = st.session_state.user_email
name = st.session_state.user_name
user_id = st.session_state.user_id

render_top_navbar(role="Student", user_name=name, user_id=f"{user_id} • {email}")

hero(
    "Prediction History & Audit Log",
    "Review your historical assessment runs, probability trajectory across iterations, and official faculty recommendations.",
    tag="Historical Records"
)

hist_df = get_student_prediction_history(email)
fb_df = get_student_feedback(email)

if len(hist_df) == 0:
    st.info("No prediction attempts recorded in the database yet. Head to **'Placement Prediction'** to generate your first assessment!")
    if st.button("🎯 Run Placement Prediction Now", type="primary"):
        st.switch_page("pages/3_Placement_Prediction.py")
else:
    # Summary Metrics Strip
    latest = hist_df.iloc[0]
    avg_prob = hist_df["probability"].mean() * 100
    placed_count = len(hist_df[hist_df["predicted_status"] == "Placed"])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Assessments", f"{len(hist_df)}", "Evaluations Stored")
    with m2:
        st.metric("Latest Status", latest["predicted_status"], f"{float(latest['probability'])*100:.1f}% Confidence")
    with m3:
        st.metric("Average Probability", f"{avg_prob:.1f}%", "Overall Trajectory")
    with m4:
        st.metric("Placed Outcomes", f"{placed_count} / {len(hist_df)}", "Success Ratio")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Historical Probability Progression Chart
    if len(hist_df) > 1:
        st.markdown("### 📈 Readiness Probability Progression")
        chart_df = hist_df.sort_values("id").copy()
        chart_df["probability_pct"] = chart_df["probability"] * 100
        fig_trend = px.line(
            chart_df,
            x="predicted_at",
            y="probability_pct",
            markers=True,
            title="Readiness Probability % Over Time",
            labels={"predicted_at": "Evaluation Timestamp", "probability_pct": "Estimated Probability (%)"}
        )
        fig_trend = base(fig_trend, "Readiness Probability % Over Time")
        fig_trend.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_trend, use_container_width=True)

    # Detailed Records Table
    st.markdown("### 📜 Prediction Log Records (Stored in SQLite)")
    
    display_df = hist_df[[
        "predicted_at", "predicted_status", "probability", "model_name", "evaluated_by"
    ]].copy()
    display_df["probability"] = (display_df["probability"] * 100).round(1).astype(str) + "%"
    display_df.columns = ["Timestamp", "Prediction", "Probability", "Model Used", "Evaluator"]

    st.dataframe(display_df, use_container_width=True)

    # Download CSV
    csv_bytes = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download My Prediction History (CSV)",
        data=csv_bytes,
        file_name=f"placement_prediction_history_{user_id.lower()}.csv",
        mime="text/csv"
    )

# ----------------- ADMIN FEEDBACK SECTION -----------------
st.markdown("---")
st.markdown("### 🛡️ Faculty & Administrator Feedback History")

if len(fb_df) > 0:
    for _, fb in fb_df.iterrows():
        p_badge = "badge-danger" if fb["priority"] == "High" else "badge-info"
        st.markdown(f"""
        <div class="campus-card" style="margin-bottom: 12px; padding: 16px 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <b style="color:#0F172A; font-size:0.95rem;">Assessment: {fb['prediction']}</b>
                <span class="badge-pill {p_badge}">{fb['priority']} Priority</span>
            </div>
            <p style="color:#475569; font-size:0.9rem; margin:0 0 6px 0; line-height:1.5;">
                "{fb['recommendation']}"
            </p>
            <div style="font-size:0.75rem; color:#64748B;">
                Submitted by <b>{fb['admin_name']}</b> on <code>{fb['created_at']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No formal administrator notes or feedback submitted yet.")
