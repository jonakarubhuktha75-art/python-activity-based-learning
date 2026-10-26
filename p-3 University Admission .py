
# University Admission Decision Engine

# Course eligibility criteria
COURSES = {
    "CSE": {
        "required_subjects": ["Mathematics", "Physics"],
        "minimum_aggregate": 75,
        "minimum_subject_marks": 60
    },
    "ECE": {
        "required_subjects": ["Mathematics", "Physics"],
        "minimum_aggregate": 70,
        "minimum_subject_marks": 50
    },
    "Mechanical": {
        "required_subjects": ["Mathematics", "Physics"],
        "minimum_aggregate": 65,
        "minimum_subject_marks": 45
    },
    "BBA": {
        "required_subjects": ["English"],
        "minimum_aggregate": 60,
        "minimum_subject_marks": 40
    }
}


def evaluate_candidate(candidate, course_name):
    course = COURSES[course_name]
    marks = candidate["marks"]

    # Check whether all required subjects are present
    for subject in course["required_subjects"]:
        if subject not in marks:
            return False, f"Missing required subject: {subject}"

        if marks[subject] < course["minimum_subject_marks"]:
            return False, f"Insufficient marks in {subject}"

    # Calculate aggregate percentage across all supplied subjects
    aggregate = sum(marks.values()) / len(marks)

    candidate["aggregate"] = aggregate

    if aggregate < course["minimum_aggregate"]:
        return False, "Aggregate below course cutoff"

    return True, "Eligible"


def rank_candidates(candidates, course_name):
    eligible = []
    rejected = []

    for candidate in candidates:
        result, reason = evaluate_candidate(candidate, course_name)

        if result:
            eligible.append(candidate)
        else:
            rejected.append({
                "name": candidate["name"],
                "reason": reason
            })

    # Tie-breaking:
    # 1. Higher aggregate marks
    # 2. Higher marks in Mathematics, if available
    # 3. Higher marks in Physics, if available
    # 4. Alphabetical name
    eligible.sort(
        key=lambda candidate: (
            candidate["aggregate"],
            candidate["marks"].get("Mathematics", 0),
            candidate["marks"].get("Physics", 0),
            candidate["name"].lower()
        ),
        reverse=False
    )

    # Sort descending by marks; use a separate sort key
    eligible.sort(
        key=lambda candidate: (
            -candidate["aggregate"],
            -candidate["marks"].get("Mathematics", 0),
            -candidate["marks"].get("Physics", 0),
            candidate["name"].lower()
        )
    )

    return eligible, rejected


def main():
    print("=== UNIVERSITY ADMISSION DECISION ENGINE ===")

    print("\nAvailable courses:")
    for course in COURSES:
        print("-", course)

    course_name = input("\nEnter course name: ").strip()

    if course_name not in COURSES:
        print("Invalid course selected.")
        return

    candidates = [
        {
            "name": "Ananya",
            "application_id": "A101",
            "marks": {
                "Mathematics": 92,
                "Physics": 88,
                "Chemistry": 85,
                "English": 90
            }
        },
        {
            "name": "Rahul",
            "application_id": "A102",
            "marks": {
                "Mathematics": 80,
                "Physics": 75,
                "Chemistry": 78,
                "English": 82
            }
        },
        {
            "name": "Priya",
            "application_id": "A103",
            "marks": {
                "Mathematics": 65,
                "Physics": 55,
                "Chemistry": 70,
                "English": 80
            }
        },
        {
            "name": "Arjun",
            "application_id": "A104",
            "marks": {
                "Mathematics": 85,
                "Physics": 80,
                "Chemistry": 82,
                "English": 88
            }
        },
        {
            "name": "Sneha",
            "application_id": "A105",
            "marks": {
                "Mathematics": 75,
                "Physics": 72,
                "Chemistry": 76,
                "English": 80
            }
        }
    ]

    eligible, rejected = rank_candidates(candidates, course_name)

    print(f"\nCOURSE: {course_name}")
    print("=" * 75)
    print("RANKED LIST OF ELIGIBLE APPLICANTS")

    if not eligible:
        print("No eligible applicants found.")
    else:
        for rank, candidate in enumerate(eligible, start=1):
            print(
                f"{rank}. {candidate['name']} "
                f"| ID: {candidate['application_id']} "
                f"| Aggregate: {candidate['aggregate']:.2f}%"
            )

    print("\nINELIGIBLE APPLICANTS")
    print("-" * 75)

    if not rejected:
        print("No rejected applicants.")
    else:
        for candidate in rejected:
            print(f"{candidate['name']}: {candidate['reason']}")

    print("\nADMISSION SUMMARY")
    print("-" * 75)
    print(f"Total applicants evaluated: {len(candidates)}")
    print(f"Eligible applicants: {len(eligible)}")
    print(f"Ineligible applicants: {len(rejected)}")


if __name__ == "__main__":
    main()
