import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# 1. Base Demographics
num_employees = 5000
departments = ['Manufacturing', 'Engineering', 'Sales']
# Lumentum is highly skewed toward manufacturing headcount
dept_weights = [0.6, 0.25, 0.15] 

data = {
    'Emp_ID': range(1000, 1000 + num_employees),
    'Department': np.random.choice(departments, num_employees, p=dept_weights),
    'Tenure_Months': np.random.randint(1, 60, num_employees),
    'Base_Salary': np.random.randint(60000, 150000, num_employees)
}
df = pd.DataFrame(data)

# 2. Inject Lumentum's Business Reality (Meg's Layer)
# If Manufacturing and Tenure < 6 months, 70% chance of quitting. Otherwise, 10%.
def determine_turnover(row):
    if row['Department'] == 'Manufacturing' and row['Tenure_Months'] < 6:
        return np.random.choice(['Yes', 'No'], p=[0.7, 0.3]) 
    else:
        return np.random.choice(['Yes', 'No'], p=[0.1, 0.9])

df['Voluntary_Turnover'] = df.apply(determine_turnover, axis=1)

# 3. Add Unstructured Data (For Prathana's RAG pipeline)
exit_notes = [
    "The hiring volume is insane, we don't have enough trainers.",
    "Great team, but the manufacturing shifts are too long.",
    "I wasn't properly trained on the new optical switch assembly line.",
    "Burnout. We are hiring 500 people a week but the floor is chaos."
]
# Only assign exit notes if the person actually quit
df['Exit_Interview'] = np.where(df['Voluntary_Turnover'] == 'Yes', 
                                np.random.choice(exit_notes, num_employees), 
                                "N/A - Active Employee")

# Save to CSV
df.to_csv('lumentum_synthetic_hr.csv', index=False)
print("File 1 Complete: Lumentum Enterprise Data Generated.")