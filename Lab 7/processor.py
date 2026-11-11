
import math
import re
from datetime import date


# Function 1: Season Pass Validity
def parse_season_pass_validity(date_str):
    if not isinstance(date_str, str):
        return "Invalid date"

    date_str = date_str.strip()

    # Expected format: YYYY/MM/DD
    if not re.fullmatch(r"[0-9]{4}/[0-9]{2}/[0-9]{2}", date_str):
        return "Invalid date"

    try:
        year, month, day = map(int, date_str.split("/"))

        # Check actual calendar validity
        date(year, month, day)

        valid = year >= 2026

        status = "VALID" if valid else "EXPIRED"

        return (
            f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} "
            f"({status})"
        )

    except (ValueError, OverflowError):
        return "Invalid date"


# Function 2: Trail Gradient
def compute_trail_gradient(elevation_str):
    if not isinstance(elevation_str, str):
        return 0.0

    try:
        parts = elevation_str.split(":")

        if len(parts) != 2:
            return 0.0

        drop = float(parts[0])
        distance = float(parts[1])

        # Reject infinity, NaN and zero distance
        if not math.isfinite(drop) or not math.isfinite(distance):
            return 0.0

        if distance == 0:
            return 0.0

        gradient_pct = (drop / distance) * 100.0

        if not math.isfinite(gradient_pct):
            return 0.0

        return round(gradient_pct, 2)

    except (ValueError, TypeError, OverflowError):
        return 0.0


# Function 3: Lift Access Tier
def calculate_lift_access_tier(zone_code):
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0
    }

    if not isinstance(zone_code, str):
        return 0.0

    prefix = zone_code.strip().upper()[:3]

    # Avoid KeyError for unknown zones
    return zone_rates.get(prefix, 0.0)


# Main Application
def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(e_input))

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(z_input))


if __name__ == "__main__":
    main()
