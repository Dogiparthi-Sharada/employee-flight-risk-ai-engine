# Lumentum HR AI System

An AI-powered workforce analytics platform combining predictive modeling, natural language querying, and interactive visualization for proactive HR management.

## 🚀 Quick Start
See [QUICKSTART.md](QUICKSTART.md) for detailed setup and execution instructions.

## 🏗️ Architecture
See [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) for technical design rationale and architecture decisions.

## 📊 Features

### Predictive Analytics
- Machine learning model predicting employee turnover risk
- Risk categorization (High/Medium/Low) with probability scores
- Interactive dashboards with KPIs and visualizations

### Natural Language to SQL
- AI-powered query generation from plain English questions
- Direct database execution with results display
- Context-aware SQL construction using LangChain

### RAG-Enhanced Insights
- Vector database of exit interview text
- Semantic search for qualitative insights
- Integration with predictive analytics

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-3.5-turbo, LangChain, scikit-learn, FAISS
- **Data**: SQLite, pandas, numpy
- **Visualization**: Plotly

## 📁 Project Structure
```
├── data_generator.py          # Synthetic HR data generation
├── predictive_engine.py       # ML turnover prediction model
├── rag_engine.py             # Vector database for exit interviews
├── ai_sql_constructor.py     # NL-to-SQL AI agent
├── dashboard.py              # Streamlit web application
├── requirements.txt          # Python dependencies
├── QUICKSTART.md             # Setup and usage guide
├── DESIGN_DECISIONS.md       # Technical design documentation
├── doc/                      # Visual documentation and diagrams
├── lumentum_synthetic_hr.csv # Generated employee data
├── hr_enterprise.db          # SQLite database
├── faiss_hr_index/           # FAISS vector database
├── .env                      # API keys (configure with OpenAI key)
└── lumentum_env/             # Python virtual environment
```

## 🎯 Use Cases
- **HR Analytics**: Workforce planning and retention strategies
- **Risk Assessment**: Identify at-risk employees for intervention
- **Data Democratization**: Enable non-technical users to query HR data
- **Qualitative Insights**: Analyze exit interview patterns

## 📈 Sample Queries
- "How many employees are in the Manufacturing department?"
- "What is the average salary of High Risk employees?"
- "Show me turnover rates by department"

The system is designed for easy deployment and can be adapted for real HR data sources.