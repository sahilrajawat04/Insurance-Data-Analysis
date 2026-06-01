import pandas as pd
from datetime import datetime

# Relative paths for GitHub compatibility
claim = pd.read_csv('claims.csv')
customer = pd.read_csv('cust_demographics.csv')
audit = pd.read_csv('DataAudit.csv')

merge = pd.merge(left=claim, right=customer, left_on='customer_id', right_on='CUST_ID', how='inner')
print("Columns in dataset:", merge.columns)

# Global Data Cleaning
merge['claim_amount'] = merge['claim_amount'].str.replace('$', '', regex=False).astype(float)
merge['DateOfBirth'] = pd.to_datetime(merge['DateOfBirth'])
merge['claim_date'] = pd.to_datetime(merge['claim_date'])

# #q3
print("\n--- Q3: Claims Overview ---")
print(merge[['claim_id', 'claim_amount']])

# #q4
merge['alert_flag'] = [1 if x == 0 else 0 for x in merge['police_report']]

# #q5
print("\n--- Q5: Unique Customers ---")
print(merge[~merge.customer_id.duplicated(keep='last')])

# #q6 & q7
t = datetime.today()
merge['Age'] = (t - merge['DateOfBirth']).dt.days // 365
merge['Age_group'] = ['Children' if age < 18 else 'Youth' if age >= 18 and age < 30 else 'Adult' if age >= 30 and age < 60 else 'Senior' for age in merge['Age']] 
print("\n--- Q7: Age Group Head ---")
print(merge['Age_group'].head(10))

# #q8
print("\n--- Q8: Average Claim by Segment ---")
s = merge.groupby('Segment')['claim_amount'].mean()
print(s)

# #q9
print("\n--- Q9: Claims before 2018-09-11 by Incident Cause ---")
r = merge[merge['claim_date'] <= '2018-09-11'].groupby('incident_cause')['claim_amount'].sum()
print(r)

# #q10
print("\n--- Q10: Total Count for Target Adults ---")
c = ((merge['State'].isin(['TX', 'DE', 'AK'])) &
     (merge['incident_cause'].str.contains('Driver', case=False, na=False)) &
     (merge['Age_group'] == 'Adult')).sum()
print(c)