import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


principal = int(
    input("How much would you like to borrow (in whole dollars)? "))

interest_rate = float(
    input("What is the interest rate being applied to this loan? ")) / 100

loan_period = int(input("How long, in whole years, is the loan period? "))

compounding_periods_per_year = int(
    input("Is the interest compounded (A)nually, (Q)uarterly or (M)onthly? "))

total_periods_in_loan = float(compounding_periods_per_year * loan_period)

# Correct formula for monthly loan repayment
monthly_interest_rate = interest_rate / compounding_periods_per_year
monthly_loan_repayment = principal * (monthly_interest_rate * (1 + monthly_interest_rate)
                                      ** total_periods_in_loan) / ((1 + monthly_interest_rate) ** total_periods_in_loan - 1)

loan_repayment_rounded = round(monthly_loan_repayment, 2)

interest_on_loan = principal * \
    ((1 + interest_rate) ** total_periods_in_loan - 1)

print("Monthly Loan Repayment:", loan_repayment_rounded)
print("Total Interest on Loan:", interest_on_loan)


def compounding_period():
    if compounding_periods_per_year == "A":
        compounding_factor = 1
    elif compounding_periods_per_year == "Q":
        compounding_factor = 4
    else:
        compounding_factor = 12

    return compounding_factor
