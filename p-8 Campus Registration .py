
import re
from collections import Counter



BRANCH_CODES = {
    "CSE": "Computer Science Engineering",
    "ECE": "Electronics and Communication Engineering",
    "EEE": "Electrical and Electronics Engineering",
    "MECH": "Mechanical Engineering",
    "CIVIL": "Civil Engineering",
    "IT": "Information Technology"
}

MIN_ADMISSION_YEAR = 2000
MAX_ADMISSION_YEAR = 2100

PATTERN = re.compile(
    r"^UNI-(\d{4})-([A-Z]{2,5})-(\d{4})$"
)


def analyze_identifier(identifier):
    identifier = identifier.strip().upper()
    errors = []

    if not identifier:
        return None, ["Identifier is missing."]

    parts = identifier.split("-")

    if len(parts) != 4:
        errors.append(
            "Identifier must contain exactly 4 components "
            "separated by hyphens."
        )
        return None, errors

    campus, year_text, branch, number = parts

    if campus != "UNI":
        errors.append("Campus prefix must be UNI.")

    if not year_text.isdigit() or len(year_text) != 4:
        errors.append("Admission year must contain 4 digits.")
        year = None
    else:
        year = int(year_text)
        if not MIN_ADMISSION_YEAR <= year <= MAX_ADMISSION_YEAR:
            errors.append("Admission year is outside the allowed range.")

    if not re.fullmatch(r"[A-Z]{2,5}", branch):
        errors.append("Branch code must contain 2-5 uppercase letters.")
    elif branch not in BRANCH_CODES:
        errors.append(f"Unknown branch code: {branch}")

    if not re.fullmatch(r"\d{4}", number):
        errors.append("Student number must contain exactly 4 digits.")

    if errors:
        return None, errors

    return {
        "identifier": identifier,
        "campus": campus,
        "admission_year": year,
        "branch_code": branch,
        "branch_name": BRANCH_CODES[branch],
        "student_number": number
    }, []


def classify_year(year):
    if year >= 2025:
        return "Recent Admission"
    elif year >= 2020:
        return "Intermediate Admission"
    else:
        return "Earlier Admission"


def main():
    print("=== CAMPUS REGISTRATION IDENTIFIER ANALYZER ===")

    identifiers = [
        "UNI-2025-CSE-0123",
        "UNI-2024-ECE-0045",
        "UNI-2023-MECH-0156",
        "UNI-2022-IT-0234",
        "UNI-2021-XYZ-0021",
        "UNI-20C5-CSE-0123",
        "UNI-2020-CIVIL-1001",
        "BAD-2025-EEE-0007"
    ]

    valid_records = []
    invalid_records = []

    for identifier in identifiers:
        record, errors = analyze_identifier(identifier)

        print("\nIdentifier:", identifier)

        if record:
            record["admission_category"] = classify_year(
                record["admission_year"]
            )
            valid_records.append(record)

            print("Status          : VALID")
            print("Campus          :", record["campus"])
            print("Admission Year  :", record["admission_year"])
            print("Branch Code     :", record["branch_code"])
            print("Branch Name     :", record["branch_name"])
            print("Student Number  :", record["student_number"])
            print("Year Category   :", record["admission_category"])
        else:
            invalid_records.append(identifier)
            print("Status          : INVALID")
            for error in errors:
                print("Error           :", error)

    # Summary by branch
    branch_counts = Counter(
        record["branch_code"] for record in valid_records
    )

    # Summary by admission year
    year_counts = Counter(
        record["admission_year"] for record in valid_records
    )

    print("\n========== CLASSIFICATION SUMMARY ==========")
    print("Total identifiers:", len(identifiers))
    print("Valid records    :", len(valid_records))
    print("Invalid records  :", len(invalid_records))

    print("\nStudents by Branch:")
    for branch, count in sorted(branch_counts.items()):
        print(f"{branch} ({BRANCH_CODES[branch]}): {count}")

    print("\nStudents by Admission Year:")
    for year, count in sorted(year_counts.items()):
        print(f"{year}: {count}")

    print("\nInvalid Identifiers:")
    if invalid_records:
        for identifier in invalid_records:
            print("-", identifier)
    else:
        print("None")


if __name__ == "__main__":
    main()
