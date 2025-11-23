import pandas as pd

# Constants
workingDays = 220
superannuationRate = round((11.5 / 100), 3)
hoursInDay = 8.00


class ContractRateCalculator:
    def __init__(self):
        self.calculation1_prompt = input(
            "Do you want to start with an (H)ourly rate, (D)ay rate or a Desired (A)nnual income? ").upper()
        while self.calculation1_prompt not in ["H", "D", "A"]:
            print("Invalid input. Please enter 'H', 'D', or 'A'.")
            self.calculation1_prompt = input(
                "Do you want to start with an (H)ourly rate, (D)ay rate or a Desired (A)nnual income? ").upper()

        self.calculation2_prompt = input(
            "Is the value you input (I)nclusive of superannuation or (B)ase (excluding super)? ").upper()
        while self.calculation2_prompt not in ["I", "B"]:
            print("Invalid input. Please enter 'I' or 'B'.")
            self.calculation2_prompt = input(
                "Is the value you input (I)nclusive of superannuation or (B)ase (excluding super)? ").upper()

    def calculateFromAnnual(self):
        amount = float(input("What annual amount are you starting with? "))
        if self.calculation2_prompt == "B":
            base = amount
            superannuation = base * superannuationRate
        else:
            base = amount / (1 + superannuationRate)
            superannuation = amount - base
        total = base + superannuation
        day_rate = round(total / workingDays, 2)
        hour_rate = round(day_rate / hoursInDay, 2)
        print(f"\nAnnual Base: ${base:.2f}")
        print(f"Superannuation: ${superannuation:.2f}")
        print(f"Total Package: ${total:.2f}")
        print(f"Day Rate: ${day_rate:.2f}")
        print(f"Hourly Rate: ${hour_rate:.2f}")

    def calculateFromHourly(self):
        hourly = float(input("What hourly rate are you starting with? "))
        if self.calculation2_prompt == "B":
            base = hourly * hoursInDay * workingDays
            superannuation = base * superannuationRate
        else:
            total = hourly * hoursInDay * workingDays
            base = total / (1 + superannuationRate)
            superannuation = total - base
        total = base + superannuation
        print(f"\nAnnual Base: ${base:.2f}")
        print(f"Superannuation: ${superannuation:.2f}")
        print(f"Total Package: ${total:.2f}")

    def calculateFromDaily(self):
        daily = float(input("What day rate are you starting with? "))
        if self.calculation2_prompt == "B":
            base = daily * workingDays
            superannuation = base * superannuationRate
        else:
            total = daily * workingDays
            base = total / (1 + superannuationRate)
            superannuation = total - base
        total = base + superannuation
        print(f"\nAnnual Base: ${base:.2f}")
        print(f"Superannuation: ${superannuation:.2f}")
        print(f"Total Package: ${total:.2f}")

    def calculateRates(self):
        if self.calculation1_prompt == "A":
            self.calculateFromAnnual()
        elif self.calculation1_prompt == "H":
            self.calculateFromHourly()
        elif self.calculation1_prompt == "D":
            self.calculateFromDaily()


# Run the calculator
calculator = ContractRateCalculator()
calculator.calculateRates()
