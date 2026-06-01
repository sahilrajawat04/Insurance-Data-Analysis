import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

claim = pd.read_csv('claims.csv')
customer = pd.read_csv('cust_demographics.csv')

merge = pd.merge(left=claim, right=customer, left_on='customer_id', right_on='CUST_ID', how='inner')

#Global Data Cleaning
merge['claim_amount'] = merge['claim_amount'].str.replace('$', '', regex=False).astype(float)
merge['DateOfBirth'] = pd.to_datetime(merge['DateOfBirth'])
merge['claim_date'] = pd.to_datetime(merge['claim_date'])

#12 Driver Incidents Bar Chart
print("\n--- Q12: Driver Incidents Analysis ---")
l = merge[merge['incident_cause'].str.contains('driver', case=False)].copy()
sum_driver = l.groupby('gender')['claim_amount'].sum()
print(sum_driver)

sum_driver.plot(kind='bar')
plt.title('Total Claim Amount by Gender (Driver Incidents)')
plt.xlabel('Gender')
plt.ylabel('Claim Amount')
plt.show()

#13 Fraud by Age Bar Chart
t = datetime.today()
merge['Age'] = (t - merge['DateOfBirth']).dt.days // 365
frd = merge[merge['fraudulent'] == 'Yes']
x = frd.groupby('Age').size()

x.plot(kind='bar')
plt.title('Fraudulent Claims by Age')
plt.xlabel('Age')
plt.ylabel('Number of Fraud Cases')
plt.show()

#q14 Pivot Table
merge['month'] = merge['claim_date'].dt.month
pivot_summary = pd.pivot_table(
    merge, 
    values='claim_amount', 
    index='month', 
    aggfunc=['sum', 'count']
)
print("\n--- Q14: Monthly Claims Pivot Table ---")
print(pivot_summary)

# Bonus Segment Pie Chart
chart_data = merge.groupby(['gender', 'Segment'])['claim_amount'].sum()
plt.pie(chart_data.values, labels=chart_data.index, autopct='%1.1f%%')
plt.title('Total Claim Amount by Gender and Segment')
plt.show()