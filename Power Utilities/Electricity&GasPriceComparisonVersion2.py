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


def get_user_input(prompt):
    return input(prompt).strip().lower()


def prompt_choice(prompt, valid_options, aliases=None):
    aliases = aliases or {}
    while True:
        choice = get_user_input(prompt)
        if choice in aliases:
            return aliases[choice]
        if choice in valid_options:
            return choice
        allowed = sorted(set(valid_options + list(aliases.keys())))
        print(f"Please enter one of: {', '.join(allowed)}")


def prompt_float(prompt):
    while True:
        raw = get_user_input(prompt)
        try:
            value = float(raw)
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def prompt_nonempty(prompt):
    while True:
        value = get_user_input(prompt)
        if value:
            return value
        print("Please enter a value.")


def get_supplier_details(service_type):
    supplier_name = prompt_nonempty(
        f"Enter your current {service_type} supplier name: ")
    latest_bill = prompt_float(
        f"Enter your latest {service_type} bill amount: ")
    cost_breakdown = prompt_nonempty(
        f"Enter the cost breakdown for {service_type} (e.g., base charge, usage charge): ")
    return supplier_name, latest_bill, cost_breakdown


def main():
    compare_choice = prompt_choice(
        "Do you want to compare prices for electricity/e, gas/g, or both/b? ",
        ["electricity", "gas", "both"],
        aliases={"e": "electricity", "g": "gas", "b": "both"}
    )

    current_suppliers = {}
    if prompt_choice(
        "Do you have a current supplier? (yes/y, no/n) ",
        ["yes", "no"],
        aliases={"y": "yes", "n": "no"}
    ) == "yes":
        if compare_choice in ["electricity", "both"]:
            current_suppliers['electricity'] = get_supplier_details(
                "electricity")
        if compare_choice in ["gas", "both"]:
            current_suppliers['gas'] = get_supplier_details("gas")

    proposed_suppliers = {}
    if prompt_choice(
        "Do you want to enter details for a proposed supplier? (yes/y, no/n) ",
        ["yes", "no"],
        aliases={"y": "yes", "n": "no"}
    ) == "yes":
        if compare_choice in ["electricity", "both"]:
            proposed_suppliers['electricity'] = get_supplier_details(
                "electricity")
        if compare_choice in ["gas", "both"]:
            proposed_suppliers['gas'] = get_supplier_details("gas")

    # Calculate and compare values
    comparison_results = []
    warnings = []
    for service, (current_supplier, current_bill, current_breakdown) in current_suppliers.items():
        proposed_supplier, proposed_bill, proposed_breakdown = proposed_suppliers.get(
            service, (None, None, None))
        if proposed_supplier:
            savings = current_bill - proposed_bill
            comparison_results.append({
                'Service': service,
                'Current Supplier': current_supplier,
                'Proposed Supplier': proposed_supplier,
                'Current Bill': current_bill,
                'Proposed Bill': proposed_bill,
                'Savings': savings,
                'Current Breakdown': current_breakdown,
                'Proposed Breakdown': proposed_breakdown
            })
        else:
            warnings.append(
                f"No proposed {service} supplier entered; skipping comparison.")

    # Display results using pandas DataFrame
    if comparison_results:
        df = pd.DataFrame(comparison_results)
        print("\nComparison Results:")
        print(df)
    else:
        print("No comparison data available.")
    if warnings:
        print("\nNotes:")
        for note in warnings:
            print(f"- {note}")


if __name__ == "__main__":
    main()
