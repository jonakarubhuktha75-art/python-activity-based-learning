
def calculate_attendance(attended, total):
    if total == 0:
        return 0.0
    return (attended / total) * 100


def classes_needed(attended, total, threshold):
    if calculate_attendance(attended, total) >= threshold:
        return 0

    # Assume all future classes are attended
    needed = 0

    while calculate_attendance(attended + needed, total + needed) < threshold:
        needed += 1

    return needed


def main():
    print("=== Attendance Recovery Computation ===")

    attended = int(input("Enter classes attended: "))
    total = int(input("Enter total classes conducted: "))
    threshold = float(input("Enter eligibility threshold (%): "))

    if total < 0 or attended < 0 or attended > total:
        print("Invalid attendance details.")
        return

    if not 0 <= threshold <= 100:
        print("Threshold must be between 0 and 100.")
        return

    current = calculate_attendance(attended, total)

    print(f"\nCurrent Attendance: {current:.2f}%")
    print(f"Eligibility Threshold: {threshold:.2f}%")

    if current >= threshold:
        print("Status: Eligible")
        print("Additional consecutive classes required: 0")
    elif threshold == 100:
        print("A 100% attendance rate requires attending every future class.")
        print("If any class has already been missed, 100% cannot be reached.")
    else:
        needed = classes_needed(attended, total, threshold)
        print("Status: Not Eligible")
        print(f"Minimum consecutive classes to attend: {needed}")

        future_total = total + needed
        future_attended = attended + needed
        future_percentage = calculate_attendance(
            future_attended, future_total
        )

        print(f"Future attendance: {future_percentage:.2f}%")

    print("\n--- Future Attendance Scenarios ---")

    for scenario in [0, 5, 10, 15, 20]:
        future_attended = attended + scenario
        future_total = total + scenario
        percentage = calculate_attendance(
            future_attended, future_total
        )

        print(
            f"If you attend the next {scenario:2d} classes: "
            f"{percentage:.2f}%"
        )


if __name__ == "__main__":
    main()
