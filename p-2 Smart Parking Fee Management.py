
from datetime import datetime
import math

VEHICLE_RATES = {
    "bike": 10,
    "car": 20,
    "bus": 40
}

DAILY_LIMITS = {
    "bike": 100,
    "car": 200,
    "bus": 400
}

OVERNIGHT_FEE = {
    "bike": 20,
    "car": 50,
    "bus": 100
}

LATE_EXIT_PENALTY = 100
LOST_TICKET_PENALTY = 200


def get_datetime(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid input! Use YYYY-MM-DD HH:MM (e.g. 2026-10-26 09:30).")


def calculate_fee(entry, exit_time, vehicle):
    if exit_time <= entry:
        raise ValueError("Exit time must be after entry time.")

    duration_minutes = (exit_time - entry).total_seconds() / 60
    total_hours = math.ceil(duration_minutes / 60)

    days = math.ceil(duration_minutes / (24 * 60))

    hourly_rate = VEHICLE_RATES[vehicle]
    daily_limit = DAILY_LIMITS[vehicle]

    remaining_hours = total_hours
    total_fee = 0
    overnight_count = 0

    for day in range(days):
        hours = min(24, remaining_hours)
        daily_charge = min(hours * hourly_rate, daily_limit)
        total_fee += daily_charge
        remaining_hours -= hours

        if day < days - 1:
            overnight_count += 1

    overnight_charge = overnight_count * OVERNIGHT_FEE[vehicle]
    total_fee += overnight_charge

    return total_hours, days, overnight_count, overnight_charge, total_fee


def main():
    print("=== SMART PARKING FEE MANAGEMENT ===")

    print("\nVehicle categories: bike, car, bus")
    vehicle = input("Enter vehicle category: ").strip().lower()

    if vehicle not in VEHICLE_RATES:
        print("Invalid vehicle category.")
        return

    entry = get_datetime("Enter entry time (YYYY-MM-DD HH:MM): ")
    exit_time = get_datetime("Enter exit time (YYYY-MM-DD HH:MM): ")

    if exit_time <= entry:
        print("Error: Exit time must be later than entry time.")
        return

    lost_ticket = input("Lost parking ticket? (yes/no): ").strip().lower()
    late_exit = input("Late exit penalty applicable? (yes/no): ").strip().lower()

    if lost_ticket not in ("yes", "no"):
        print("Invalid lost-ticket response.")
        return

    if late_exit not in ("yes", "no"):
        print("Invalid late-exit response.")
        return

    try:
        hours, days, nights, overnight_fee, parking_fee = calculate_fee(
            entry, exit_time, vehicle
        )
    except ValueError as error:
        print("Error:", error)
        return

    lost_penalty = LOST_TICKET_PENALTY if lost_ticket == "yes" else 0
    late_penalty = LATE_EXIT_PENALTY if late_exit == "yes" else 0

    total_penalty = lost_penalty + late_penalty
    final_amount = parking_fee + total_penalty

    print("\n========== PARKING RECEIPT ==========")
    print(f"Vehicle category      : {vehicle.title()}")
    print(f"Entry time            : {entry}")
    print(f"Exit time             : {exit_time}")
    print(f"Parking duration      : {hours} billed hour(s)")
    print(f"Billing periods       : {days}")
    print(f"Overnight periods     : {nights}")
    print(f"Base parking fee      : Rs. {parking_fee}")
    print(f"Overnight fee         : Rs. {overnight_fee}")
    print(f"Lost-ticket penalty   : Rs. {lost_penalty}")
    print(f"Late-exit penalty     : Rs. {late_penalty}")
    print("-------------------------------------")
    print(f"TOTAL AMOUNT           : Rs. {final_amount}")
    print("=====================================")


if __name__ == "__main__":
    main()
