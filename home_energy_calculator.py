class ElectricityCalculator:
    BREAKDOWN_FACTOR = 100
    DAILY_CHARGE_MULTIPLIER = 100

    def __init__(self):
        """Initialize the calculator after getting user consent."""
        if not self.get_user_consent():
            print("Calculator terminated. Goodbye!")
            return

        # Initialize basic parameters
        self.elecDailyCharge = self.get_positive_float(
            "What is the daily charge of this plan? ")
        self.daysInBillPeriod = self.get_positive_float(
            "How many days is the bill comparison period? ")

        # Start the calculation process
        self.run_calculator()

    def get_user_consent(self) -> bool:
        """Get user consent before proceeding with calculations."""
        while True:
            welcome = input(
                "This calculator allows you to use information from your current electricity or gas bill "
                "and assess it against other rate offers.\n"
                "Enter the values from your bill.\n"
                "If your rate is looks like this 0.2623 enter this value\n"
                "if your rate appears as 26.23 then divide by 100 before entering\n"
                "Do you want to continue (Y/N)? ").upper()
            if welcome in ['Y', 'N']:
                return welcome == 'Y'
            print("Invalid input. Please enter Y or N.")

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

    def calculate_solar_feed_in_tariff(self, tariffRate: float, tariffkWhForPeriod: float) -> float:
        """Calculate the solar feed-in tariff."""
        # return (tariffRate/self.BREAKDOWN_FACTOR) * tariffkWhForPeriod
        return (tariffRate * tariffkWhForPeriod)

    def calculate_daily_supply(self) -> float:
        """Calculate the daily supply charge, multiplied by 100."""
        return (self.elecDailyCharge * self.daysInBillPeriod)

    def get_usage_details(self) -> tuple:
        """Get electricity usage details from user including peak and off-peak rates."""
        print("\nPlease enter your electricity usage details:")

        # Peak usage details
        print("\nPeak Usage Details:")
        peak_rate = self.get_positive_float(
            "What is your peak electricity rate (cents per kWh)? ")
        peak_usage = self.get_positive_float(
            "What is your peak electricity usage (kWh) for the period? ")

        # Off-peak usage details
        print("\nOff-Peak Usage Details:")
        offpeak_rate = self.get_positive_float(
            "What is your off-peak electricity rate (cents per kWh)? ")
        offpeak_usage = self.get_positive_float(
            "What is your off-peak electricity usage (kWh) for the period? ")

        return peak_rate, peak_usage, offpeak_rate, offpeak_usage

    def calculate_usage_cost(self, rate: float, usage: float) -> float:
        """Calculate the cost of electricity usage."""
        return (rate * usage)

    def run_calculator(self) -> None:
        """Main calculation process."""
        try:
            # Get usage details
            peak_rate, peak_usage, offpeak_rate, offpeak_usage = self.get_usage_details()

            # Calculate costs
            supply_charge = self.calculate_daily_supply()
            peak_cost = self.calculate_usage_cost(peak_rate, peak_usage)
            offpeak_cost = self.calculate_usage_cost(
                offpeak_rate, offpeak_usage)
            total_cost = supply_charge + peak_cost + offpeak_cost

            # Display results
            print("\nCalculation Results:")
            print(f"Period Length: {self.daysInBillPeriod} days")
            print(f"Daily Supply Charge: ${supply_charge:.2f}")
            print(f"Peak Usage Cost: ${peak_cost:.2f}")
            print(f"Off-Peak Usage Cost: ${offpeak_cost:.2f}")
            print(f"Total Cost: ${total_cost:.2f}")

            # Display usage breakdown
            total_usage = peak_usage + offpeak_usage
            print("\nUsage Breakdown:")
            print(
                f"Peak Usage: {peak_usage:.2f} kWh ({(peak_usage/total_usage*100):.1f}%)")
            print(
                f"Off-Peak Usage: {offpeak_usage:.2f} kWh ({(offpeak_usage/total_usage*100):.1f}%)")
            print(f"Total Usage: {total_usage:.2f} kWh")

            # Ask if user wants to calculate solar feed-in tariff
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


calculator = ElectricityCalculator()
