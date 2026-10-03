import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def base(fig, title=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", family="Plus Jakarta Sans, sans-serif"),
        margin=dict(l=20, r=20, t=55, b=20),
        title=dict(text=title, font=dict(size=16, color="#f8fafc")) if title else None
    )
    return fig

def bar(df, x, y, title="", color=None, barmode="relative"):
    fig = px.bar(df, x=x, y=y, title=title, color=color, barmode=barmode, text_auto=True)
    return base(fig, title)

def line(df, x, y, title="", markers=True):
    fig = px.line(df, x=x, y=y, title=title, markers=markers)
    return base(fig, title)

def scatter(df, x, y, color=None, size=None, hover_data=None, title=""):
    fig = px.scatter(df, x=x, y=y, color=color, size=size, hover_data=hover_data, title=title, opacity=0.8)
    return base(fig, title)

def pie(df, names, values, title="", hole=0.55, color_discrete_map=None):
    fig = px.pie(df, names=names, values=values, title=title, hole=hole, color=names, color_discrete_map=color_discrete_map)
    return base(fig, title)

def radar_comparison(student_vals: dict, cohort_vals: dict, title="Candidate vs. Placed Cohort Benchmark"):
    """Render a spider/radar chart comparing student skills against placed cohort averages."""
    categories = list(student_vals.keys())
    s_scores = [student_vals[c] for c in categories]
    c_scores = [cohort_vals[c] for c in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=c_scores + [c_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Placed Student Benchmark',
        line=dict(color='#818cf8', width=2),
        fillcolor='rgba(129, 140, 248, 0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=s_scores + [s_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Profile',
        line=dict(color='#38bdf8', width=3),
        fillcolor='rgba(56, 189, 248, 0.35)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(148, 163, 184, 0.15)'),
            bgcolor='rgba(15, 23, 42, 0.6)'
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return base(fig, title)

def confusion_matrix_heatmap(cm, labels=["Not Placed", "Placed"]):
    """Render annotated heatmap for a 2x2 confusion matrix."""
    fig = px.imshow(
        cm,
        x=[f"Pred {l}" for l in labels],
        y=[f"Actual {l}" for l in labels],
        text_auto=True,
        color_continuous_scale="Blues",
        title="Annotated Confusion Matrix"
    )
    fig.update_layout(coloraxis_showscale=False)
    return base(fig, "Annotated Confusion Matrix")
