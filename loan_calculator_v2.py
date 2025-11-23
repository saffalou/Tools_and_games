import pandas as pd
import numpy as np

# Input from user
principle = int(
    input("How much would you like to borrow (in whole dollars)? "))
annual_interest_rate = float(
    input("What is the interest rate being applied to this loan? ")) / 100
loan_period_years = int(
    input("How long, in whole years, is the loan period? "))

# Convert annual interest rate to monthly and calculate total number of payments
monthly_interest_rate = annual_interest_rate / 12
total_payments = loan_period_years * 12

# Correct formula for monthly loan repayment
monthly_repayment = principle * monthly_interest_rate * \
    (1 + monthly_interest_rate) ** total_payments / \
    ((1 + monthly_interest_rate) ** total_payments - 1)
monthly_repayment_rounded = round(monthly_repayment, 2)

# Calculate loan balance over time
loan_balance = []
beginning_loan_balance = []

for month in range(1, total_payments + 1):
    if month == 1:
        balance = principle * (1 + monthly_interest_rate) - monthly_repayment
        beginning_loan_balance.append(principle)
    else:
        balance = loan_balance[month - 2] * \
            (1 + monthly_interest_rate) - monthly_repayment
        beginning_loan_balance.append(loan_balance[month - 2])

    loan_balance.append(round(balance, 2))  # Round balance to 2 decimal places

# Create DataFrame
period = [month for month in range(1, total_payments + 1)]
data = {
    'Period': period,
    'Beginning_loan_balance': beginning_loan_balance,
    'End_balance_amount': loan_balance,
    'Monthly_repayment': monthly_repayment_rounded
}

df = pd.DataFrame(data)
df['Interest'] = df['Beginning_loan_balance'] * monthly_interest_rate
total_interest = df['Interest'].sum()
total_amount_due = principle + total_interest

# Calculate total amount due over time
total = []
for month in period:
    if month == 1:
        amount = float(total_amount_due)
    else:
        amount = float(total[month - 2] - monthly_repayment)

    total.append(round(amount, 2))  # Round total to 2 decimal places

df['Total'] = total

# Output results
print("\nMonthly Loan Repayment (principle + interest):",
      monthly_repayment_rounded, "\n")
print(df)
