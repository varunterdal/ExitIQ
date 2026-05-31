import streamlit as st
from groq import Groq
import json
from utils.data_loader import load_executive_insights, load_theme_results, load_risk_results

st.set_page_config(page_title="AI Executive Insights",
                   page_icon="🤖", layout="wide")
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)

insights = load_executive_insights()
themes   = load_theme_results()
risk     = load_risk_results()

st.markdown(
    "<h1>🤖 AI Executive Insights</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "AI-powered executive intelligence with explainable evidence</p>",
    unsafe_allow_html=True
)
st.divider()

# ── API Key
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ''

api_key = st.text_input(
    "Enter your Groq API Key",
    type="password",
    placeholder="Paste your Groq API key here...",
    value=st.session_state.groq_api_key
)
if api_key:
    st.session_state.groq_api_key = api_key

if not st.session_state.groq_api_key:
    st.info("👆 Enter your Groq API key to unlock AI insights")
    st.stop()

client = Groq(api_key=st.session_state.groq_api_key)
st.success("✅ AI Connected")
st.divider()

# ── Evidence Panel (Explainability Layer)
st.markdown(
    "<div style='font-size:18px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:16px;'>🔍 Evidence Behind These Insights</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#a0aec0;font-size:13px;margin-top:-12px;"
    "margin-bottom:16px;'>"
    "Every AI insight below is generated from this verified data. "
    "No hallucination — only your workforce data.</p>",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #667eea;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Reviews Analyzed</div>"
        f"<div style='font-size:32px;font-weight:800;color:#667eea;'>"
        f"{insights['total_reviews_analyzed']:,}</div>"
        "<div style='font-size:11px;color:#a0aec0;'>Data points feeding AI</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #e74c3c;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Attrition Rate</div>"
        f"<div style='font-size:32px;font-weight:800;color:#e74c3c;'>"
        f"{insights['attrition_rate']}%</div>"
        "<div style='font-size:11px;color:#a0aec0;'>From HR records</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    top_theme = insights['top_themes'][0]['theme'] if insights['top_themes'] else 'N/A'
    top_count = insights['top_themes'][0]['count'] if insights['top_themes'] else 0
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #f39c12;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>#1 Theme</div>"
        f"<div style='font-size:18px;font-weight:800;color:#f39c12;"
        f"margin:8px 0;'>{top_theme}</div>"
        f"<div style='font-size:11px;color:#a0aec0;'>{top_count} mentions</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col4:
    pos_pct = insights['overall_sentiment']['positive_pct']
    neg_pct = insights['overall_sentiment']['negative_pct']
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #2ecc71;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Sentiment Split</div>"
        f"<div style='font-size:18px;font-weight:800;color:#2ecc71;"
        f"margin:4px 0;'>{pos_pct}% Positive</div>"
        f"<div style='font-size:11px;color:#e74c3c;'>{neg_pct}% Negative</div>"
        "</div>",
        unsafe_allow_html=True
    )

# ── Supporting Evidence Expander
with st.expander("📂 View Full Evidence Dataset used by AI", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 Top Themes (AI uses these)**")
        for i, t in enumerate(insights['top_themes'][:5]):
            st.markdown(
                f"<div style='padding:6px 0;border-bottom:"
                f"1px solid rgba(255,255,255,0.05);'>"
                f"<span style='color:#667eea;'>#{i+1}</span> "
                f"<span style='color:#e2e8f0;'>{t['theme']}</span> "
                f"<span style='color:#a0aec0;'>— {t['count']} mentions</span>"
                f"</div>",
                unsafe_allow_html=True
            )
    with col2:
        st.markdown("**⚠️ Attrition Drivers (AI uses these)**")
        for d in insights['top_attrition_drivers'][:5]:
            st.markdown(
                f"<div style='padding:6px 0;border-bottom:"
                f"1px solid rgba(255,255,255,0.05);'>"
                f"<span style='color:#e74c3c;'>▶</span> "
                f"<span style='color:#e2e8f0;'>{d['feature']}</span> "
                f"<span style='color:#a0aec0;'>— importance: {d['importance']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

st.divider()

# ── Build AI Context
context = f"""
You are an expert HR Analytics consultant analyzing workforce data.

VERIFIED DATA (use this as your evidence):
- Total reviews analyzed: {insights['total_reviews_analyzed']}
- Overall attrition rate: {insights['attrition_rate']}%
- Average employee rating: {insights['avg_overall_rating']}/5
- Positive sentiment: {insights['overall_sentiment']['positive_pct']}%
- Negative sentiment: {insights['overall_sentiment']['negative_pct']}%
- Neutral sentiment: {insights['overall_sentiment']['neutral_pct']}%
- Top theme: {insights['top_themes'][0]['theme']} ({insights['top_themes'][0]['count']} mentions)
- #2 theme: {insights['top_themes'][1]['theme']} ({insights['top_themes'][1]['count']} mentions)
- #3 theme: {insights['top_themes'][2]['theme']} ({insights['top_themes'][2]['count']} mentions)
- Top attrition driver: {insights['top_attrition_drivers'][0]['feature']}
- Annual attrition cost: ${insights['cost_of_attrition']:,.0f}

Top themes: {json.dumps(insights['top_themes'], indent=2)}
Top attrition drivers: {json.dumps(insights['top_attrition_drivers'], indent=2)}
Risk distribution: {json.dumps(insights['risk_distribution'], indent=2)}
Department attrition: {json.dumps(insights['dept_attrition'], indent=2)}

IMPORTANT: Always cite specific numbers from the data above in your response.
Always end your response with a "Confidence Score" line like:
**Confidence Score: XX% — based on N data points**
"""

def generate_insight(prompt, evidence_points):
    with st.spinner("🤖 AI is analyzing your workforce data..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user",   "content": prompt}
                ]
            )
            result = response.choices[0].message.content

            # Show evidence used
            st.markdown(
                "<div style='background:rgba(102,126,234,0.1);"
                "border:1px solid #667eea;border-radius:8px;"
                "padding:12px;margin-bottom:16px;'>"
                "<div style='font-size:12px;font-weight:700;color:#667eea;"
                "margin-bottom:8px;'>🔍 Evidence Used to Generate This Insight</div>"
                + "".join([
                    f"<div style='font-size:12px;color:#a0aec0;"
                    f"padding:2px 0;'>✓ {e}</div>"
                    for e in evidence_points
                ])
                + "</div>",
                unsafe_allow_html=True
            )

            st.markdown(result)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ── Insight Buttons
st.markdown(
    "<div style='font-size:18px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:8px;'>📊 Generate AI Insights</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#a0aec0;font-size:13px;margin-top:-8px;"
    "margin-bottom:16px;'>"
    "Each insight shows the exact data evidence it was generated from.</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
    btn1 = st.button("📋 Executive Summary",         use_container_width=True)
with col2:
    btn2 = st.button("⚠️ Attrition Risk Report",     use_container_width=True)
with col3:
    btn3 = st.button("🎯 Retention Strategy",         use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    btn4 = st.button("💬 Sentiment Analysis Report",  use_container_width=True)
with col5:
    btn5 = st.button("🏢 Department Intelligence",    use_container_width=True)
with col6:
    btn6 = st.button("🚀 90-Day HR Action Plan",      use_container_width=True)

st.divider()

if btn1:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>📋 Executive Summary</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate a professional executive summary of this workforce data.
Include:
1. Overall workforce health assessment
2. Key findings in 5 bullet points — cite specific numbers
3. Most critical areas needing attention
4. Overall risk level for the organization
5. Confidence Score at the end

Always reference actual numbers: {insights['attrition_rate']}% attrition,
{insights['total_reviews_analyzed']} reviews, 
{insights['overall_sentiment']['positive_pct']}% positive sentiment.
Keep it concise and suitable for C-suite presentation.""",
        [
            f"{insights['total_reviews_analyzed']:,} employee reviews analyzed",
            f"{insights['attrition_rate']}% overall attrition rate",
            f"{insights['overall_sentiment']['positive_pct']}% positive sentiment",
            f"Top theme: {insights['top_themes'][0]['theme']} ({insights['top_themes'][0]['count']} mentions)",
            f"Annual cost of attrition: ${insights['cost_of_attrition']:,.0f}"
        ]
    )

if btn2:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>⚠️ Attrition Risk Report</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate a detailed attrition risk report.
Include:
1. Current attrition situation — cite the {insights['attrition_rate']}% rate
2. Top 3 factors driving attrition from the data
3. Which departments are most at risk
4. Financial impact: ${insights['cost_of_attrition']:,.0f} annual cost
5. Urgency level: Low / Medium / High / Critical
6. Confidence Score at the end
Be specific and data-driven.""",
        [
            f"Attrition rate: {insights['attrition_rate']}%",
            f"Attrition count: {insights['attrition_count']} employees",
            f"Annual cost: ${insights['cost_of_attrition']:,.0f}",
            f"Top driver: {insights['top_attrition_drivers'][0]['feature']}",
            f"Risk distribution: {json.dumps(insights['risk_distribution'])}"
        ]
    )

if btn3:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>🎯 Retention Strategy</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate a comprehensive employee retention strategy.
Include:
1. Top 5 retention initiatives ranked by impact
2. Quick wins achievable in 30 days
3. Long-term strategic recommendations
4. Expected impact on the current {insights['attrition_rate']}% attrition rate
5. Implementation priority order
6. Confidence Score at the end
Make it actionable and specific to the data.""",
        [
            f"Current attrition: {insights['attrition_rate']}%",
            f"Top theme to address: {insights['top_themes'][0]['theme']}",
            f"#2 theme: {insights['top_themes'][1]['theme']}",
            f"Negative sentiment: {insights['overall_sentiment']['negative_pct']}%",
            f"Avg rating: {insights['avg_overall_rating']}/5"
        ]
    )

if btn4:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>💬 Sentiment Analysis Report</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate a sentiment analysis report for HR leadership.
Include:
1. Overall sentiment health — {insights['overall_sentiment']['positive_pct']}% positive, 
   {insights['overall_sentiment']['negative_pct']}% negative
2. What employees feel most positive about
3. What employees feel most negative about
4. Sentiment patterns by theme
5. Recommended communication strategies
6. Confidence Score at the end""",
        [
            f"Positive sentiment: {insights['overall_sentiment']['positive_pct']}%",
            f"Negative sentiment: {insights['overall_sentiment']['negative_pct']}%",
            f"Neutral sentiment: {insights['overall_sentiment']['neutral_pct']}%",
            f"Based on {insights['total_reviews_analyzed']:,} reviews",
            f"Avg rating: {insights['avg_overall_rating']}/5"
        ]
    )

if btn5:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>🏢 Department Intelligence</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate department-level workforce intelligence.
Include:
1. Which department needs most urgent attention and why
2. Department-specific attrition patterns from: {json.dumps(insights['dept_attrition'])}
3. Recommended interventions per department
4. Resource allocation recommendations
5. Priority order for HR intervention
6. Confidence Score at the end
Be specific about each department.""",
        [
            f"Department data: {len(insights['dept_attrition'])} departments analyzed",
            f"Overall attrition: {insights['attrition_rate']}%",
            f"Attrition count: {insights['attrition_count']} employees",
            "Department-level attrition rates from HR records",
            "Risk scores per department"
        ]
    )

if btn6:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>🚀 90-Day HR Action Plan</div>",
        unsafe_allow_html=True
    )
    generate_insight(
        f"""Generate a 90-day HR action plan based on this data.
Include:
1. Week 1-2: Immediate actions (address {insights['top_themes'][0]['theme']})
2. Month 1: Short term actions
3. Month 2-3: Medium term actions
4. Success metrics — target reducing {insights['attrition_rate']}% attrition
5. Key stakeholders to involve
6. Confidence Score at the end
Format as a clear action plan with deadlines.""",
        [
            f"Primary problem: {insights['top_themes'][0]['theme']}",
            f"Current attrition to reduce: {insights['attrition_rate']}%",
            f"Cost to recover: ${insights['cost_of_attrition']:,.0f}",
            f"Top driver to fix: {insights['top_attrition_drivers'][0]['feature']}",
            f"{insights['total_reviews_analyzed']:,} reviews as baseline"
        ]
    )