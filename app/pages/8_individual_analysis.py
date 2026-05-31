import streamlit as st
from groq import Groq
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.styles import load_css

st.set_page_config(page_title="Individual Employee Analysis",
                   page_icon="👤", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

analyzer = SentimentIntensityAnalyzer()

# ── Header
st.markdown(
    "<h1>👤 Individual Employee Analysis</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Analyze a single employee review or exit interview transcript</p>",
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
    st.info("👆 Enter your Groq API key to enable AI analysis")
    st.stop()

client = Groq(api_key=st.session_state.groq_api_key)
st.success("✅ AI Connected")
st.divider()

# ── Input Section
st.markdown(
    "<div style='font-size:18px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:8px;'>📝 Enter Employee Review or Exit Interview</div>",
    unsafe_allow_html=True
)

# Sample reviews for quick testing
st.markdown(
    "<div style='font-size:13px;color:#a0aec0;margin-bottom:8px;'>"
    "💡 Try a sample:</div>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
    s1 = st.button("😞 Negative Sample",  use_container_width=True)
with col2:
    s2 = st.button("😊 Positive Sample",  use_container_width=True)
with col3:
    s3 = st.button("😐 Mixed Sample",     use_container_width=True)

samples = {
    's1': """The management here is completely toxic. My manager never 
listened to any of my concerns and constantly micromanaged everything 
I did. The pay was below market rate and despite promises of raises 
nothing ever happened. Work life balance was terrible - I was expected 
to be available 24/7. After 2 years I decided I had to leave for my 
own mental health. The only positive was my immediate team who were 
great people but leadership ruined the culture completely.""",

    's2': """I had an amazing experience at this company. Great work life 
balance, flexible hours and remote work options made it easy to manage 
personal commitments. My manager was supportive and genuinely invested 
in my career growth. Got promoted twice in 3 years. Compensation was 
competitive and the benefits package was excellent. The culture was 
inclusive and collaborative. I only left because I got an opportunity 
abroad otherwise I would have stayed long term.""",

    's3': """Mixed feelings about my time here. The technical work was 
interesting and I learned a lot. However the compensation was not 
competitive especially compared to industry standards. Management was 
hit or miss - some managers were great others were difficult to work 
with. Work life balance was okay most of the time but during project 
deadlines it got very stressful. Career growth opportunities were 
limited in my department. Overall a decent place to work but room 
for improvement in several areas."""
}

default_text = ""
if s1: default_text = samples['s1']
if s2: default_text = samples['s2']
if s3: default_text = samples['s3']

review_text = st.text_area(
    "Employee Review / Exit Interview Text",
    value=default_text,
    height=180,
    placeholder="Paste employee review, exit interview transcript, "
                "or any employee feedback here..."
)

analyze_btn = st.button(
    "🔍 Analyze This Review",
    use_container_width=True
)

if analyze_btn and review_text.strip():

    st.divider()

    # ── Step 1 — VADER Sentiment
    scores     = analyzer.polarity_scores(review_text)
    compound   = scores['compound']
    positive   = round(scores['pos'] * 100, 1)
    negative   = round(scores['neg'] * 100, 1)
    neutral    = round(scores['neu'] * 100, 1)

    if compound >= 0.05:
        sentiment_label = "Positive"
        sentiment_color = "#2ecc71"
        sentiment_emoji = "😊"
    elif compound <= -0.05:
        sentiment_label = "Negative"
        sentiment_color = "#e74c3c"
        sentiment_emoji = "😞"
    else:
        sentiment_label = "Neutral"
        sentiment_color = "#f39c12"
        sentiment_emoji = "😐"

    # ── Step 2 — Theme Detection
    themes = {
        'Work Life Balance': ['work life balance','flexible','overtime',
                              'remote','wfh','schedule','time off'],
        'Management':        ['manager','management','leadership',
                              'supervisor','boss','micromanage'],
        'Compensation':      ['salary','pay','compensation','benefits',
                              'bonus','raise','underpaid'],
        'Career Growth':     ['promotion','growth','career','learning',
                              'training','development','opportunity'],
        'Culture':           ['culture','environment','diversity',
                              'toxic','politics','team','collaboration'],
        'Job Security':      ['layoff','job security','unstable',
                              'restructure','uncertain'],
        'Workload':          ['workload','stress','burnout',
                              'overworked','demanding','exhausted'],
        'Recognition':       ['recognition','appreciated','valued',
                              'ignored','feedback','acknowledge']
    }

    text_lower     = review_text.lower()
    detected       = []
    for theme, keywords in themes.items():
        for kw in keywords:
            if kw in text_lower:
                detected.append(theme)
                break

    primary_theme   = detected[0] if len(detected) > 0 else "General"
    secondary_theme = detected[1] if len(detected) > 1 else "General"

    # ── Step 3 — Risk Score
    risk_score = 50
    if compound <= -0.05:  risk_score += 20
    if compound <= -0.3:   risk_score += 10
    if 'management' in detected or 'Management' in detected:
        risk_score += 10
    if 'compensation' in detected or 'Compensation' in detected:
        risk_score += 10
    if 'workload' in detected or 'Workload' in detected:
        risk_score += 5
    if compound >= 0.05:   risk_score -= 20
    risk_score = max(0, min(100, risk_score))

    if risk_score >= 70:
        risk_label = "High Risk"
        risk_color = "#e74c3c"
        risk_emoji = "🔴"
    elif risk_score >= 40:
        risk_label = "Medium Risk"
        risk_color = "#f39c12"
        risk_emoji = "🟡"
    else:
        risk_label = "Low Risk"
        risk_color = "#2ecc71"
        risk_emoji = "🟢"

    # ── Step 4 — AI Analysis
    with st.spinner("🤖 AI is analyzing this review..."):
        try:
            ai_prompt = f"""
You are an expert HR analyst. Analyze this employee review:

"{review_text}"

Provide a JSON response with exactly these fields:
{{
    "primary_concern": "one sentence describing main concern",
    "secondary_concern": "one sentence describing second concern",
    "emotional_tone": "one word: Frustrated/Satisfied/Neutral/Burned Out/Hopeful",
    "flight_risk": "Immediate/High/Medium/Low",
    "key_quote": "most important quote from the review under 20 words",
    "hr_action_1": "specific immediate HR action",
    "hr_action_2": "specific medium term HR action",
    "hr_action_3": "specific long term HR action",
    "manager_alert": "yes or no - should manager be alerted",
    "confidence": "percentage how confident you are in this analysis"
}}
Return only valid JSON. No explanation.
"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": ai_prompt}
                ]
            )
            import json
            raw      = response.choices[0].message.content
            clean    = raw.strip().replace('```json','').replace('```','')
            ai_data  = json.loads(clean)
        except Exception as e:
            ai_data = {
                "primary_concern":   "Unable to parse — see manual analysis",
                "secondary_concern": "Unable to parse",
                "emotional_tone":    "Unknown",
                "flight_risk":       "Unknown",
                "key_quote":         review_text[:100],
                "hr_action_1":       "Review manually",
                "hr_action_2":       "Conduct follow-up interview",
                "hr_action_3":       "Monitor employee",
                "manager_alert":     "yes",
                "confidence":        "N/A"
            }

    # ── Display Results

    # Row 1 — Key Metrics
    st.markdown(
        "<div style='font-size:18px;font-weight:700;"
        "color:#e2e8f0;margin-bottom:16px;'>"
        "📊 Analysis Results</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border:1px solid {sentiment_color};border-radius:12px;"
            "padding:20px;text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:2px;'>Sentiment</div>"
            f"<div style='font-size:36px;'>{sentiment_emoji}</div>"
            f"<div style='font-size:18px;font-weight:700;"
            f"color:{sentiment_color};'>{sentiment_label}</div>"
            f"<div style='font-size:12px;color:#a0aec0;'>"
            f"Score: {compound:.3f}</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #667eea;border-radius:12px;"
            "padding:20px;text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:2px;'>Primary Theme</div>"
            "<div style='font-size:28px;'>🎯</div>"
            f"<div style='font-size:16px;font-weight:700;color:#667eea;'>"
            f"{primary_theme}</div>"
            f"<div style='font-size:12px;color:#a0aec0;'>"
            f"Secondary: {secondary_theme}</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border:1px solid {risk_color};border-radius:12px;"
            "padding:20px;text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:2px;'>Risk Level</div>"
            f"<div style='font-size:36px;'>{risk_emoji}</div>"
            f"<div style='font-size:18px;font-weight:700;"
            f"color:{risk_color};'>{risk_label}</div>"
            f"<div style='font-size:12px;color:#a0aec0;'>"
            f"Score: {risk_score}/100</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col4:
        flight   = ai_data.get('flight_risk','Unknown')
        f_color  = ("#e74c3c" if flight == "Immediate"
                    else "#f39c12" if flight == "High"
                    else "#2ecc71")
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border:1px solid {f_color};border-radius:12px;"
            "padding:20px;text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:2px;'>Flight Risk</div>"
            "<div style='font-size:28px;'>✈️</div>"
            f"<div style='font-size:18px;font-weight:700;"
            f"color:{f_color};'>{flight}</div>"
            f"<div style='font-size:12px;color:#a0aec0;'>"
            f"Confidence: {ai_data.get('confidence','N/A')}</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Row 2 — AI Insights
    col1, col2 = st.columns(2)

    with col1:
        tone    = ai_data.get('emotional_tone','Unknown')
        concern = ai_data.get('primary_concern','N/A')
        concern2= ai_data.get('secondary_concern','N/A')
        quote   = ai_data.get('key_quote','N/A')
        alert   = ai_data.get('manager_alert','no')
        a_color = "#e74c3c" if alert == 'yes' else "#2ecc71"
        a_text  = "⚠️ YES — Alert Manager" if alert == 'yes' \
                  else "✅ No Alert Needed"

        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #0f3460;border-radius:12px;padding:24px;'>"
            "<div style='font-size:16px;font-weight:700;color:#667eea;"
            "margin-bottom:16px;'>🧠 AI Intelligence Report</div>"

            "<div style='margin-bottom:12px;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:1px;'>Emotional Tone</div>"
            f"<div style='color:#e2e8f0;font-size:14px;'>{tone}</div>"
            "</div>"

            "<div style='margin-bottom:12px;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:1px;'>Primary Concern</div>"
            f"<div style='color:#e2e8f0;font-size:14px;'>{concern}</div>"
            "</div>"

            "<div style='margin-bottom:12px;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:1px;'>Secondary Concern</div>"
            f"<div style='color:#e2e8f0;font-size:14px;'>{concern2}</div>"
            "</div>"

            "<div style='margin-bottom:12px;'>"
            "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
            "letter-spacing:1px;'>Key Quote</div>"
            f"<div style='color:#f39c12;font-size:14px;font-style:italic;'>"
            f'"{quote}"</div>'
            "</div>"

            "<div style='margin-top:16px;padding:12px;"
            f"background:rgba(0,0,0,0.2);border-left:3px solid {a_color};"
            "border-radius:4px;'>"
            "<div style='font-size:11px;color:#a0aec0;'>Manager Alert</div>"
            f"<div style='color:{a_color};font-weight:700;'>{a_text}</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        a1 = ai_data.get('hr_action_1','Review manually')
        a2 = ai_data.get('hr_action_2','Conduct follow-up')
        a3 = ai_data.get('hr_action_3','Monitor employee')

        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #0f3460;border-radius:12px;padding:24px;'>"
            "<div style='font-size:16px;font-weight:700;color:#2ecc71;"
            "margin-bottom:16px;'>✅ Recommended HR Actions</div>"

            "<div style='margin-bottom:16px;padding:12px;"
            "background:rgba(231,76,60,0.1);"
            "border-left:3px solid #e74c3c;border-radius:4px;'>"
            "<div style='font-size:11px;color:#e74c3c;font-weight:700;"
            "text-transform:uppercase;'>Immediate Action</div>"
            f"<div style='color:#e2e8f0;font-size:14px;margin-top:4px;'>"
            f"{a1}</div>"
            "</div>"

            "<div style='margin-bottom:16px;padding:12px;"
            "background:rgba(243,156,18,0.1);"
            "border-left:3px solid #f39c12;border-radius:4px;'>"
            "<div style='font-size:11px;color:#f39c12;font-weight:700;"
            "text-transform:uppercase;'>30-Day Action</div>"
            f"<div style='color:#e2e8f0;font-size:14px;margin-top:4px;'>"
            f"{a2}</div>"
            "</div>"

            "<div style='margin-bottom:16px;padding:12px;"
            "background:rgba(46,204,113,0.1);"
            "border-left:3px solid #2ecc71;border-radius:4px;'>"
            "<div style='font-size:11px;color:#2ecc71;font-weight:700;"
            "text-transform:uppercase;'>90-Day Action</div>"
            f"<div style='color:#e2e8f0;font-size:14px;margin-top:4px;'>"
            f"{a3}</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Row 3 — Sentiment Breakdown
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:16px;'>📊 Sentiment Breakdown</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #2ecc71;border-radius:12px;padding:16px;"
            "text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;'>Positive Content</div>"
            f"<div style='font-size:32px;font-weight:800;color:#2ecc71;'>"
            f"{positive}%</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #e74c3c;border-radius:12px;padding:16px;"
            "text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;'>Negative Content</div>"
            f"<div style='font-size:32px;font-weight:800;color:#e74c3c;'>"
            f"{negative}%</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:1px solid #f39c12;border-radius:12px;padding:16px;"
            "text-align:center;'>"
            "<div style='font-size:11px;color:#a0aec0;'>Neutral Content</div>"
            f"<div style='font-size:32px;font-weight:800;color:#f39c12;'>"
            f"{neutral}%</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Row 4 — Detected Themes
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:16px;'>🎯 Detected Themes</div>",
        unsafe_allow_html=True
    )

    if detected:
        theme_cols = st.columns(len(detected))
        colors     = ['#667eea','#764ba2','#f64f59',
                      '#e74c3c','#2ecc71','#f39c12',
                      '#3498db','#9b59b6']
        for i, (col, theme) in enumerate(
                zip(theme_cols, detected)):
            with col:
                c = colors[i % len(colors)]
                st.markdown(
                    f"<div style='background:rgba(0,0,0,0.2);"
                    f"border:1px solid {c};border-radius:8px;"
                    "padding:12px;text-align:center;'>"
                    f"<div style='color:{c};font-weight:700;'>"
                    f"{theme}</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
    else:
        st.info("No specific themes detected")

elif analyze_btn and not review_text.strip():
    st.warning("⚠️ Please enter a review or exit interview text first")