import pandas as pd
import os
import webbrowser
from colorama import init, Fore, Style

init(autoreset=True)

# === Input Utilities ===


def get_user_input(prompt):
    return input(prompt).strip()


def get_float(prompt, allow_zero=True):
    while True:
        try:
            value = float(get_user_input(prompt))
            if not allow_zero and value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid number in digits (e.g., 22.34)")


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
    print("1. Electricity")
    print("2. Gas")
    print("3. Both")
    choice = None
    while choice not in ["1", "2", "3"]:
        choice = get_user_input("Enter your choice (1/2/3): ")
    return choice


def show_cents_notice():
    print("\n⚠️ IMPORTANT: Enter all rates and charges in **cents** (as shown on your bill)")
    print("   For example:")
    print("   - If your peak rate is 22.34¢/kWh → enter 22.34")
    print("   - If your feed-in tariff is 3¢/kWh → enter 3")
    print("   - If your daily supply charge is 105¢ → enter 105")
    print("   (The system will convert cents to dollars for calculations.)\n")


def append_usage_and_rate_tables(usage_list, rate_list, service, supplier, usage_data, rate_data):
    usage_row = {"Service": service, "Supplier": supplier, **usage_data}
    rate_row = {"Service": service, "Supplier": supplier, **rate_data}
    usage_list.append(usage_row)
    rate_list.append(rate_row)


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
        "Gross Bill ($)": round(gross_total, 2),
        "Solar Credit ($)": round(solar_credit, 2),
        "Net Bill ($)": round(net, 2),
        "Cost Per Day ($)": round(per_day, 2),
        "% Saved vs Current": None
    }


def export_to_html(df, usage_table, rate_table, filename="comparison_report.html"):
    df["Rank"] = df.groupby("Service")['Net Bill ($)'].rank("dense")
    df_sorted = df.sort_values(by=["Service", "Rank"])

    def style_row(row):
        min_net = df[df["Service"] == row["Service"]]["Net Bill ($)"].min()
        max_net = df[df["Service"] == row["Service"]]["Net Bill ($)"].max()
        is_current = row["Supplier Type"].strip().lower() == "current"
        is_best = row["Net Bill ($)"] == min_net
        is_worst = row["Net Bill ($)"] == max_net

        styles = []
        for _ in row:
            if is_best and is_current:
                styles.append(
                    'background-color: #d4edda; color: green; font-weight: bold')
            elif is_best:
                styles.append('color: green; font-weight: bold')
            elif is_worst:
                styles.append('color: red')
            elif is_current:
                styles.append('color: blue')
            else:
                styles.append('')
        return styles

    styled = df_sorted.style.set_caption("<h2>Utility Comparison Report <span style='font-size:14px;'>(💰 Best deal highlighted)</span></h2>") \
        .set_table_attributes('border="1" class="dataframe table table-striped table-bordered"') \
        .apply(style_row, axis=1) \
        .format({
            "Gross Bill ($)": "${:.2f}",
            "Solar Credit ($)": "${:.2f}",
            "Net Bill ($)": "${:.2f}",
            "Cost Per Day ($)": "${:.2f}",
            "% Saved vs Current": lambda x: x if x else "",
            "$ Saved vs Current": "${:.2f}",
            "Rank": "{:,.0f}"
        })

    with open(filename, "w", encoding="utf-8") as f:

        f.write("<html><head><title>Utility Comparison Report</title></head><body>")
        f.write("<h1>Input Usage Data</h1>")
        f.write(usage_table.to_html(index=False, border=1))
        f.write("<h1>Input Rate Data</h1>")
        f.write(rate_table.to_html(index=False, border=1))
        f.write(styled.to_html(index=False))
        f.write("</body></html>")

    webbrowser.open('file://' + os.path.realpath(filename))
    print(f"\n🌐 HTML report saved as {filename}")

# === MAIN LOGIC ===


def main():
    results = []
    usage_rows = []
    rate_rows = []

    choice = get_service_choice()
    compare_electricity = choice in ["1", "3"]
    compare_gas = choice in ["2", "3"]

    if compare_electricity:
        print("\n--- Enter Electricity Usage ---")
        usage_data = {
            "peak_usage": get_float("Enter peak power consumption (kWh): "),
            "offpeak_usage": get_float("Enter off-peak power consumption (kWh): "),
            "billing_days": get_float("Enter number of billing days: "),
            "solar_export_kwh": get_float("Enter solar export to grid (kWh): ") if get_yes_no("Do you have solar? (y/n): ") else 0
        }
        show_cents_notice()
        name = get_user_input("Enter current electricity supplier name: ")
        rate_data = {
            "peak_rate": get_float("Enter the peak rate (in cents/kWh): "),
            "offpeak_rate": get_float("Enter the off-peak rate (in cents/kWh): "),
            "daily_supply_charge": get_float("Enter the daily supply charge (in cents): "),
            "feed_in_rate": get_float("Enter the solar feed-in tariff rate (in cents/kWh): ") if usage_data["solar_export_kwh"] > 0 else 0
        }
        append_usage_and_rate_tables(
            usage_rows, rate_rows, "Electricity", name, usage_data, rate_data)
        results.append(calculate_bill("Electricity", name,
                       "Current", usage_data, rate_data))

        while get_yes_no("Add another electricity supplier to compare? (y/n): "):
            name = get_user_input(
                "Enter alternative electricity supplier name: ")
            rate_data = {
                "peak_rate": get_float("Enter the peak rate (in cents/kWh): "),
                "offpeak_rate": get_float("Enter the off-peak rate (in cents/kWh): "),
                "daily_supply_charge": get_float("Enter the daily supply charge (in cents): "),
                "feed_in_rate": get_float("Enter the solar feed-in tariff rate (in cents/kWh): ") if usage_data["solar_export_kwh"] > 0 else 0
            }
            append_usage_and_rate_tables(
                usage_rows, rate_rows, "Electricity", name, usage_data, rate_data)
            results.append(calculate_bill("Electricity", name,
                           "Alternative", usage_data, rate_data))

    if compare_gas:
        print("\n--- Enter Gas Usage ---")
        usage_data = {
            "billing_days": get_float("Enter number of billing days: "),
            "tier1_units": get_float("Enter gas usage in first tier (units): "),
            "tier2_units": get_float("Enter gas usage in second tier (units): "),
            "tier3_units": get_float("Enter gas usage in third tier (units): ")
        }
        show_cents_notice()
        name = get_user_input("Enter current gas supplier name: ")
        rate_data = {
            "daily_supply_charge": get_float("Enter the daily supply charge (in cents): "),
            "tier1_rate": get_float("Enter the first tier rate (in cents/unit): "),
            "tier2_rate": get_float("Enter the second tier rate (in cents/unit): "),
            "tier3_rate": get_float("Enter the third tier rate (in cents/unit): ")
        }
        append_usage_and_rate_tables(
            usage_rows, rate_rows, "Gas", name, usage_data, rate_data)
        results.append(calculate_bill(
            "Gas", name, "Current", usage_data, rate_data))

        while get_yes_no("Add another gas supplier to compare? (y/n): "):
            name = get_user_input("Enter alternative gas supplier name: ")
            rate_data = {
                "daily_supply_charge": get_float("Enter the daily supply charge (in cents): "),
                "tier1_rate": get_float("Enter the first tier rate (in cents/unit): "),
                "tier2_rate": get_float("Enter the second tier rate (in cents/unit): "),
                "tier3_rate": get_float("Enter the third tier rate (in cents/unit): ")
            }
            append_usage_and_rate_tables(
                usage_rows, rate_rows, "Gas", name, usage_data, rate_data)
            results.append(calculate_bill(
                "Gas", name, "Alternative", usage_data, rate_data))

    df = pd.DataFrame(results)

    # Calculate % Saved and $ Saved vs Current per service
    for service in df['Service'].unique():
        service_df = df[df['Service'] == service]
        current_net = service_df[service_df['Supplier Type'].str.lower(
        ) == 'current']['Net Bill ($)']
        if not current_net.empty:
            current_net = current_net.iloc[0]
            df.loc[df['Service'] == service, '% Saved vs Current'] = (
                (current_net - df.loc[df['Service'] ==
                 service, 'Net Bill ($)']) / current_net * 100
            ).round(1).astype(str) + '%'
            df.loc[df['Service'] == service, '$ Saved vs Current'] = (
                current_net - df.loc[df['Service'] == service, 'Net Bill ($)']
            ).round(2)
    usage_df = pd.DataFrame(usage_rows)
    rate_df = pd.DataFrame(rate_rows)

    if get_yes_no("\nWould you like to export these results to HTML? (y/n):"):
        filename = get_user_input("Enter filename (without extension): ")
        export_to_html(df, usage_df, rate_df, filename + ".html")


if __name__ == "__main__":
    main()
