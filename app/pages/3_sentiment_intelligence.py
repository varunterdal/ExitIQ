import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_sentiment_results

st.set_page_config(page_title="Sentiment Intelligence",
                   page_icon="💬", layout="wide")
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
# Load data
sentiment = load_sentiment_results()

# Header
st.markdown(
    "<h1>💬 Sentiment Intelligence</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Sentiment Intelligence analyzes employee feedback to measure overall workforce sentiment. It uncovers emotional trends, identifies areas of concern, and provides a clear understanding of employee perceptions across the organization.</p>",
    unsafe_allow_html=True
)
st.divider()

# Row 1 — Metrics
total = len(sentiment)
positive = (sentiment['overall_sentiment'] == 'Positive').sum()
negative = (sentiment['overall_sentiment'] == 'Negative').sum()
neutral  = (sentiment['overall_sentiment'] == 'Neutral').sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📝 Total Reviews", f"{total:,}")
with col2:
    st.metric("😊 Positive",
              f"{positive:,}",
              f"{round(positive/total*100,1)}%")
with col3:
    st.metric("😞 Negative",
              f"{negative:,}",
              f"{round(negative/total*100,1)}%")
with col4:
    st.metric("😐 Neutral",
              f"{neutral:,}",
              f"{round(neutral/total*100,1)}%")

st.divider()

# Row 2 — Pie + Bar
col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Overall Sentiment Distribution")
    sentiment_counts = sentiment['overall_sentiment'].value_counts()
    fig1 = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        color=sentiment_counts.index,
        color_discrete_map={
            'Positive': '#2ecc71',
            'Negative': '#e74c3c',
            'Neutral':  '#f39c12'
        },
        hole=0.4
    )
    fig1.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("👍 Pros vs Cons Sentiment")
    pros_counts = sentiment['pros_sentiment'].value_counts()
    cons_counts = sentiment['cons_sentiment'].value_counts()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name='Pros',
        x=pros_counts.index,
        y=pros_counts.values,
        marker_color=['#2ecc71','#e74c3c','#f39c12']
    ))
    fig2.add_trace(go.Bar(
        name='Cons',
        x=cons_counts.index,
        y=cons_counts.values,
        marker_color=['#27ae60','#c0392b','#e67e22'],
        opacity=0.7
    ))
    fig2.update_layout(
        barmode='group',
        height=380,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 3 — Sentiment Score Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Pros Sentiment Score Distribution")
    fig3 = px.histogram(
        sentiment,
        x='pros_sentiment_score',
        nbins=50,
        color_discrete_sequence=['#2ecc71'],
        labels={'pros_sentiment_score': 'Sentiment Score'}
    )
    fig3.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📉 Cons Sentiment Score Distribution")
    fig4 = px.histogram(
        sentiment,
        x='cons_sentiment_score',
        nbins=50,
        color_discrete_sequence=['#e74c3c'],
        labels={'cons_sentiment_score': 'Sentiment Score'}
    )
    fig4.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Row 4 — Sentiment vs Rating
st.subheader("⭐ Sentiment vs Overall Rating")
fig5 = px.box(
    sentiment,
    x='overall_sentiment',
    y='overall_rating',
    color='overall_sentiment',
    color_discrete_map={
        'Positive': '#2ecc71',
        'Negative': '#e74c3c',
        'Neutral':  '#f39c12'
    },
    labels={
        'overall_sentiment': 'Sentiment',
        'overall_rating': 'Overall Rating'
    }
)
fig5.update_layout(
    height=400,
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# Row 5 — Raw Data Table
st.subheader("📋 Sentiment Data Sample")
st.dataframe(
    sentiment.head(100),
    use_container_width=True,
    hide_index=True,
    column_config={
        "overall_sentiment":    st.column_config.TextColumn("Overall"),
        "pros_sentiment":       st.column_config.TextColumn("Pros"),
        "cons_sentiment":       st.column_config.TextColumn("Cons"),
        "pros_sentiment_score": st.column_config.NumberColumn(
            "Pros Score", format="%.3f"),
        "cons_sentiment_score": st.column_config.NumberColumn(
            "Cons Score", format="%.3f"),
        "overall_rating":       st.column_config.NumberColumn("Rating")
    }
)