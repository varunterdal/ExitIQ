import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_theme_results
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
st.set_page_config(page_title="Theme Intelligence",
                   page_icon="🎯", layout="wide")
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
# Load data
themes = load_theme_results()

# Header
st.markdown(
    "<h1>🎯 Theme Intelligence</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Discover what employees talk about most</p>",
    unsafe_allow_html=True
)
st.divider()

# Row 1 — Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 Total Themes Detected",
              f"{len(themes)}")
with col2:
    top_theme = themes.iloc[0]['theme']
    st.metric("🏆 Most Common Theme", top_theme)
with col3:
    best_rated = themes.loc[themes['avg_rating'].idxmax(), 'theme']
    st.metric("⭐ Highest Rated Theme", best_rated)

st.divider()

# Row 2 — Main Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Theme Frequency")
    fig1 = px.bar(
        themes.sort_values('count', ascending=True),
        x='count',
        y='theme',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        labels={'count': 'Mentions', 'theme': 'Theme'},
        text='count'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("⭐ Average Rating per Theme")
    fig2 = px.bar(
        themes.sort_values('avg_rating', ascending=True),
        x='avg_rating',
        y='theme',
        orientation='h',
        color='avg_rating',
        color_continuous_scale='RdYlGn',
        labels={'avg_rating': 'Avg Rating', 'theme': 'Theme'},
        text='avg_rating'
    )
    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 3 — Bubble Chart
st.subheader("🔵 Theme Intelligence Map — Frequency vs Rating")
fig3 = px.scatter(
    themes,
    x='count',
    y='avg_rating',
    size='count',
    color='avg_rating',
    text='theme',
    color_continuous_scale='RdYlGn',
    labels={'count': 'Frequency', 'avg_rating': 'Avg Rating'},
    size_max=60
)
fig3.update_traces(textposition='top center')
fig3.update_layout(
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Row 4 — Theme Table
st.subheader("📋 Full Theme Breakdown")
st.dataframe(
    themes.sort_values('count', ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "theme":      st.column_config.TextColumn("Theme"),
        "count":      st.column_config.NumberColumn("Mentions"),
        "avg_rating": st.column_config.ProgressColumn(
            "Avg Rating",
            min_value=0,
            max_value=5,
            format="%.2f"
        )
    }
)