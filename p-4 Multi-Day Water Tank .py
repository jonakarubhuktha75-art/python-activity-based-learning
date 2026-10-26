
# Multi-Day Water Tank Simulation

def simulate_tank(capacity, initial_water, inflows, outflows, threshold):
    water_level = initial_water
    first_threshold_interval = None

    overflow_count = 0
    shortage_count = 0

    print("\n========== WATER TANK SIMULATION ==========")
    print(f"Tank Capacity       : {capacity} liters")
    print(f"Initial Water Level : {initial_water} liters")
    print(f"Target Threshold    : {threshold} liters")
    print("-" * 85)

    print(
        f"{'Day':<8}{'Inflow':<12}{'Outflow':<12}"
        f"{'Final Level':<16}{'Status'}"
    )
    print("-" * 85)

    for day, (inflow, outflow) in enumerate(
        zip(inflows, outflows), start=1
    ):
        # Calculate water before applying tank limits
        raw_level = water_level + inflow - outflow
        status = []

        # Detect overflow
        if raw_level > capacity:
            overflow = raw_level - capacity
            overflow_count += 1
            status.append(f"OVERFLOW ({overflow:.1f} L)")
            water_level = capacity
        else:
            water_level = raw_level

        # Detect shortage
        if water_level < 0:
            shortage = abs(water_level)
            shortage_count += 1
            status.append(f"SHORTAGE ({shortage:.1f} L)")
            water_level = 0

        # Detect the first interval at or above threshold
        if (
            first_threshold_interval is None
            and water_level >= threshold
        ):
            first_threshold_interval = day

        if not status:
            status.append("Normal")

        print(
            f"{day:<8}{inflow:<12.1f}{outflow:<12.1f}"
            f"{water_level:<16.1f}{', '.join(status)}"
        )

    print("-" * 85)
    print(f"Final Water Level    : {water_level:.1f} liters")
    print(f"Overflow Events      : {overflow_count}")
    print(f"Shortage Events      : {shortage_count}")

    if first_threshold_interval is not None:
        print(
            "First Threshold Reached: "
            f"Day {first_threshold_interval}"
        )
    else:
        print("Threshold was not reached during the simulation.")

    print("===========================================")


def main():
    try:
        capacity = float(input("Enter tank capacity (liters): "))
        initial_water = float(input("Enter initial water level (liters): "))
        threshold = float(input("Enter target water threshold (liters): "))
        days = int(input("Enter number of days: "))

        if capacity <= 0:
            raise ValueError("Tank capacity must be positive.")

        if not 0 <= initial_water <= capacity:
            raise ValueError(
                "Initial water must be between 0 and capacity."
            )

        if not 0 <= threshold <= capacity:
            raise ValueError(
                "Threshold must be between 0 and capacity."
            )

        if days <= 0:
            raise ValueError("Number of days must be positive.")

        inflows = []
        outflows = []

        for day in range(1, days + 1):
            print(f"\nDay {day}")
            inflow = float(input("Enter inflow (liters): "))
            outflow = float(input("Enter outflow (liters): "))

            if inflow < 0 or outflow < 0:
                raise ValueError(
                    "Inflow and outflow cannot be negative."
                )

            inflows.append(inflow)
            outflows.append(outflow)

        simulate_tank(
            capacity,
            initial_water,
            inflows,
            outflows,
            threshold
        )

    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()
