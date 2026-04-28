import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

print("Loading data for predictive modeling...")
df = pd.read_csv('lumentum_synthetic_hr.csv')

# 1. Feature Engineering (Prepping data for the ML model)
df['Dept_Code'] = df['Department'].astype('category').cat.codes
df['Target'] = df['Voluntary_Turnover'].apply(lambda x: 1 if x == 'Yes' else 0)

X = df[['Tenure_Months', 'Base_Salary', 'Dept_Code']]
y = df['Target']

# 2. Handle Imbalanced Turnover Data using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# 3. Train the Model & Predict 
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_resampled, y_resampled)

# Score every employee's probability of leaving
df['Flight_Risk_Probability'] = rf_model.predict_proba(X)[:, 1] 

def categorize_risk(prob):
    if prob > 0.75: return 'High Risk'
    elif prob > 0.40: return 'Medium Risk'
    else: return 'Low Risk'

df['Risk_Level'] = df['Flight_Risk_Probability'].apply(categorize_risk)

# 4. Push to SQLite Database (The "Processed Data Lake")
# This is critical. NL-to-SQL AI models need a SQL database, not a CSV.
conn = sqlite3.connect('hr_enterprise.db')
df.to_sql('workforce_predictions', conn, if_exists='replace', index=False)
conn.close()

print("File 2 Complete: Predictive engine ran and SQLite database updated.")