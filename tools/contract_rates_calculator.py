import os
import csv
from projects.Tools_and_games.tools.contract_rates_models import RateCalculator, ContractEstimator

# Instantiate helpers
calculator = RateCalculator()
estimator = ContractEstimator()
contractMarkup = 1.2  # Define contract markup rate

# --- User input section ---
print("Choose input type:")
print("1. Annual full-time income (including super)")
print("2. Annual full-time income (excluding super)")
print("3. Daily rate (including super)")
print("4. Daily rate (excluding super)")
print("5. Hourly rate (including super)")
print("6. Hourly rate (excluding super)")

# Validate input type with retry
valid_choices = ["1", "2", "3", "4", "5", "6"]
choice = ""
while choice not in valid_choices:
    choice = input("Enter choice (1-6): ")
    if choice not in valid_choices:
        print("Invalid choice. Please enter a number between 1 and 6.")
input_type = "incl" if choice in ["1", "3", "5"] else "excl"

if choice == "1":
    annual_incl = -1
    while annual_incl <= 0:
        try:
            annual_incl = float(
                input("Enter annual income (including super): "))
            if annual_incl <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    day_rate = round(annual_incl / calculator.working_days, 2)
elif choice == "2":
    base_annual = -1
    while base_annual <= 0:
        try:
            base_annual = float(
                input("Enter annual income (excluding super): "))
            if base_annual <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    contractFTEquivalent = base_annual * contractMarkup
    day_rate = round(contractFTEquivalent / calculator.working_days, 2)
elif choice == "3":
    daily_incl = -1
    while daily_incl <= 0:
        try:
            daily_incl = float(input("Enter daily rate (including super): "))
            if daily_incl <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    day_rate = daily_incl  # no markup when super is included
elif choice == "4":
    base_day = -1
    while base_day <= 0:
        try:
            base_day = float(input("Enter daily rate (excluding super): "))
            if base_day <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    day_rate = round(base_day * (1 + calculator.super_rate), 2)
elif choice == "5":
    hourly_incl = -1
    while hourly_incl <= 0:
        try:
            hourly_incl = float(input("Enter hourly rate (including super): "))
            if hourly_incl <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    day_rate = round(hourly_incl * calculator.hours_per_day,
                     2)  # no markup when super is included
elif choice == "6":
    hourly_base = -1
    while hourly_base <= 0:
        try:
            hourly_base = float(input("Enter hourly rate (excluding super): "))
            if hourly_base <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    base_day = hourly_base * calculator.hours_per_day
    day_rate = round(base_day * (1 + calculator.super_rate), 2)
else:
    print("Invalid choice.")
    exit()

# --- Contract duration ---
contract_length = -1
while contract_length <= 0:
    try:
        contract_length = float(input("Enter contract length (numeric): "))
        if contract_length <= 0:
            print("Please enter a positive number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
# Validate contract unit with retry
valid_units = {"D": "days", "W": "weeks", "M": "months", "Y": "years"}
contract_unit = ""
while contract_unit not in valid_units:
    contract_unit = input(
        "Enter contract unit (days [D], weeks [W], months [M], years [Y]): ").upper()
    if contract_unit not in valid_units:
        print("Invalid input. Please enter one of D, W, M, Y.")

contract_days = estimator.estimate_working_days(
    contract_length, valid_units[contract_unit])

# --- Calculations ---
rate_info = calculator.calculate(day_rate, input_type)
contract_info = estimator.calculate_contract_earnings(
    rate_info["Raw"]["base_day_rate"],
    rate_info["Raw"]["full_day_rate"],
    contract_days,
    input_type
)

# --- Output ---

print("\n--- Rate Breakdown ---\n")

for category in ["Hourly", "Daily", "Monthly", "Annual"]:
    for label, (base, super_part, total) in rate_info[category].items():
        print(f"{category} {label}: ${base:.2f} + ${super_part:.2f} = ${total:.2f}")
    print()

print("--- Contract Earnings Estimate ---")
for label, value in contract_info.items():
    print(f"{label}: ${value:.2f}")

# --- Optional CSV Output ---
save_csv = input("Would you like to save this to CSV? (Y/N): ").strip().upper()
if save_csv == "Y":
    csv_file = "rate_calculations.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Input Type", "Base Daily Rate", "Full Daily Rate", "Contract Days",
                "Hourly Base", "Hourly Super", "Hourly Total",
                "Daily Base", "Daily Super", "Daily Total",
                "Monthly Base", "Monthly Super", "Monthly Total",
                "Annual Base", "Annual Super", "Annual Total",
                *contract_info.keys()
            ])

        hourly = list(rate_info["Hourly"].values())[0]
        daily = list(rate_info["Daily"].values())[0]
        monthly = list(rate_info["Monthly"].values())[0]
        annual = list(rate_info["Annual"].values())[0]

        writer.writerow([
            input_type,
            rate_info["Raw"]["base_day_rate"],
            rate_info["Raw"]["full_day_rate"],
            contract_days,
            *hourly,
            *daily,
            *monthly,
            *annual,
            *contract_info.values()
        ])

    print(f"Saved to {csv_file}.")
