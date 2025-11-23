import pandas as pd

# create the ability to calculate day rate and FT equivalent annual:
# day rate exclusive of superannuation
# day rate inclusive of superannuation
# hourly rate for both

# given a day or hourly rate calculate FT equivalent annual

# given a desired FT annual calculate:
# day rate exclusive of superannuation
# day rate inclusive of superannuation
# hourly rate for both


workingDays = 220
superannuationRate = round((11.5/100), 3)
contractMarkup = 1.2
hoursInDay = 8.00


calculation1_prompt = float(
    input("What is your desired annual FT income (excluding superannuation)? "))


def ratesBasedOnFTEquivalent():

    contractFTEquivalent = calculation1_prompt * contractMarkup
    dayRate = round((contractFTEquivalent/workingDays), 2)
    hourRate = round((dayRate/hoursInDay), 2)
    dayRateSuperannuation = round((dayRate/(1+superannuationRate)), 2)
    superAmountIncluded = round((dayRate - dayRateSuperannuation), 2)
    superOnTopofBase = round((dayRate * superannuationRate), 2)
    days_inPeriod = 30

    print("RATE INFORMATION - SUPERANNUATION INCLUDED IN RATE these rates need to be adjusted for superannuation. True income is rate minus super")
    print("------------------------------------------")

    print(f'\nBased on your FT income, your contract equivalent FT income, including superannuation, is: {contractFTEquivalent}')
    print(f'\nBased on the contract FTE your day rate, including superannuation, is: {dayRate}')
    print(f'\nBased on the day rate, your hourly rate, including superannuation, is: {hourRate}')

    print("\nRATE INFORMATION - SUPERANNUATION calculated. This is the amount of superannuation you need to contribute based on 11.5%")
    print(f'\nYour day rate attracts the following superannuation amount (per day): ${superAmountIncluded}')
    print(f'\nAfter superannuation you have the following remaining: $ {dayRate - superAmountIncluded}')
    print(f'\nYour superannuation contribution for period length of {days_inPeriod} days is {round((days_inPeriod * dayRateSuperannuation), 2)}')

    print("\nRATE INFORMATION - SUPERANNUATION not INCLUDED IN RATES. Super will be paid additional to the rates. These FTE equivalents are base plus super")
    print("------------------------------------------")
    print(f'\nBased on your FT income, your contract equivalent FT income, base rate PLUS superannuation, is: {contractFTEquivalent + superOnTopofBase}')
    print(f'\nBased on your FT income, your total day rate, (base rate PLUS superannuation), is: {round(((contractFTEquivalent + superOnTopofBase)/workingDays), 2)}')
    print(f'Your daily superannuation value is: $ {superOnTopofBase}')
    print(f'The period contribution value to superannuation is: ${round((superOnTopofBase * days_inPeriod), 2)} based on day period of {days_inPeriod} days')


ratesBasedOnFTEquivalent()
