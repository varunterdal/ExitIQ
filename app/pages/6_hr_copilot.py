import streamlit as st
from groq import Groq
import json
from utils.data_loader import load_all

st.set_page_config(page_title="HR Copilot",
                   page_icon="🤝", layout="wide")
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
# Load data
data      = load_all()
insights  = data['insights']
themes    = data['themes']
risk      = data['risk']
attrition = data['attrition']

# Header
st.markdown(
    "<h1>🤝 HR Copilot</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Ask anything about your workforce data</p>",
    unsafe_allow_html=True
)
st.divider()

# API Key input
api_key = st.text_input(
    "Enter your Groq API Key",
    type="password",
    placeholder="Paste your Groq API key here..."
)

if not api_key:
    st.info("👆 Enter your Groq API key above to start chatting")
    st.stop()

client = Groq(api_key=api_key)

st.success("✅ HR Copilot Ready")
st.divider()

# System context
system_context = f"""
You are ExitIQ HR Copilot, an expert AI HR Analytics assistant.
You have access to real workforce data and provide specific,
data-driven answers to HR questions.

Workforce Data Summary:
- Total reviews analyzed: {insights['total_reviews_analyzed']}
- Attrition rate: {insights['attrition_rate']}%
- Average rating: {insights['avg_overall_rating']}/5
- Positive sentiment: {insights['overall_sentiment']['positive_pct']}%
- Negative sentiment: {insights['overall_sentiment']['negative_pct']}%
- Neutral sentiment: {insights['overall_sentiment']['neutral_pct']}%

Top themes: {json.dumps(insights['top_themes'], indent=2)}
Top attrition drivers: {json.dumps(insights['top_attrition_drivers'], indent=2)}
Risk distribution: {json.dumps(insights['risk_distribution'], indent=2)}
Department attrition: {json.dumps(insights['dept_attrition'], indent=2)}

Always:
- Be specific and reference the actual data
- Give actionable recommendations
- Be concise but thorough
- Format responses clearly with bullet points where needed
- Act as a trusted HR advisor
"""

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Suggested questions
st.subheader("💡 Suggested Questions")
col1, col2, col3 = st.columns(3)

with col1:
    q1 = st.button("What are the top reasons employees leave?",
                   use_container_width=True)
    q2 = st.button("Which department has highest attrition?",
                   use_container_width=True)
with col2:
    q3 = st.button("How can we improve employee sentiment?",
                   use_container_width=True)
    q4 = st.button("What is our biggest retention risk?",
                   use_container_width=True)
with col3:
    q5 = st.button("Give me a 30-day retention action plan",
                   use_container_width=True)
    q6 = st.button("What do employees say most positively?",
                   use_container_width=True)

st.divider()

# Handle suggested question clicks
suggested_question = None
if q1: suggested_question = "What are the top reasons employees leave?"
if q2: suggested_question = "Which department has the highest attrition rate and why?"
if q3: suggested_question = "How can we improve overall employee sentiment?"
if q4: suggested_question = "What is our biggest retention risk right now?"
if q5: suggested_question = "Give me a concrete 30-day retention action plan"
if q6: suggested_question = "What do employees talk about most positively?"

# Chat interface
st.subheader("💬 Chat with HR Copilot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Handle input
user_input = st.chat_input("Ask anything about your workforce...")

if suggested_question:
    user_input = suggested_question

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_context},
                        {"role": "user",   "content": user_input}
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)

                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': reply
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()

if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()