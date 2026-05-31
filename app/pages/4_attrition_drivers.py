import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_attrition_results, load_risk_results, load_executive_insights

st.set_page_config(page_title="Attrition Driver Intelligence",
                   page_icon="⚠️", layout="wide")
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)
# Load data
attrition = load_attrition_results()
risk      = load_risk_results()
insights  = load_executive_insights()

# Header
st.markdown(
    "<h1>⚠️ Attrition Driver Intelligence</h1>"
    "<p style='color:#a0aec0;margin-top:-16px;'>"
    "Attrition Drivers identifies the key factors contributing to employee turnover. It helps HR teams understand the root causes behind employee exits and prioritize initiatives that improve retention and workforce stability.</p>",
    unsafe_allow_html=True
)
st.divider()

# Row 1 — Metrics
col1, col2, col3, col4 = st.columns(4)

total       = len(risk)
high_risk   = (risk['risk_level'] == 'High Risk').sum()
medium_risk = (risk['risk_level'] == 'Medium Risk').sum()
low_risk    = (risk['risk_level'] == 'Low Risk').sum()

with col1:
    st.metric("👥 Total Employees", f"{total:,}")
with col2:
    st.metric("🔴 High Risk",
              f"{high_risk}",
              f"{round(high_risk/total*100,1)}%")
with col3:
    st.metric("🟡 Medium Risk",
              f"{medium_risk}",
              f"{round(medium_risk/total*100,1)}%")
with col4:
    st.metric("🟢 Low Risk",
              f"{low_risk}",
              f"{round(low_risk/total*100,1)}%")

st.divider()

# Row 2 — Top Drivers + Department Attrition
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Top Attrition Drivers")
    fig1 = px.bar(
        attrition.head(10),
        x='importance',
        y='feature',
        orientation='h',
        color='importance',
        color_continuous_scale='Reds',
        labels={'importance': 'Importance Score',
                'feature': 'Factor'},
        text=attrition.head(10)['importance'].apply(
            lambda x: f"{x:.3f}")
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏢 Attrition Rate by Department")
    dept_df = pd.DataFrame(insights['dept_attrition'])
    fig2 = px.bar(
        dept_df,
        x='department',
        y='attrition_rate',
        color='attrition_rate',
        color_continuous_scale='Reds',
        labels={'attrition_rate': 'Attrition %',
                'department': 'Department'},
        text='attrition_rate'
    )
    fig2.update_traces(texttemplate='%{text}%',
                       textposition='outside')
    fig2.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 3 — Risk Distribution + Overtime Impact
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚨 Risk Level Distribution")
    risk_counts = risk['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level', 'count']
    fig3 = px.pie(
        risk_counts,
        values='count',
        names='risk_level',
        color='risk_level',
        color_discrete_map={
            'High Risk':   '#e74c3c',
            'Medium Risk': '#f39c12',
            'Low Risk':    '#2ecc71'
        },
        hole=0.4
    )
    fig3.update_layout(
        height=380,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("⏰ Overtime Impact on Attrition")
    overtime_attrition = risk.groupby('OverTime')['Attrition'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100
    ).reset_index()
    overtime_attrition.columns = ['OverTime', 'Attrition Rate %']
    fig4 = px.bar(
        overtime_attrition,
        x='OverTime',
        y='Attrition Rate %',
        color='OverTime',
        color_discrete_map={
            'Yes': '#e74c3c',
            'No':  '#2ecc71'
        },
        labels={'OverTime': 'Works Overtime'},
        text='Attrition Rate %'
    )
    fig4.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig4.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Row 4 — Income vs Attrition + Job Role Attrition
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Monthly Income vs Attrition")
    fig5 = px.box(
        risk,
        x='Attrition',
        y='MonthlyIncome',
        color='Attrition',
        color_discrete_map={
            'Yes': '#e74c3c',
            'No':  '#2ecc71'
        },
        labels={'MonthlyIncome': 'Monthly Income ($)'}
    )
    fig5.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("👔 Attrition by Job Role")
    role_attrition = risk.groupby('JobRole')['Attrition'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100
    ).reset_index()
    role_attrition.columns = ['JobRole', 'Attrition Rate %']
    role_attrition = role_attrition.sort_values(
        'Attrition Rate %', ascending=True)
    fig6 = px.bar(
        role_attrition,
        x='Attrition Rate %',
        y='JobRole',
        orientation='h',
        color='Attrition Rate %',
        color_continuous_scale='Reds',
        text='Attrition Rate %'
    )
    fig6.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig6.update_layout(
        height=380,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# Row 5 — Risk Table
st.subheader("📋 Employee Risk Register")
st.dataframe(
    risk[['Department','JobRole','Age','MonthlyIncome',
          'JobSatisfaction','OverTime','WorkLifeBalance',
          'risk_score','risk_level','Attrition']
    ].sort_values('risk_score', ascending=False).head(50),
    use_container_width=True,
    hide_index=True,
    column_config={
        "risk_level": st.column_config.TextColumn("Risk Level"),
        "risk_score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100,
            format="%d"
        ),
        "MonthlyIncome": st.column_config.NumberColumn(
            "Monthly Income",
            format="$%d"
        )
    }
)