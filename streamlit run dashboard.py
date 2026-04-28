import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from ai_sql_constructor import query_database_with_ai

# UI Configuration
st.set_page_config(page_title="Lumentum HR Command Center", layout="wide", initial_sidebar_state="expanded")
st.title("Proactive Workforce & AI Command Center")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Predictive Analytics", "🤖 NL-to-SQL Assistant"])

# TAB 1: Beautiful Descriptive & Predictive Analytics
with tab1:
    conn = sqlite3.connect('hr_enterprise.db')
    df = pd.read_sql_query("SELECT * FROM workforce_predictions", conn)
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Workforce", f"{len(df):,}")
    col2.metric("High Flight Risk", f"{len(df[df['Risk_Level'] == 'High Risk']):,}")
    col3.metric("Avg Manufacturing Tenure", f"{df[df['Department'] == 'Manufacturing']['Tenure_Months'].mean():.1f} Mos")
    col4.metric("Avg Salary", f"${df['Base_Salary'].mean():,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Plotly Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Flight Risk Distribution")
        # A beautiful donut chart with custom enterprise colors
        fig_pie = px.pie(df, names='Risk_Level', color='Risk_Level', 
                         color_discrete_map={'High Risk':'#EF553B', 'Medium Risk':'#FFA15A', 'Low Risk':'#00CC96'},
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_col2:
        st.subheader("High Risk by Department")
        # An interactive bar chart
        high_risk_df = df[df['Risk_Level'] == 'High Risk']
        fig_bar = px.histogram(high_risk_df, x='Department', color='Department', 
                               text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_bar.update_layout(showlegend=False, xaxis_title="", yaxis_title="Employee Count")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Targeted Retention Interventions")
    # Adds a heatmap gradient to the probability column
    styled_df = df[df['Risk_Level'] == 'High Risk'].sort_values(by='Flight_Risk_Probability', ascending=False)
    st.dataframe(styled_df.style.background_gradient(cmap='Reds', subset=['Flight_Risk_Probability']), use_container_width=True)
    
    conn.close()

# TAB 2: The Enterprise AI Agent
with tab2:
    st.header("Ask your Data Lake in Plain English")
    st.markdown("Translate natural language questions directly into SQL queries against the nightly predictive database.")
    
    user_question = st.text_input("Ask a question:", placeholder="e.g., What is the average salary of High Risk employees in Manufacturing?")
    
    if st.button("Generate SQL & Run"):
        if user_question:
            with st.spinner("AI is constructing the SQL query..."):
                sql_query, result = query_database_with_ai(user_question)
                
                if sql_query:
                    st.success("Query Executed Successfully!")
                    st.code(sql_query, language='sql') 
                    st.write("**Database Result:**")
                    st.write(result)
                else:
                    st.error(result)