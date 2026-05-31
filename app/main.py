import streamlit as st
from utils.data_loader import load_executive_insights
from utils.styles import load_css

st.set_page_config(
    page_title="ExitIQ — AI Workforce Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(load_css(), unsafe_allow_html=True)

insights = load_executive_insights()
score    = insights['health_score']
label    = insights['health_label']



if score >= 80:
    h_color, h_bg, h_emoji = "#2ecc71", "rgba(46,204,113,0.08)",  "✅"
elif score >= 60:
    h_color, h_bg, h_emoji = "#f39c12", "rgba(243,156,18,0.08)",  "⚠️"
elif score >= 40:
    h_color, h_bg, h_emoji = "#e67e22", "rgba(230,126,34,0.08)",  "🔶"
else:
    h_color, h_bg, h_emoji = "#e74c3c", "rgba(231,76,60,0.08)",   "🚨"

# ── Sidebar
st.sidebar.markdown(
    "<div style='text-align:center;padding:10px 0 20px 0;'>"
    "<div style='font-size:40px;'>🧠</div>"
    "<div style='font-size:22px;font-weight:800;"
    "background:linear-gradient(90deg,#667eea,#764ba2);"
    "-webkit-background-clip:text;"
    "-webkit-text-fill-color:transparent;'>ExitIQ</div>"
    "<div style='font-size:11px;color:#a0aec0;margin-top:4px;'>"
    "AI Workforce Intelligence</div>"
    "</div>",
    unsafe_allow_html=True
)

st.sidebar.divider()
st.sidebar.markdown("### 📊 Overview")
st.sidebar.page_link("main.py",                            label="🏠 Home")
st.sidebar.markdown("### 🔍 Intelligence")
st.sidebar.page_link("pages/1_executive_dashboard.py",     label="📊 Executive Dashboard")
st.sidebar.page_link("pages/2_theme_intelligence.py",      label="🎯 Theme Intelligence")
st.sidebar.page_link("pages/3_sentiment_intelligence.py",  label="💬 Sentiment Intelligence")
st.sidebar.page_link("pages/4_attrition_drivers.py",       label="⚠️ Attrition Drivers")
st.sidebar.markdown("### 🚀 Action")
st.sidebar.page_link("pages/5_ai_insights.py",             label="🤖 AI Insights")
st.sidebar.page_link("pages/6_hr_copilot.py",              label="🤝 HR Copilot")
st.sidebar.page_link("pages/7_report_generator.py",        label="📄 Executive Report")
st.sidebar.markdown("### 🔬 Tools")
st.sidebar.page_link("pages/8_individual_analysis.py",     label="👤 Individual Analysis")
st.sidebar.page_link("pages/9_csv_upload.py",              label="📁 CSV Upload & Analyze")
st.sidebar.page_link("pages/10_methodology.py",            label="🔬 Methodology & Validation")
st.sidebar.divider()

st.sidebar.markdown(
    f"<div style='background:{h_bg};"
    f"border:1px solid {h_color};"
    "border-radius:12px;padding:16px;text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;letter-spacing:2px;"
    "text-transform:uppercase;'>Workforce Health</div>"
    f"<div style='font-size:40px;font-weight:900;color:{h_color};'>"
    f"{score}</div>"
    f"<div style='font-size:12px;color:{h_color};font-weight:600;'>"
    f"{h_emoji} {label}</div>"
    "</div>",
    unsafe_allow_html=True
)

# ── Hero
st.markdown(
    "<div style='text-align:center;padding:30px 0 4px 0;'>"
    "<div style='font-size:13px;color:#a0aec0;letter-spacing:4px;"
    "text-transform:uppercase;margin-bottom:4px;'>AI Workforce Intelligence</div>"
    "<div style='font-size:48px;font-weight:900;margin:0;"
    "background:linear-gradient(90deg,#667eea,#764ba2,#f64f59);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>"
    "🧠 ExitIQ</div>"
    "<div style='font-size:15px;color:#718096;margin-top:6px;'>"
    "Turning employee feedback into executive decisions</div>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="max-width:1100px;">

<h1 style="
    font-size:2.8rem;
    font-weight:800;
    margin-bottom:10px;
    text-align:center;
">                     Welcome to ExitIQ 
</h1>

<p style="
    color:#A1A1AA;
    font-size:1.1rem;
    line-height:1.8;
    margin-bottom:15px;
            text-align:center;
">
ExitIQ enables organizations to convert large volumes of employee feedback and exit interview data into actionable business insights. The platform leverages AI-driven analytics to identify sentiment trends, workforce concerns, and critical attrition drivers, providing HR leaders with a comprehensive understanding of employee experiences.
</p>

<p style="
    color:#D4D4D8;
    font-size:1.05rem;
    line-height:1.8;
            text-align:center;
">
By combining workforce intelligence, executive reporting, and data-driven recommendations, ExitIQ supports proactive decision-making, strengthens retention strategies, and helps organizations build a healthier, more sustainable workplace culture.
</p>
<br>
            <br>
            <br>
       <p style="
    color:#D4D4D8;
    font-size:1.05rem;
    line-height:1.8;
            text-align:center;
">
            Important Stats and Insights
</p>     
</div>
""", unsafe_allow_html=True)
# ── Workforce Health Score
st.markdown(
    f"<div style='background:{h_bg};border:2px solid {h_color};"
    "border-radius:20px;padding:40px;text-align:center;'>"
    "<div style='font-size:13px;color:#a0aec0;letter-spacing:4px;"
    "text-transform:uppercase;margin-bottom:8px;'>Workforce Health Score</div>"
    f"<div style='font-size:100px;font-weight:900;color:{h_color};"
    f"line-height:1;margin-bottom:8px;'>{score}</div>"
    f"<div style='font-size:26px;font-weight:700;color:{h_color};"
    f"margin-bottom:16px;'>{h_emoji} {label}</div>"
    f"<div style='width:60px;height:3px;background:{h_color};"
    "margin:0 auto 20px;border-radius:2px;'></div>"
    "<div style='display:flex;justify-content:center;gap:40px;flex-wrap:wrap;'>"
    "<div style='text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>Reviews Analyzed</div>"
    f"<div style='font-size:24px;font-weight:800;color:#e2e8f0;'>"
    f"{insights['total_reviews_analyzed']:,}</div>"
    "</div>"
    "<div style='text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>Attrition Rate</div>"
    f"<div style='font-size:24px;font-weight:800;color:#e74c3c;'>"
    f"{insights['attrition_rate']}%</div>"
    "</div>"
    "<div style='text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>Positive Sentiment</div>"
    f"<div style='font-size:24px;font-weight:800;color:#2ecc71;'>"
    f"{insights['overall_sentiment']['positive_pct']}%</div>"
    "</div>"
    "<div style='text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>Annual Cost</div>"
    f"<div style='font-size:24px;font-weight:800;color:#e74c3c;'>"
    f"${insights['cost_of_attrition']/1000000:.1f}M</div>"
    "</div>"
    "<div style='text-align:center;'>"
    "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>Avg Rating</div>"
    f"<div style='font-size:24px;font-weight:800;color:#f39c12;'>"
    f"{insights['avg_overall_rating']}/5</div>"
    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ── Cost Banner
st.markdown(
    "<div style='background:linear-gradient(135deg,"
    "rgba(231,76,60,0.12),rgba(192,57,43,0.12));"
    "border:1px solid rgba(231,76,60,0.4);border-radius:12px;"
    "padding:18px 28px;display:flex;align-items:center;"
    "justify-content:space-between;flex-wrap:wrap;gap:12px;'>"
    "<div>"
    "<div style='font-size:12px;color:#a0aec0;text-transform:uppercase;"
    "letter-spacing:2px;'>💸 Estimated Annual Cost of Current Attrition</div>"
    f"<div style='font-size:38px;font-weight:900;color:#e74c3c;'>"
    f"${insights['cost_of_attrition']:,.0f}</div>"
    "</div>"
    "<div style='text-align:right;'>"
    f"<div style='font-size:13px;color:#a0aec0;'>"
    f"{insights['attrition_count']} employees leaving</div>"
    f"<div style='font-size:13px;color:#a0aec0;'>"
    f"x ${insights['cost_per_employee']:,.0f} replacement cost each</div>"
    "<div style='font-size:12px;color:#e74c3c;margin-top:4px;"
    "font-weight:600;'>Every month of inaction = more loss</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)

st.divider()

# ── Live Intelligence
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#a0aec0;"
    "text-transform:uppercase;letter-spacing:3px;"
    "margin-bottom:16px;'>📡 Live Intelligence</div>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    top_themes = insights['top_themes'][:3]
    medals     = ['🥇','🥈','🥉']
    rows       = ""
    for i, t in enumerate(top_themes):
        rows += (
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;padding:10px 0;"
            "border-bottom:1px solid rgba(255,255,255,0.05);'>"
            f"<span style='color:#e2e8f0;font-size:14px;'>"
            f"{medals[i]} {t['theme']}</span>"
            f"<span style='background:rgba(102,126,234,0.2);color:#667eea;"
            f"font-weight:700;padding:2px 10px;border-radius:20px;"
            f"font-size:13px;'>{t['count']}</span>"
            "</div>"
        )
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #667eea;border-radius:16px;padding:24px;'>"
        "<div style='font-size:13px;font-weight:700;color:#667eea;"
        "text-transform:uppercase;letter-spacing:2px;"
        "margin-bottom:16px;'>🎯 Why Employees Leave</div>"
        + rows +
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    drivers = insights['top_attrition_drivers'][:3]
    rows2   = ""
    for d in drivers:
        pct = round(d['importance'] * 100, 1)
        rows2 += (
            "<div style='padding:10px 0;"
            "border-bottom:1px solid rgba(255,255,255,0.05);'>"
            "<div style='display:flex;justify-content:space-between;"
            "margin-bottom:6px;'>"
            f"<span style='color:#e2e8f0;font-size:13px;'>{d['feature']}</span>"
            f"<span style='color:#e74c3c;font-size:12px;font-weight:700;'>"
            f"{pct}%</span>"
            "</div>"
            "<div style='background:rgba(231,76,60,0.15);border-radius:4px;"
            "height:5px;'>"
            f"<div style='background:linear-gradient(90deg,#e74c3c,#c0392b);"
            f"width:{min(pct*5,100)}%;height:5px;border-radius:4px;'></div>"
            "</div>"
            "</div>"
        )
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #e74c3c;border-radius:16px;padding:24px;'>"
        "<div style='font-size:13px;font-weight:700;color:#e74c3c;"
        "text-transform:uppercase;letter-spacing:2px;"
        "margin-bottom:16px;'>⚠️ Top Attrition Drivers</div>"
        + rows2 +
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    risk_dist = insights['risk_distribution']
    total_emp = sum(r['count'] for r in risk_dist)
    rows3     = ""
    for r in risk_dist:
        if r['risk_level'] == 'High Risk':
            rc, re = "#e74c3c", "🔴"
        elif r['risk_level'] == 'Medium Risk':
            rc, re = "#f39c12", "🟡"
        else:
            rc, re = "#2ecc71", "🟢"
        pct = round(r['count'] / total_emp * 100, 1) if total_emp else 0
        rows3 += (
            "<div style='padding:10px 0;"
            "border-bottom:1px solid rgba(255,255,255,0.05);'>"
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px;'>"
            f"<span style='color:#e2e8f0;font-size:13px;'>{re} {r['risk_level']}</span>"
            f"<span style='color:{rc};font-weight:700;font-size:13px;'>"
            f"{r['count']} ({pct}%)</span>"
            "</div>"
            f"<div style='background:rgba(255,255,255,0.05);border-radius:4px;"
            "height:5px;'>"
            f"<div style='background:{rc};width:{pct}%;height:5px;"
            "border-radius:4px;'></div>"
            "</div>"
            "</div>"
        )
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #f39c12;border-radius:16px;padding:24px;'>"
        "<div style='font-size:13px;font-weight:700;color:#f39c12;"
        "text-transform:uppercase;letter-spacing:2px;"
        "margin-bottom:16px;'>🚨 Employee Risk Distribution</div>"
        + rows3 +
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Navigation
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#a0aec0;"
    "text-transform:uppercase;letter-spacing:3px;"
    "margin-bottom:16px;'>🚀 What do you want to do?</div>",
    unsafe_allow_html=True
)

nav_items = [
    ("📊", "Executive Dashboard", "Full KPIs, charts & trends",   "#667eea"),
    ("🎯", "Theme Intelligence",  "Why employees are unhappy",     "#764ba2"),
    ("💬", "Sentiment Analysis",  "How employees feel",            "#f64f59"),
    ("⚠️", "Attrition Drivers",  "What drives people to leave",   "#e74c3c"),
    ("🤖", "AI Insights",         "AI-powered recommendations",    "#2ecc71"),
    ("🤝", "HR Copilot",          "Ask anything about your data",  "#3498db"),
    ("📄", "Executive Report",    "Download board-ready report",   "#9b59b6"),
    ("👤", "Individual Analysis", "Analyze one employee review",   "#f39c12"),
    ("📁", "CSV Upload",          "Upload & analyze your own data","#e67e22"),
    ("🔬", "Methodology",         "How we validate results",       "#1abc9c"),
]

cols1 = st.columns(5)
for col, (icon, title, desc, color) in zip(cols1, nav_items[:5]):
    with col:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border:1px solid {color};border-radius:12px;padding:18px;"
            "text-align:center;'>"
            f"<div style='font-size:28px;margin-bottom:6px;'>{icon}</div>"
            "<div style='font-size:13px;font-weight:700;"
            f"color:#e2e8f0;margin-bottom:4px;'>{title}</div>"
            f"<div style='font-size:11px;color:#a0aec0;'>{desc}</div>"
            "</div>",
            unsafe_allow_html=True
        )

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

cols2 = st.columns(5)
for col, (icon, title, desc, color) in zip(cols2, nav_items[5:]):
    with col:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border:1px solid {color};border-radius:12px;padding:18px;"
            "text-align:center;'>"
            f"<div style='font-size:28px;margin-bottom:6px;'>{icon}</div>"
            "<div style='font-size:13px;font-weight:700;"
            f"color:#e2e8f0;margin-bottom:4px;'>{title}</div>"
            f"<div style='font-size:11px;color:#a0aec0;'>{desc}</div>"
            "</div>",
            unsafe_allow_html=True
        )

# ── Footer
st.divider()
st.markdown(
    "<div style='text-align:center;color:#4a5568;font-size:12px;"
    "padding:16px 0;'>"
    "ExitIQ — AI Workforce Intelligence Platform | "
    "Built with KLETECH for HR Leaders | "
    "Powered by Groq AI + Streamlit"
    "</div>",
    unsafe_allow_html=True
)