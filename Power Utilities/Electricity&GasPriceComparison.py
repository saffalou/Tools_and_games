from abc import ABC, abstractmethod


def get_user_consent() -> bool:
    """Get user consent before proceeding with calculations."""
    while True:
        welcome = input(
            "This calculator allows you to use information from your current electricity or gas bill "
            "and assess it against other rate offers.\n"
            "\t -Enter the values from your bill.\n"
            "\t -If your rate looks like this 0.2623 enter this value\n"
            "\t -if your rate appears as 26.23 then divide by 100 before entering\n"
            "Do you want to continue (Y/N)? ").upper()
        if welcome in ['Y', 'N']:
            return welcome == 'Y'
        print("Invalid input. Please enter Y or N.")


class EnergyCalculator(ABC):
    """Abstract base class for energy calculators."""
    BREAKDOWN_FACTOR = 100
    DAILY_CHARGE_MULTIPLIER = 100

    def __init__(self):
        """Initialize the calculator."""
        self.dailyCharge = 0
        self.daysInBillPeriod = 0

    def get_positive_float(self, prompt: str) -> float:
        """Get a positive float value from user input."""
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    print("Please enter a positive number")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number")

    def calculate_daily_supply(self) -> float:
        """Calculate the daily supply charge."""
        return (self.dailyCharge * self.daysInBillPeriod)

    def calculate_usage_cost(self, rate: float, usage: float) -> float:
        """Calculate the cost of energy usage."""
        return (rate * usage)

    @abstractmethod
    def get_usage_details(self) -> tuple:
        """Get energy usage details from user."""
        pass

    @abstractmethod
    def run_calculator(self) -> None:
        """Main calculation process."""
        pass


class ElectricityCalculator(EnergyCalculator):
    """Calculator for electricity usage and costs."""

    def __init__(self):
        """Initialize the electricity calculator."""
        super().__init__()
        self.dailyCharge = self.get_positive_float(
            "What is the daily charge of this electricity plan? ")
        self.daysInBillPeriod = self.get_positive_float(
            "How many days is the bill comparison period? ")
        self.run_calculator()

    def calculate_solar_feed_in_tariff(self, tariffRate: float, tariffkWhForPeriod: float) -> float:
        """Calculate the solar feed-in tariff."""
        return (tariffRate * tariffkWhForPeriod)

    def get_usage_details(self) -> tuple:
        """Get electricity usage details from user including peak and off-peak rates."""
        print("\nPlease enter your electricity usage details:")

        print("\nPeak Usage Details:")
        peak_rate = self.get_positive_float(
            "What is your peak electricity rate (cents per kWh)? ")
        peak_usage = self.get_positive_float(
            "What is your peak electricity usage (kWh) for the period? ")

        print("\nOff-Peak Usage Details:")
        offpeak_rate = self.get_positive_float(
            "What is your off-peak electricity rate (cents per kWh)? ")
        offpeak_usage = self.get_positive_float(
            "What is your off-peak electricity usage (kWh) for the period? ")

        return peak_rate, peak_usage, offpeak_rate, offpeak_usage

    def run_calculator(self) -> None:
        """Main calculation process for electricity."""
        try:
            peak_rate, peak_usage, offpeak_rate, offpeak_usage = self.get_usage_details()

            supply_charge = self.calculate_daily_supply()
            peak_cost = self.calculate_usage_cost(peak_rate, peak_usage)
            offpeak_cost = self.calculate_usage_cost(
                offpeak_rate, offpeak_usage)
            total_cost = supply_charge + peak_cost + offpeak_cost

            print("\nCalculation Results:")
            print(f"Period Length: {self.daysInBillPeriod} days")
            print(f"Daily Supply Charge: ${supply_charge:.2f}")
            print(f"Peak Usage Cost: ${peak_cost:.2f}")
            print(f"Off-Peak Usage Cost: ${offpeak_cost:.2f}")
            print(f"Total Cost: ${total_cost:.2f}")

            total_usage = peak_usage + offpeak_usage
            print("\nUsage Breakdown:")
            print(
                f"Peak Usage: {peak_usage:.2f} kWh ({(peak_usage/total_usage*100):.1f}%)")
            print(
                f"Off-Peak Usage: {offpeak_usage:.2f} kWh ({(offpeak_usage/total_usage*100):.1f}%)")
            print(f"Total Usage: {total_usage:.2f} kWh")

            if input("\nWould you like to calculate solar feed-in tariff? (Y/N): ").upper() == 'Y':
                tariff_rate = self.get_positive_float(
                    "What is your feed-in tariff rate (cents per kWh)? ")
                solar_kwh = self.get_positive_float(
                    "How many kWh did you export to the grid? ")
                solar_credit = self.calculate_solar_feed_in_tariff(
                    tariff_rate, solar_kwh)
                print(f"\nSolar Feed-in Credit: ${solar_credit:.2f}")
                print(
                    f"Final Bill After Solar Credit: ${(total_cost - solar_credit):.2f}")

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")


class GasCalculator(EnergyCalculator):
    """Calculator for gas usage and costs."""

    def __init__(self):
        """Initialize the gas calculator."""
        super().__init__()
        self.dailyCharge = self.get_positive_float(
            "What is the daily charge of this gas plan? ")
        self.daysInBillPeriod = self.get_positive_float(
            "How many days is the bill comparison period? ")
        self.run_calculator()

    def get_usage_details(self) -> tuple:
        """Get gas usage details from user."""
        print("\nPlease enter your gas usage details:")

        # First tier is always required
        print("\nFirst Tier Usage Details:")
        first_rate = self.get_positive_float(
            "What is your first tier gas rate (cents per MJ)? ")
        first_usage = self.get_positive_float(
            "What is your first tier gas usage (MJ) for the period? ")

        # Ask if there's a second tier
        has_second_tier = input(
            "\nIs there a second tier rate? (Y/N): ").upper() == 'Y'

        if has_second_tier:
            print("\nSecond Tier Usage Details:")
            second_rate = self.get_positive_float(
                "What is your second tier gas rate (cents per MJ)? ")
            second_usage = self.get_positive_float(
                "What is your second tier gas usage (MJ) for the period? ")
        else:
            second_rate = 0
            second_usage = 0

        return first_rate, first_usage, second_rate, second_usage, has_second_tier

    def run_calculator(self) -> None:
        """Main calculation process for gas."""
        try:
            first_rate, first_usage, second_rate, second_usage, has_second_tier = self.get_usage_details()

            supply_charge = self.calculate_daily_supply()
            first_tier_cost = self.calculate_usage_cost(
                first_rate, first_usage)
            second_tier_cost = self.calculate_usage_cost(
                second_rate, second_usage)
            total_cost = supply_charge + first_tier_cost + second_tier_cost

            print("\nCalculation Results:")
            print(f"Period Length: {self.daysInBillPeriod} days")
            print(f"Daily Supply Charge: ${supply_charge:.2f}")
            print(f"First Tier Usage Cost: ${first_tier_cost:.2f}")

            total_usage = first_usage
            if has_second_tier:
                print(f"Second Tier Usage Cost: ${second_tier_cost:.2f}")
                total_usage += second_usage

            print(f"Total Cost: ${total_cost:.2f}")

            print("\nUsage Breakdown:")
            print(
                f"First Tier Usage: {first_usage:.2f} MJ ({(first_usage/total_usage*100):.1f}%)")
            if has_second_tier:
                print(
                    f"Second Tier Usage: {second_usage:.2f} MJ ({(second_usage/total_usage*100):.1f}%)")
            print(f"Total Gas Usage: {total_usage:.2f} MJ")

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")


def main():
    """Main function to run the energy calculator."""
    # Get initial consent
    if not get_user_consent():
        print("Calculator terminated. Goodbye!")
        return

    # Let user choose calculator type
    while True:
        choice = input(
            "\nWhat would you like to calculate?\n1. Electricity\n2. Gas\nEnter choice (1/2): ")
        if choice == "1":
            calculator = ElectricityCalculator()
            break
        elif choice == "2":
            calculator = GasCalculator()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
