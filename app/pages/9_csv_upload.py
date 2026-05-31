import streamlit as st
import pandas as pd
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.styles import load_css

st.set_page_config(page_title="CSV Upload & Analysis",
                   page_icon="📁", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

analyzer = SentimentIntensityAnalyzer()

st.markdown(
    "<h1>📁 CSV Upload & Analysis</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Upload your own employee data and analyze it instantly</p>",
    unsafe_allow_html=True
)
st.divider()

# ── What CSV format is needed
with st.expander("📋 What should my CSV look like?", expanded=False):
    st.markdown(
        "<div style='color:#a0aec0;font-size:14px;'>"
        "Your CSV needs at least <b style='color:#e2e8f0;'>one text column</b> "
        "with employee reviews or feedback.<br><br>"
        "Supported column names (any of these work):<br>"
        "<code>review</code>, <code>review_text</code>, <code>feedback</code>, "
        "<code>comments</code>, <code>text</code>, <code>exit_interview</code>"
        "<br><br>"
        "Optional columns for richer analysis:<br>"
        "<code>department</code>, <code>rating</code>, <code>employee_id</code>, "
        "<code>date</code>, <code>tenure</code>"
        "</div>",
        unsafe_allow_html=True
    )
    # Show sample
    sample_df = pd.DataFrame({
        'employee_id': ['E001', 'E002', 'E003'],
        'department':  ['Engineering', 'Sales', 'HR'],
        'rating':      [2, 4, 3],
        'review_text': [
            'Management is toxic and pay is below market rate.',
            'Great culture and work life balance. Love the team.',
            'Mixed experience. Good work but limited growth.'
        ]
    })
    st.dataframe(sample_df, use_container_width=True)

st.divider()

# ── Upload
st.markdown(
    "<div style='font-size:18px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:8px;'>⬆️ Upload Your CSV</div>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Drop your CSV file here",
    type=['csv'],
    help="Max file size: 200MB"
)

if uploaded_file is None:
    st.info("👆 Upload a CSV file to begin analysis")
    st.stop()

# ── Load CSV
try:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ File loaded: {len(df):,} rows, {len(df.columns)} columns")
except Exception as e:
    st.error(f"❌ Could not read file: {str(e)}")
    st.stop()

# ── Preview
with st.expander("👀 Preview uploaded data", expanded=True):
    st.dataframe(df.head(10), use_container_width=True)
    st.caption(f"Showing first 10 of {len(df):,} rows")

st.divider()

# ── Detect text column
text_col_candidates = [
    'review', 'review_text', 'feedback',
    'comments', 'text', 'exit_interview',
    'employee_review', 'survey_response'
]

detected_col = None
for col in text_col_candidates:
    if col in df.columns:
        detected_col = col
        break

# Let user pick if not auto-detected
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:8px;'>⚙️ Configure Analysis</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    text_column = st.selectbox(
        "Select the text/review column",
        options=df.columns.tolist(),
        index=df.columns.tolist().index(detected_col)
              if detected_col else 0,
        help="This column contains the employee reviews or feedback"
    )
    if detected_col:
        st.caption(f"✅ Auto-detected: '{detected_col}'")

with col2:
    dept_candidates = ['department', 'dept', 'team', 'division']
    dept_col = None
    for c in dept_candidates:
        if c in df.columns:
            dept_col = c
            break

    dept_column = st.selectbox(
        "Select department column (optional)",
        options=['None'] + df.columns.tolist(),
        index=df.columns.tolist().index(dept_col) + 1
              if dept_col else 0,
        help="Used for department-level breakdowns"
    )

analyze_btn = st.button(
    "🔍 Analyze This Dataset",
    use_container_width=True
)

if not analyze_btn:
    st.stop()

# ── Run Analysis
st.divider()
st.markdown(
    "<div style='font-size:18px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:16px;'>📊 Analysis Results</div>",
    unsafe_allow_html=True
)

progress = st.progress(0, text="Starting analysis...")

# Step 1 — Sentiment
progress.progress(20, text="Running sentiment analysis...")

def get_sentiment(text):
    try:
        score = analyzer.polarity_scores(str(text))['compound']
        if score >= 0.05:   return 'Positive', score
        elif score <= -0.05: return 'Negative', score
        else:                return 'Neutral',  score
    except:
        return 'Neutral', 0.0

df['_sentiment'], df['_score'] = zip(*df[text_column].apply(get_sentiment))

progress.progress(50, text="Detecting themes...")

# Step 2 — Theme Detection
themes_map = {
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

def detect_themes(text):
    text_lower = str(text).lower()
    found = []
    for theme, keywords in themes_map.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(theme)
                break
    return found[0] if found else 'General'

df['_primary_theme'] = df[text_column].apply(detect_themes)

progress.progress(75, text="Calculating risk scores...")

# Step 3 — Risk Score
def calc_risk(row):
    score = 50
    s = row['_score']
    if s <= -0.05: score += 20
    if s <= -0.3:  score += 10
    t = row['_primary_theme']
    if t == 'Management':   score += 10
    if t == 'Compensation': score += 10
    if t == 'Workload':     score += 5
    if s >= 0.05:           score -= 20
    return max(0, min(100, score))

df['_risk_score'] = df.apply(calc_risk, axis=1)

def risk_label(s):
    if s >= 70: return 'High Risk'
    elif s >= 40: return 'Medium Risk'
    else: return 'Low Risk'

df['_risk_level'] = df['_risk_score'].apply(risk_label)

progress.progress(100, text="✅ Analysis complete!")
progress.empty()

# ── KPI Cards
total       = len(df)
positive_n  = (df['_sentiment'] == 'Positive').sum()
negative_n  = (df['_sentiment'] == 'Negative').sum()
neutral_n   = (df['_sentiment'] == 'Neutral').sum()
high_risk_n = (df['_risk_level'] == 'High Risk').sum()
avg_score   = round(df['_score'].mean(), 3)

pos_pct  = round(positive_n / total * 100, 1)
neg_pct  = round(negative_n / total * 100, 1)
risk_pct = round(high_risk_n / total * 100, 1)

# Health Score
if pos_pct >= 60:   health = int(60 + (pos_pct - 60) * 0.5)
elif pos_pct >= 40: health = int(40 + (pos_pct - 40) * 1.0)
else:               health = int(pos_pct * 0.8)
health = max(0, min(100, health))

if health >= 80:
    h_color, h_label = "#2ecc71", "Healthy"
elif health >= 60:
    h_color, h_label = "#f39c12", "At Risk"
elif health >= 40:
    h_color, h_label = "#e67e22", "Concerning"
else:
    h_color, h_label = "#e74c3c", "Critical"

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        f"border:2px solid {h_color};border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Health Score</div>"
        f"<div style='font-size:36px;font-weight:900;color:{h_color};'>"
        f"{health}</div>"
        f"<div style='font-size:11px;color:{h_color};'>{h_label}</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #667eea;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Total Reviews</div>"
        f"<div style='font-size:36px;font-weight:900;color:#667eea;'>"
        f"{total:,}</div>"
        "<div style='font-size:11px;color:#a0aec0;'>Analyzed</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #2ecc71;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Positive</div>"
        f"<div style='font-size:36px;font-weight:900;color:#2ecc71;'>"
        f"{pos_pct}%</div>"
        f"<div style='font-size:11px;color:#a0aec0;'>{positive_n:,} reviews</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #e74c3c;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Negative</div>"
        f"<div style='font-size:36px;font-weight:900;color:#e74c3c;'>"
        f"{neg_pct}%</div>"
        f"<div style='font-size:11px;color:#a0aec0;'>{negative_n:,} reviews</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #f39c12;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>High Risk</div>"
        f"<div style='font-size:36px;font-weight:900;color:#f39c12;'>"
        f"{risk_pct}%</div>"
        f"<div style='font-size:11px;color:#a0aec0;'>{high_risk_n:,} employees</div>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Confidence Score Panel
total_words = df[text_column].apply(lambda x: len(str(x).split())).sum()
avg_words   = round(total_words / total, 1)
coverage    = min(100, round((total / 1000) * 100, 1))
confidence  = min(98, round((coverage * 0.4) + (min(avg_words, 50) / 50 * 40) + 18, 1))

st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:12px;'>🎯 Analysis Confidence & Coverage</div>",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    c_color = "#2ecc71" if confidence >= 75 else "#f39c12" if confidence >= 50 else "#e74c3c"
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        f"border:1px solid {c_color};border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Confidence Score</div>"
        f"<div style='font-size:32px;font-weight:800;color:{c_color};'>"
        f"{confidence}%</div>"
        "<div style='font-size:11px;color:#a0aec0;'>Analysis reliability</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #3498db;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Data Coverage</div>"
        f"<div style='font-size:32px;font-weight:800;color:#3498db;'>"
        f"{coverage}%</div>"
        "<div style='font-size:11px;color:#a0aec0;'>vs 1,000 review baseline</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #9b59b6;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Avg Review Length</div>"
        f"<div style='font-size:32px;font-weight:800;color:#9b59b6;'>"
        f"{avg_words}</div>"
        "<div style='font-size:11px;color:#a0aec0;'>words per review</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        "border:1px solid #2ecc71;border-radius:12px;padding:16px;"
        "text-align:center;'>"
        "<div style='font-size:11px;color:#a0aec0;text-transform:uppercase;"
        "letter-spacing:2px;'>Total Words</div>"
        f"<div style='font-size:32px;font-weight:800;color:#2ecc71;'>"
        f"{total_words:,}</div>"
        "<div style='font-size:11px;color:#a0aec0;'>analyzed by AI</div>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Theme Breakdown
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:12px;'>🎯 Theme Breakdown</div>",
    unsafe_allow_html=True
)

theme_counts = df['_primary_theme'].value_counts().reset_index()
theme_counts.columns = ['theme', 'count']
theme_counts['pct'] = (theme_counts['count'] / total * 100).round(1)

colors = ['#667eea','#764ba2','#f64f59','#e74c3c',
          '#2ecc71','#f39c12','#3498db','#9b59b6']

for i, row in theme_counts.iterrows():
    c = colors[i % len(colors)]
    bar_width = int(row['pct'] * 4)
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
        f"border:1px solid {c};border-radius:8px;padding:12px 16px;"
        "margin-bottom:8px;display:flex;align-items:center;"
        "justify-content:space-between;'>"
        f"<span style='color:#e2e8f0;font-weight:600;min-width:160px;'>"
        f"{row['theme']}</span>"
        "<div style='flex:1;margin:0 16px;"
        "background:rgba(255,255,255,0.05);border-radius:4px;height:8px;'>"
        f"<div style='background:{c};width:{bar_width}px;max-width:100%;"
        "height:8px;border-radius:4px;'></div>"
        "</div>"
        f"<span style='color:{c};font-weight:700;min-width:80px;"
        f"text-align:right;'>{row['count']} ({row['pct']}%)</span>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ── Department Breakdown (if available)
if dept_column != 'None' and dept_column in df.columns:
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
        "margin-bottom:12px;'>🏢 Department Breakdown</div>",
        unsafe_allow_html=True
    )
    dept_summary = df.groupby(dept_column).agg(
        total    = (text_column, 'count'),
        positive = ('_sentiment', lambda x: (x == 'Positive').sum()),
        negative = ('_sentiment', lambda x: (x == 'Negative').sum()),
        high_risk= ('_risk_level', lambda x: (x == 'High Risk').sum()),
        avg_score= ('_score', 'mean')
    ).reset_index()
    dept_summary['pos_pct']  = (dept_summary['positive'] / dept_summary['total'] * 100).round(1)
    dept_summary['risk_pct'] = (dept_summary['high_risk'] / dept_summary['total'] * 100).round(1)
    dept_summary = dept_summary.sort_values('risk_pct', ascending=False)

    for _, row in dept_summary.iterrows():
        r_color = ("#e74c3c" if row['risk_pct'] >= 40
                   else "#f39c12" if row['risk_pct'] >= 20
                   else "#2ecc71")
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            f"border-left:4px solid {r_color};border-radius:8px;"
            "padding:16px;margin-bottom:8px;'>"
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;'>"
            f"<span style='color:#e2e8f0;font-weight:700;font-size:15px;'>"
            f"🏢 {row[dept_column]}</span>"
            f"<span style='color:{r_color};font-weight:700;'>"
            f"{row['risk_pct']}% High Risk</span>"
            "</div>"
            "<div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;"
            "gap:12px;margin-top:10px;'>"
            f"<div><div style='font-size:11px;color:#a0aec0;'>Total</div>"
            f"<div style='color:#e2e8f0;font-weight:600;'>{int(row['total'])}</div></div>"
            f"<div><div style='font-size:11px;color:#a0aec0;'>Positive</div>"
            f"<div style='color:#2ecc71;font-weight:600;'>{row['pos_pct']}%</div></div>"
            f"<div><div style='font-size:11px;color:#a0aec0;'>Negative</div>"
            f"<div style='color:#e74c3c;font-weight:600;'>"
            f"{round(row['negative']/row['total']*100,1)}%</div></div>"
            f"<div><div style='font-size:11px;color:#a0aec0;'>Avg Sentiment</div>"
            f"<div style='color:#667eea;font-weight:600;'>"
            f"{round(row['avg_score'],3)}</div></div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )
    st.divider()

# ── Full Results Table
with st.expander("📋 View Full Analyzed Dataset", expanded=False):
    display_cols = [text_column, '_sentiment', '_score',
                    '_primary_theme', '_risk_level', '_risk_score']
    if dept_column != 'None' and dept_column in df.columns:
        display_cols = [dept_column] + display_cols
    st.dataframe(
        df[display_cols].rename(columns={
            text_column:      'Review',
            '_sentiment':     'Sentiment',
            '_score':         'Score',
            '_primary_theme': 'Primary Theme',
            '_risk_level':    'Risk Level',
            '_risk_score':    'Risk Score',
            dept_column:      'Department'
        }),
        use_container_width=True
    )

# ── Download
st.divider()
st.markdown(
    "<div style='font-size:16px;font-weight:700;color:#e2e8f0;"
    "margin-bottom:12px;'>⬇️ Download Results</div>",
    unsafe_allow_html=True
)

csv_out = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Full Analysis as CSV",
    data=csv_out,
    file_name="exitiq_analysis_results.csv",
    mime="text/csv",
    use_container_width=True
)