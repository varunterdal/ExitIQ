import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_all
from utils.styles import load_css

st.set_page_config(page_title="Executive Dashboard",
                   page_icon="📊", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

data     = load_all()
insights = data['insights']
themes   = data['themes']
sentiment= data['sentiment']
risk     = data['risk']

# ── Header
st.markdown(
    "<h1>📊 Executive Dashboard</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "The Executive Dashboard transforms employee feedback into actionable business insights. It highlights workforce health, top attrition drivers, sentiment trends, and recommended HR actions, enabling faster and more informed decision-making.</p>",
    unsafe_allow_html=True
)
st.divider()

# ── Health Score + KPIs
score = insights['health_score']
label = insights['health_label']
if score >= 80:
    border_col = "#2ecc71"
    emoji      = "✅"
elif score >= 60:
    border_col = "#f39c12"
    emoji      = "⚠️"
elif score >= 40:
    border_col = "#e67e22"
    emoji      = "🔶"
else:
    border_col = "#e74c3c"
    emoji      = "🚨"

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        f"border:2px solid {border_col};border-radius:12px;padding:20px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Health Score</div>"
        f"<div style='font-size:40px;font-weight:900;color:{border_col};'>"
        f"{score}</div>"
        f"<div style='font-size:11px;color:{border_col};font-weight:600;'>"
        f"{emoji} {label}</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #e74c3c;border-radius:12px;padding:20px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Attrition Rate</div>"
        f"<div style='font-size:40px;font-weight:900;color:#e74c3c;'>"
        f"{insights['attrition_rate']}%</div>"
        "<div style='font-size:11px;color:#e74c3c;'>⬆ Needs attention</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #2ecc71;border-radius:12px;padding:20px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Positive Sentiment</div>"
        f"<div style='font-size:40px;font-weight:900;color:#2ecc71;'>"
        f"{insights['overall_sentiment']['positive_pct']}%</div>"
        "<div style='font-size:11px;color:#2ecc71;'>💬 Employee reviews</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #e74c3c;border-radius:12px;padding:20px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Annual Cost</div>"
        f"<div style='font-size:40px;font-weight:900;color:#e74c3c;'>"
        f"${insights['cost_of_attrition']/1000000:.1f}M</div>"
        "<div style='font-size:11px;color:#e74c3c;'>💸 Attrition cost</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #3498db;border-radius:12px;padding:20px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Avg Rating</div>"
        f"<div style='font-size:40px;font-weight:900;color:#3498db;'>"
        f"{insights['avg_overall_rating']}/5</div>"
        "<div style='font-size:11px;color:#3498db;'>⭐ Satisfaction</div>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Row 2 Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:8px;'>🎯 Top Themes in Employee Feedback</div>",
        unsafe_allow_html=True
    )
    fig1 = px.bar(
        themes.head(8).sort_values('count', ascending=True),
        x='count',
        y='theme',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        labels={'count':'Mentions','theme':'Theme'},
        text='count'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:8px;'>💬 Overall Sentiment Distribution</div>",
        unsafe_allow_html=True
    )
    sentiment_counts = sentiment['overall_sentiment'].value_counts()
    fig2 = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        color=sentiment_counts.index,
        color_discrete_map={
            'Positive':'#2ecc71',
            'Negative':'#e74c3c',
            'Neutral': '#f39c12'
        },
        hole=0.5
    )
    fig2.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Row 3 Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:8px;'>🚨 Employee Risk Distribution</div>",
        unsafe_allow_html=True
    )
    risk_counts = risk['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level','count']
    fig3 = px.pie(
        risk_counts,
        values='count',
        names='risk_level',
        color='risk_level',
        color_discrete_map={
            'High Risk':  '#e74c3c',
            'Medium Risk':'#f39c12',
            'Low Risk':   '#2ecc71'
        },
        hole=0.5
    )
    fig3.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0')
        )
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:8px;'>🏢 Attrition Rate by Department</div>",
        unsafe_allow_html=True
    )
    dept_df = pd.DataFrame(insights['dept_attrition'])
    fig4 = px.bar(
        dept_df,
        x='department',
        y='attrition_rate',
        color='attrition_rate',
        color_continuous_scale='Reds',
        labels={'attrition_rate':'Attrition %','department':'Department'},
        text='attrition_rate'
    )
    fig4.update_traces(
        texttemplate='%{text}%',
        textposition='outside'
    )
    fig4.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Row 4 — Theme Ratings
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:8px;'>⭐ Average Employee Rating by Theme</div>",
    unsafe_allow_html=True
)
fig5 = px.bar(
    themes.sort_values('avg_rating', ascending=False),
    x='theme',
    y='avg_rating',
    color='avg_rating',
    color_continuous_scale='RdYlGn',
    labels={'avg_rating':'Avg Rating','theme':'Theme'},
    text='avg_rating'
)
fig5.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)
fig5.update_layout(
    height=380,
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e2e8f0'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── Executive Action Center
st.markdown(
    "<h2>🎯 Executive Action Center</h2>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Prioritized recommendations for HR leadership</p>",
    unsafe_allow_html=True
)

actions = [
    {
        "priority":   "🔴 CRITICAL",
        "color":      "#e74c3c",
        "issue":      "High Monthly Income Disparity",
        "impact":     f"${insights['cost_of_attrition']/1000000:.1f}M annual cost",
        "action":     "Conduct immediate compensation benchmarking",
        "outcome":    "20-30% reduction in income-driven exits",
        "timeline":   "30 days"
    },
    {
        "priority":   "🟡 HIGH",
        "color":      "#f39c12",
        "issue":      "Compensation & Culture Dissatisfaction",
        "impact":     f"Top 2 themes in {insights['total_reviews_analyzed']:,} reviews",
        "action":     "Launch culture survey + compensation review",
        "outcome":    "15-20% improvement in sentiment score",
        "timeline":   "60 days"
    },
    {
        "priority":   "🟢 MONITOR",
        "color":      "#2ecc71",
        "issue":      "Career Growth Concerns",
        "impact":     "3rd most mentioned theme by employees",
        "action":     "Implement career development framework",
        "outcome":    "Improved retention of high performers",
        "timeline":   "90 days"
    }
]

for a in actions:
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        f"border-left:4px solid {a['color']};border-radius:12px;"
        "padding:20px;margin-bottom:12px;'>"
        "<div style='display:flex;justify-content:space-between;"
        "align-items:center;margin-bottom:12px;'>"
        f"<span style='color:{a['color']};font-weight:700;font-size:14px;'>"
        f"{a['priority']}</span>"
        f"<span style='color:#a0aec0;font-size:12px;'>⏱ {a['timeline']}</span>"
        "</div>"
        f"<div style='color:#e2e8f0;font-weight:700;font-size:16px;"
        f"margin-bottom:8px;'>{a['issue']}</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr 1fr;"
        "gap:12px;margin-top:8px;'>"
        "<div>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:1px;'>Business Impact</div>"
        f"<div style='color:#e2e8f0;font-size:13px;'>{a['impact']}</div>"
        "</div>"
        "<div>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:1px;'>Recommended Action</div>"
        f"<div style='color:#e2e8f0;font-size:13px;'>{a['action']}</div>"
        "</div>"
        "<div>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:1px;'>Expected Outcome</div>"
        f"<div style='color:#e2e8f0;font-size:13px;'>{a['outcome']}</div>"
        "</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )