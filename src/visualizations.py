import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Campus Blue Color Tokens
CAMPUS_BLUE_PALETTE = ["#2563EB", "#60A5FA", "#16A34A", "#F59E0B", "#818CF8", "#0F172A"]

def base(fig, title=None):
    """Apply consistent Campus Blue light theme to Plotly figures."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#334155", family="Inter, -apple-system, BlinkMacSystemFont, sans-serif"),
        margin=dict(l=24, r=24, t=55 if title else 30, b=24),
        title=dict(text=title, font=dict(size=15, color="#0F172A", family="Inter, sans-serif")) if title else None,
        colorway=CAMPUS_BLUE_PALETTE,
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            linecolor="#E2E8F0",
            tickfont=dict(color="#64748B", size=11),
            title=dict(font=dict(color="#334155", size=12))
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            linecolor="#E2E8F0",
            tickfont=dict(color="#64748B", size=11),
            title=dict(font=dict(color="#334155", size=12))
        ),
        legend=dict(
            font=dict(color="#334155", size=11),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        )
    )
    return fig

def apply_campus_theme(fig, title=None):
    """Helper alias for base() to apply campus blue styling."""
    return base(fig, title)

def bar(df, x, y, title="", color=None, barmode="relative"):
    fig = px.bar(df, x=x, y=y, title=title, color=color, barmode=barmode, text_auto=True,
                 color_discrete_sequence=CAMPUS_BLUE_PALETTE)
    return base(fig, title)

def line(df, x, y, title="", markers=True):
    fig = px.line(df, x=x, y=y, title=title, markers=markers,
                  color_discrete_sequence=CAMPUS_BLUE_PALETTE)
    return base(fig, title)

def scatter(df, x, y, color=None, size=None, hover_data=None, title=""):
    fig = px.scatter(df, x=x, y=y, color=color, size=size, hover_data=hover_data, title=title, opacity=0.85,
                     color_discrete_sequence=CAMPUS_BLUE_PALETTE)
    return base(fig, title)

def pie(df, names, values, title="", hole=0.55, color_discrete_map=None):
    fig = px.pie(df, names=names, values=values, title=title, hole=hole, color=names,
                 color_discrete_map=color_discrete_map,
                 color_discrete_sequence=CAMPUS_BLUE_PALETTE)
    return base(fig, title)

def radar_comparison(student_vals: dict, cohort_vals: dict, title="Candidate vs. Placed Cohort Benchmark"):
    """Render a spider/radar chart comparing student skills against placed cohort averages in Campus Blue style."""
    categories = list(student_vals.keys())
    s_scores = [student_vals[c] for c in categories]
    c_scores = [cohort_vals[c] for c in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=c_scores + [c_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Placed Student Benchmark',
        line=dict(color='#2563EB', width=2),
        fillcolor='rgba(37, 99, 235, 0.12)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=s_scores + [s_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Profile',
        line=dict(color='#16A34A', width=3),
        fillcolor='rgba(22, 163, 74, 0.22)'
    ))
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#334155", family="Inter, sans-serif"),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E2E8F0', linecolor='#CBD5E1', tickfont=dict(color="#64748B", size=10)),
            angularaxis=dict(gridcolor='#E2E8F0', linecolor='#CBD5E1', tickfont=dict(color="#0F172A", size=11, family="Inter, sans-serif")),
            bgcolor='#FAFCFF'
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5, font=dict(color="#334155")),
        margin=dict(l=30, r=30, t=50 if title else 20, b=40),
        title=dict(text=title, font=dict(size=15, color="#0F172A")) if title else None
    )
    return fig

def confusion_matrix_heatmap(cm, labels=["Not Placed", "Placed"]):
    """Render annotated heatmap for a 2x2 confusion matrix in Campus Blue palette."""
    fig = px.imshow(
        cm,
        x=[f"Pred {l}" for l in labels],
        y=[f"Actual {l}" for l in labels],
        text_auto=True,
        color_continuous_scale=[[0, "#EFF6FF"], [0.5, "#93C5FD"], [1, "#1D4ED8"]],
        title="Annotated Confusion Matrix"
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        coloraxis_showscale=False,
        font=dict(color="#334155", family="Inter, sans-serif"),
        title=dict(text="Annotated Confusion Matrix", font=dict(size=15, color="#0F172A")),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

