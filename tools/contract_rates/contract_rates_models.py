# Tools_and_games/rates/models.py

class RateCalculator:
    def __init__(self, working_days=220, super_rate=0.115, hours_per_day=8.0, months_in_year=12):
        self.working_days = working_days
        self.super_rate = super_rate
        self.hours_per_day = hours_per_day
        self.months_in_year = months_in_year

    def calculate(self, day_rate_incl_super, input_type):
        base_day_rate = round(day_rate_incl_super / (1 + self.super_rate), 2)
        super_daily = round(day_rate_incl_super - base_day_rate, 2)

        base_hour_rate = round(base_day_rate / self.hours_per_day, 2)
        full_hour_rate = round(day_rate_incl_super / self.hours_per_day, 2)
        super_hourly = round(full_hour_rate - base_hour_rate, 2)

        annual_base = round(base_day_rate * self.working_days, 2)
        annual_super = round(annual_base * self.super_rate, 2)
        annual_package = round(annual_base + annual_super, 2)

        annual_incl_super = round(day_rate_incl_super * self.working_days, 2)
        super_annual_incl = round(
            annual_incl_super - base_day_rate * self.working_days, 2)

        monthly_base = round(annual_base / self.months_in_year, 2)
        monthly_super = round(monthly_base * self.super_rate, 2)
        monthly_package = round(monthly_base + monthly_super, 2)

        monthly_incl_super = round(annual_incl_super / self.months_in_year, 2)
        super_monthly_incl = round(monthly_incl_super - monthly_base, 2)

        result = {
            "Hourly": {},
            "Daily": {},
            "Monthly": {},
            "Annual": {},
            "Raw": {
                "base_day_rate": base_day_rate,
                "full_day_rate": day_rate_incl_super,
            }
        }

        if input_type == "incl":
            result["Hourly"]["Incl Super"] = (
                base_hour_rate, super_hourly, full_hour_rate)
            result["Daily"]["Incl Super"] = (
                base_day_rate, super_daily, day_rate_incl_super)
            result["Monthly"]["Incl Super"] = (
                monthly_base, super_monthly_incl, monthly_incl_super)
            result["Annual"]["Incl Super"] = (
                annual_base, super_annual_incl, annual_incl_super)
        elif input_type == "excl":
            result["Hourly"]["Super On Top"] = (
                base_hour_rate,
                round(base_hour_rate * self.super_rate, 2),
                round(base_hour_rate * (1 + self.super_rate), 2),
            )
            result["Daily"]["Super On Top"] = (
                base_day_rate,
                round(base_day_rate * self.super_rate, 2),
                round(base_day_rate * (1 + self.super_rate), 2),
            )
            result["Monthly"]["Super On Top"] = (
                monthly_base,
                monthly_super,
                monthly_package,
            )
            result["Annual"]["Super On Top"] = (
                annual_base,
                annual_super,
                annual_package,
            )

        return result


class ContractEstimator:
    def __init__(self, working_days=220, super_rate=0.115):
        self.working_days = working_days
        self.super_rate = super_rate

    def estimate_working_days(self, duration, unit):
        unit = unit.lower()
        if unit in ["day", "days"]:
            return int(duration)
        elif unit in ["week", "weeks"]:
            return int(duration * 5)
        elif unit in ["month", "months"]:
            return int((duration / 12) * self.working_days)
        elif unit in ["year", "years"]:
            return int(duration * self.working_days)
        else:
            raise ValueError("Invalid contract unit")

    def calculate_contract_earnings(self, base_day_rate, full_day_rate, contract_days, input_type):
        base = round(base_day_rate * contract_days, 2)
        super_val = round(base * self.super_rate, 2)
        incl = round(full_day_rate * contract_days, 2)
        package = round(base + super_val, 2)

        if input_type == "incl":
            return {
                "Base": base,
                "Super (Derived)": incl - base,
                "Total (Incl Super)": incl,
            }
        elif input_type == "excl":
            return {
                "Base": base,
                "Super": super_val,
                "Total (Super On Top)": package,
            }
        else:
            raise ValueError("Invalid input type")
