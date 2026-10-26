
# Nested List Classroom Occupancy Analysis

# None = vacant seat
# "RESERVED" = seat reserved and unavailable for allocation
# Student names represent occupied seats

classrooms = {
    "Classroom A": [
        ["Alice", None, "RESERVED"],
        ["Bob", None, None]
    ],
    "Classroom B": [
        [None, "Charlie", None],
        ["RESERVED", None, None]
    ],
    "Classroom C": [
        [None, None, None],
        [None, "David", "RESERVED"]
    ]
}


def display_classrooms(classrooms):
    print("\n========== CLASSROOM SEATING ==========")

    for room, rows in classrooms.items():
        print(f"\n{room}")

        for row_index, row in enumerate(rows, start=1):
            print(f"Row {row_index}: {row}")


def find_student_duplicates(classrooms):
    student_locations = {}

    for room, rows in classrooms.items():
        for row_index, row in enumerate(rows):
            for seat_index, seat in enumerate(row):
                if seat is None or seat == "RESERVED":
                    continue

                student = seat.strip()

                if student:
                    student_locations.setdefault(student, []).append(
                        (room, row_index + 1, seat_index + 1)
                    )

    duplicates = {
        student: locations
        for student, locations in student_locations.items()
        if len(locations) > 1
    }

    return duplicates


def allocate_student(classrooms, student, room_name):
    if room_name not in classrooms:
        print(f"Error: {room_name} does not exist.")
        return False

    if not student.strip():
        print("Error: Student name cannot be empty.")
        return False

    # Prevent duplicate allocation across all classrooms
    duplicates = find_student_duplicates(classrooms)

    existing_students = {
        seat.strip()
        for rows in classrooms.values()
        for row in rows
        for seat in row
        if isinstance(seat, str) and seat != "RESERVED"
    }

    if student.strip() in existing_students:
        print(f"Error: {student} is already allocated.")
        return False

    # Allocate the student to the first available seat
    for row_index, row in enumerate(classrooms[room_name]):
        for seat_index, seat in enumerate(row):
            if seat is None:
                classrooms[room_name][row_index][seat_index] = student.strip()
                print(
                    f"{student} allocated to {room_name}, "
                    f"row {row_index + 1}, seat {seat_index + 1}."
                )
                return True

    print(f"Error: No vacant seats in {room_name}.")
    return False


def calculate_occupancy(classrooms):
    summary = {}

    for room, rows in classrooms.items():
        total_seats = 0
        occupied = 0
        reserved = 0
        vacant = 0

        for row in rows:
            for seat in row:
                total_seats += 1

                if seat is None:
                    vacant += 1
                elif seat == "RESERVED":
                    reserved += 1
                else:
                    occupied += 1

        summary[room] = {
            "total": total_seats,
            "occupied": occupied,
            "reserved": reserved,
            "vacant": vacant,
            "available": vacant
        }

    return summary


def main():
    display_classrooms(classrooms)

    print("\n========== DUPLICATE ASSIGNMENT CHECK ==========")
    duplicates = find_student_duplicates(classrooms)

    if duplicates:
        for student, locations in duplicates.items():
            print(f"{student} appears at:")
            for location in locations:
                print(
                    f"  Room: {location[0]}, "
                    f"Row: {location[1]}, Seat: {location[2]}"
                )
    else:
        print("No duplicate student assignments found.")

    print("\n========== STUDENT ALLOCATION ==========")
    allocate_student(classrooms, "Eve", "Classroom A")
    allocate_student(classrooms, "Alice", "Classroom B")

    display_classrooms(classrooms)

    print("\n========== OCCUPANCY SUMMARY ==========")
    summary = calculate_occupancy(classrooms)

    overall_total = 0
    overall_occupied = 0
    overall_reserved = 0
    overall_vacant = 0

    for room, details in summary.items():
        print(f"\n{room}")
        print(f"Total seats       : {details['total']}")
        print(f"Occupied seats    : {details['occupied']}")
        print(f"Reserved seats    : {details['reserved']}")
        print(f"Vacant seats      : {details['vacant']}")

        overall_total += details["total"]
        overall_occupied += details["occupied"]
        overall_reserved += details["reserved"]
        overall_vacant += details["vacant"]

    print("\n========== OVERALL CAPACITY ==========")
    print(f"Total seats       : {overall_total}")
    print(f"Occupied seats    : {overall_occupied}")
    print(f"Reserved seats    : {overall_reserved}")
    print(f"Vacant seats      : {overall_vacant}")
    print(f"Available capacity: {overall_vacant}")

    if overall_total:
        occupancy_rate = overall_occupied / overall_total * 100
        print(f"Occupancy rate    : {occupancy_rate:.2f}%")


if __name__ == "__main__":
    main()
