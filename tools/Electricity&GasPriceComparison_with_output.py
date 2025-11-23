# determine if user want to price compare electricity, gas or both
# ask if they have current supplier(s)
# if current supplier(s) is it for electricity, gas or both
# get supplier names for the services
# do they want to enter latest bill details for electricity, gas or both?
# if no to current details then we cannot calculate net differences against new supplier
# if no to comparison request name of proposed supplier(s)
# if yes to comparison we need names of current supplier(s)
#  calculate values
#  store values

#  if no, or after yes,
# name of supplier
# enter cost breakdown details
# store details

#  when all values captured compare values
# if not comparing current vs new then cheapest of the new
# if comparing current and new then calculate savings from most to least

#  show the values using pandas frame


import pandas as pd
import os
from colorama import init, Fore, Style

init(autoreset=True)

# === Utility Functions ===


def get_user_input(prompt):
    return input(prompt).strip()


def get_float(prompt, allow_zero=True, min_value=None):
    while True:
        try:
            value = float(get_user_input(prompt))
        except ValueError:
            print("Please enter a valid number in digits (e.g., 22.34)")
            continue

        if not allow_zero and value == 0:
            print("Please enter a non-zero number.")
            continue

        if min_value is not None and value < min_value:
            comparator = "or equal to " if allow_zero else ""
            print(
                f"Please enter a number greater than {comparator}{min_value}.")
            continue

        if not allow_zero and min_value is None and value <= 0:
            print("Please enter a number greater than 0.")
            continue

        return value


def get_yes_no(prompt):
    while True:
        response = get_user_input(prompt).lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        print("Please enter yes or no (y/n).")


def get_service_choice():
    print("What would you like to compare?")
    print("1/e. Electricity")
    print("2/g. Gas")
    print("3/b. Both")
    options = {
        "1": "electricity",
        "e": "electricity",
        "electricity": "electricity",
        "2": "gas",
        "g": "gas",
        "gas": "gas",
        "3": "both",
        "b": "both",
        "both": "both"
    }
    while True:
        choice = get_user_input(
            "Enter your choice (1/e for electricity, 2/g for gas, 3/b for both): ").lower()
        if choice in options:
            return options[choice]
        print("Please enter 1/e, 2/g, or 3/b.")


def get_electricity_usage():
    print("--- Electricity Usage & Billing Info ---")
    peak_usage = get_float(
        "Enter peak power consumption (kWh): ", allow_zero=False, min_value=0)
    offpeak_usage = get_float(
        "Enter off-peak power consumption (kWh): ", allow_zero=False, min_value=0)
    billing_days = get_float(
        "Enter number of billing days: ", allow_zero=False, min_value=0)
    solar_export_kwh = 0
    if get_yes_no("Do you have solar? (y/n): "):
        solar_export_kwh = get_float(
            "Enter total kWh exported to the grid: ", min_value=0)
    return {
        "peak_usage": peak_usage,
        "offpeak_usage": offpeak_usage,
        "billing_days": billing_days,
        "solar_export_kwh": solar_export_kwh
    }


def get_gas_usage():
    print("--- Gas Usage & Billing Info ---")
    billing_days = get_float(
        "Enter number of billing days: ", allow_zero=False, min_value=0)
    tier1_units = get_float(
        "Enter gas usage in first tier (units): ", allow_zero=False, min_value=0)
    tier2_units = get_float(
        "Enter gas usage in second tier (units): ", allow_zero=False, min_value=0)
    tier3_units = get_float(
        "Enter gas usage in third tier (units): ", allow_zero=False, min_value=0)
    return {
        "billing_days": billing_days,
        "tier1_units": tier1_units,
        "tier2_units": tier2_units,
        "tier3_units": tier3_units
    }


def show_cents_notice():
    print("⚠️ IMPORTANT: Enter all rates and charges in **cents** (as shown on your bill)")
    print("   For example:")
    print("   - If your peak rate is 22.34¢/kWh → enter 22.34")
    print("   - If your feed-in tariff is 3¢/kWh → enter 3")
    print("   - If your daily supply charge is 105¢ → enter 105")
    print("   (The calculator will convert cents to dollars for calculations.)")


def export_to_csv(df, filename="comparison_results.csv"):
    file_exists = os.path.isfile(filename)
    df.to_csv(filename, mode='a', index=False, header=not file_exists)
    print(f"📁 Results exported to {filename}")


def print_colored_dataframe(df):
    print("--- Final Comparison Summary ---")
    if df.empty:
        print(Fore.YELLOW + "⚠️ No data to display." + Style.RESET_ALL)
        return

    display_df = df.copy()
    display_df["% Saved vs Current"] = display_df["% Saved vs Current"].fillna(
        "")
    rate_cols = [
        "Peak Rate (c/kWh)",
        "Off-peak Rate (c/kWh)",
        "Daily Supply (c)",
        "Feed-in Rate (c/kWh)",
        "Tier1 Rate (c/unit)",
        "Tier2 Rate (c/unit)",
        "Tier3 Rate (c/unit)"
    ]

    def has_data(col):
        return col in display_df.columns and display_df[col].notna().any() and (display_df[col] != "").any()

    for col in rate_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].fillna("")

    warnings = []
    for col in ["Service", "Supplier Type", "Supplier"]:
        display_df[col] = display_df[col].astype(
            str).str.strip().str.ljust(15)

    display_df["Rank"] = 0  # Initialize column
    base_fields = [("Service", 15), ("Supplier Type", 15),
                   ("Supplier", 15), ("Billing Days", 14)]
    optional_rate_fields = [(col, width) for col, width in [
        ("Peak Rate (c/kWh)", 20),
        ("Off-peak Rate (c/kWh)", 24),
        ("Daily Supply (c)", 17),
        ("Feed-in Rate (c/kWh)", 22),
        ("Tier1 Rate (c/unit)", 21),
        ("Tier2 Rate (c/unit)", 21),
        ("Tier3 Rate (c/unit)", 21)
    ] if has_data(col)]
    tail_fields = [("Gross Bill ($)", 16), ("Solar Credit ($)", 18),
                   ("Net Bill ($)", 14), ("Cost Per Day ($)", 18), ("% Saved vs Current", 20)]

    display_fields = base_fields + optional_rate_fields + tail_fields
    for col, _ in display_fields:
        if col in display_df.columns:
            display_df[col] = display_df[col].fillna("")

    header_parts = [f"{'Rank':>4}  "] + \
        [f"{name:<{width}}" for name, width in display_fields]
    header = "".join(header_parts)
    print(header)
    print("-" * len(header))

    for service in display_df["Service"].str.strip().str.capitalize().unique():
        service_df = display_df[display_df["Service"].str.strip().str.capitalize()
                                == service].copy()
        current_rows = service_df[service_df["Supplier Type"].str.strip(
        ).str.lower() == "current"]

        if current_rows.empty:
            warnings.append(
                f"No current supplier for {service}; showing prospective options without savings.")
            service_df.sort_values("Net Bill ($)", inplace=True)
            service_df["Rank"] = range(1, len(service_df) + 1)
            for idx, row in service_df.iterrows():
                display_df.loc[row.name, "Rank"] = row["Rank"]

            min_net = service_df["Net Bill ($)"].min()
            max_net = service_df["Net Bill ($)"].max()

            service_rows = display_df[display_df["Service"].str.strip(
            ).str.capitalize() == service].sort_values("Rank")
            for _, row in service_rows.iterrows():
                color = Fore.RED if row["Net Bill ($)"] == max_net else Fore.GREEN if row[
                    "Net Bill ($)"] == min_net else ""
                bold = Style.BRIGHT if row["Net Bill ($)"] == min_net else ""
                reset = Style.RESET_ALL
                row_parts = [f"{str(row.get(name, '')):<{width}}"
                             for name, width in display_fields]
                formatted_row = f"{bold}{row['Rank']:<4}  " + \
                    "".join(row_parts) + f"{reset}"
                print(color + formatted_row + reset)
            continue

        current_net = current_rows["Net Bill ($)"].iloc[0]
        if current_net == 0:
            warnings.append(
                f"Current {service} net bill is $0; showing entries without savings.")
            service_df.sort_values("Net Bill ($)", inplace=True)
            service_df["Rank"] = range(1, len(service_df) + 1)
            for idx, row in service_df.iterrows():
                display_df.loc[row.name, "Rank"] = row["Rank"]

            min_net = service_df["Net Bill ($)"].min()
            max_net = service_df["Net Bill ($)"].max()

            service_rows = display_df[display_df["Service"].str.strip(
            ).str.capitalize() == service].sort_values("Rank")
            for _, row in service_rows.iterrows():
                color = Fore.RED if row["Net Bill ($)"] == max_net else Fore.GREEN if row["Net Bill ($)"] == min_net else Fore.BLUE if row["Supplier Type"].strip(
                ).lower() == "current" else ""
                bold = Style.BRIGHT if row["Net Bill ($)"] == min_net else ""
                reset = Style.RESET_ALL
                row_parts = [f"{str(row.get(name, '')):<{width}}"
                             for name, width in display_fields]
                formatted_row = f"{bold}{row['Rank']:<4}  " + \
                    "".join(row_parts) + f"{reset}"
                print(color + formatted_row + reset)
            continue

        service_df.sort_values("Net Bill ($)", inplace=True)
        service_df["Rank"] = range(1, len(service_df) + 1)

        for idx, row in service_df.iterrows():
            if row["Supplier Type"].strip().lower() == "prospective":
                savings_pct = (1 - row["Net Bill ($)"] / current_net) * 100
                display_df.loc[row.name,
                               "% Saved vs Current"] = f"{savings_pct:.1f}%"
            display_df.loc[row.name, "Rank"] = row["Rank"]

        min_net = service_df["Net Bill ($)"].min()
        max_net = service_df["Net Bill ($)"].max()

        service_rows = display_df[display_df["Service"].str.strip(
        ).str.capitalize() == service].sort_values("Rank")
        for _, row in service_rows.iterrows():
            color = Fore.RED if row["Net Bill ($)"] == max_net else Fore.GREEN if row["Net Bill ($)"] == min_net else Fore.BLUE if row["Supplier Type"].strip(
            ).lower() == "current" else ""
            bold = Style.BRIGHT if row["Net Bill ($)"] == min_net else ""
            reset = Style.RESET_ALL
            row_parts = [f"{str(row.get(name, '')):<{width}}"
                         for name, width in display_fields]
            formatted_row = f"{bold}{row['Rank']:<4}  " + \
                "".join(row_parts) + f"{reset}"
            print(color + formatted_row + reset)

    if warnings:
        print("\nNotes:")
        for note in warnings:
            print(f"- {note}")


def add_savings(df):
    """Compute % Saved vs Current for each service where a current supplier exists and net bill > 0."""
    if df.empty or "% Saved vs Current" not in df.columns:
        return df

    df = df.copy()
    for service in df["Service"].unique():
        service_mask = df["Service"] == service
        current_rows = df[service_mask & (
            df["Supplier Type"].str.strip().str.lower() == "current")]
        if current_rows.empty:
            continue
        current_net = current_rows["Net Bill ($)"].iloc[0]
        if current_net == 0:
            continue
        alt_mask = service_mask & (
            df["Supplier Type"].str.strip().str.lower() == "prospective")
        df.loc[alt_mask, "% Saved vs Current"] = df.loc[alt_mask].apply(
            lambda row: f"{(1 - row['Net Bill ($)'] / current_net) * 100:.1f}%",
            axis=1
        )
    return df

# === Main Comparison Logic ===


def calculate_bill(service, supplier_name, supplier_type, usage_data, rate_data):
    billing_days = usage_data["billing_days"]
    solar_credit = 0
    gross = 0

    if service == "Electricity":
        gross = (usage_data["peak_usage"] * rate_data["peak_rate"] +
                 usage_data["offpeak_usage"] * rate_data["offpeak_rate"]) / 100
        fixed = billing_days * rate_data["daily_supply_charge"] / 100
        solar_credit = usage_data["solar_export_kwh"] * \
            rate_data["feed_in_rate"] / 100
    else:
        gross = (
            usage_data["tier1_units"] * rate_data["tier1_rate"] +
            usage_data["tier2_units"] * rate_data["tier2_rate"] +
            usage_data["tier3_units"] * rate_data["tier3_rate"]
        ) / 100
        fixed = billing_days * rate_data["daily_supply_charge"] / 100

    gross_total = gross + fixed
    net = gross_total - solar_credit
    per_day = net / billing_days

    return {
        "Service": service,
        "Supplier Type": supplier_type,
        "Supplier": supplier_name,
        "Billing Days": billing_days,
        "Peak Rate (c/kWh)": rate_data.get("peak_rate") if service == "Electricity" else None,
        "Off-peak Rate (c/kWh)": rate_data.get("offpeak_rate") if service == "Electricity" else None,
        "Daily Supply (c)": rate_data.get("daily_supply_charge"),
        "Feed-in Rate (c/kWh)": rate_data.get("feed_in_rate") if service == "Electricity" else None,
        "Tier1 Rate (c/unit)": rate_data.get("tier1_rate") if service == "Gas" else None,
        "Tier2 Rate (c/unit)": rate_data.get("tier2_rate") if service == "Gas" else None,
        "Tier3 Rate (c/unit)": rate_data.get("tier3_rate") if service == "Gas" else None,
        "Gross Bill ($)": round(gross_total, 2),
        "Solar Credit ($)": round(solar_credit, 2),
        "Net Bill ($)": round(net, 2),
        "Cost Per Day ($)": round(per_day, 2),
        "% Saved vs Current": None
    }

# === Main Function ===


def main():
    results = []
    continue_mode = False

    while True:
        if results:
            if get_yes_no("Clear previous results and start fresh? (y/n): "):
                results = []
                continue_mode = False
            else:
                continue_mode = True
                print(
                    "\nContinuing with existing current suppliers; you can add more prospective options.\n")
        else:
            continue_mode = False

        choice = get_service_choice()
        print(f"\nYou chose {choice.capitalize()}.\n")
        compare_electricity = choice in ["electricity", "both"]
        compare_gas = choice in ["gas", "both"]

        if compare_electricity:
            usage = get_electricity_usage()
            show_cents_notice()
            if not continue_mode:
                name = get_user_input(
                    "\nEnter current electricity supplier name: ")
                rate_data = {
                    "peak_rate": get_float("Enter the peak rate (in cents/kWh): ", min_value=0),
                    "offpeak_rate": get_float("Enter the off-peak rate (in cents/kWh): ", min_value=0),
                    "daily_supply_charge": get_float("Enter the daily supply charge (in cents): ", min_value=0),
                    "feed_in_rate": get_float("Enter the solar feed-in tariff rate (in cents/kWh): ", min_value=0) if usage["solar_export_kwh"] > 0 else 0
                }
                results.append(calculate_bill(
                    "Electricity", name, "Current", usage, rate_data))

            while get_yes_no("Add another electricity supplier to compare? (y/n): "):
                name = get_user_input(
                    "Enter prospective electricity supplier name: ")
                rate_data = {
                    "peak_rate": get_float("Enter the peak rate (in cents/kWh): ", min_value=0),
                    "offpeak_rate": get_float("Enter the off-peak rate (in cents/kWh): ", min_value=0),
                    "daily_supply_charge": get_float("Enter the daily supply charge (in cents): ", min_value=0),
                    "feed_in_rate": get_float("Enter the solar feed-in tariff rate (in cents/kWh): ", min_value=0) if usage["solar_export_kwh"] > 0 else 0
                }
                results.append(calculate_bill(
                    "Electricity", name, "Prospective", usage, rate_data))

        if compare_gas:
            usage = get_gas_usage()
            show_cents_notice()
            if not continue_mode:
                name = get_user_input("\nEnter current gas supplier name: ")
                rate_data = {
                    "daily_supply_charge": get_float("Enter the daily supply charge (in cents): ", min_value=0),
                    "tier1_rate": get_float("Enter the first tier rate (in cents/unit): ", min_value=0),
                    "tier2_rate": get_float("Enter the second tier rate (in cents/unit): ", min_value=0),
                    "tier3_rate": get_float("Enter the third tier rate (in cents/unit): ", min_value=0)
                }
                results.append(calculate_bill(
                    "Gas", name, "Current", usage, rate_data))

            while get_yes_no("Add another gas supplier to compare? (y/n): "):
                name = get_user_input("Enter prospective gas supplier name: ")
                rate_data = {
                    "daily_supply_charge": get_float("Enter the daily supply charge (in cents): ", min_value=0),
                    "tier1_rate": get_float("Enter the first tier rate (in cents/unit): ", min_value=0),
                    "tier2_rate": get_float("Enter the second tier rate (in cents/unit): ", min_value=0),
                    "tier3_rate": get_float("Enter the third tier rate (in cents/unit): ", min_value=0)
                }
                results.append(calculate_bill(
                    "Gas", name, "Prospective", usage, rate_data))

        df = add_savings(pd.DataFrame(results))
        print_colored_dataframe(df)

        if get_yes_no("\nWould you like to export these results to CSV? (y/n): "):
            export_to_csv(df)

        if not get_yes_no("\nWould you like to start another comparison? (y/n): "):
            print("\n✅ Thank you for using the Utility Comparison Tool. Goodbye!")
            break


if __name__ == "__main__":
    main()
