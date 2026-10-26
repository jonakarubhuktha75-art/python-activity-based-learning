
import re

# Validation rules
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9-]+"
    r"(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
)

REGISTRATION_PATTERN = re.compile(
    r"^STU-\d{4}-[A-Z]{2,4}$"
)


def validate_email(email):
    errors = []

    if not email:
        return False, ["Email is missing."]

    if email.count("@") == 0:
        errors.append("Missing '@' separator.")
    elif email.count("@") > 1:
        errors.append("Multiple '@' separators found.")

    if "@" in email:
        username, domain = email.rsplit("@", 1)

        if not username:
            errors.append("Username component is missing.")
        if not domain:
            errors.append("Domain component is missing.")

        if username:
            if username.startswith(".") or username.endswith("."):
                errors.append("Username cannot start or end with a dot.")
            if ".." in username:
                errors.append("Consecutive dots in username.")

        if domain:
            if "." not in domain:
                errors.append("Domain must contain a dot.")
            if domain.startswith(".") or domain.endswith("."):
                errors.append("Domain cannot start or end with a dot.")
            if ".." in domain:
                errors.append("Consecutive dots in domain.")

    if any(char.isspace() for char in email):
        errors.append("Whitespace is not allowed.")

    if not errors and not EMAIL_PATTERN.fullmatch(email):
        errors.append("Invalid email character group or format.")

    return len(errors) == 0, errors


def validate_registration_id(reg_id):
    errors = []

    if not reg_id:
        return False, ["Registration ID is missing."]

    if reg_id.count("-") != 2:
        errors.append("Registration ID must contain exactly 2 hyphens.")

    parts = reg_id.split("-")

    if len(parts) >= 1 and parts[0] != "STU":
        errors.append("Prefix must be 'STU'.")

    if len(parts) < 2 or not parts[1]:
        errors.append("Year component is missing.")
    elif not parts[1].isdigit():
        errors.append("Year must contain digits only.")
    elif len(parts[1]) != 4:
        errors.append("Year must contain exactly 4 digits.")

    if len(parts) < 3 or not parts[2]:
        errors.append("Student code component is missing.")
    elif not re.fullmatch(r"[A-Z]{2,4}", parts[2]):
        errors.append(
            "Student code must contain 2-4 uppercase letters only."
        )

    if not errors and not REGISTRATION_PATTERN.fullmatch(reg_id):
        errors.append("Registration ID format is invalid.")

    return len(errors) == 0, errors


def report(label, value, validator):
    valid, errors = validator(value)

    print(f"\n{label}: {value!r}")

    if valid:
        print("Status: VALID")
    else:
        print("Status: INVALID")
        for error in errors:
            print(f" - {error}")


def main():
    print("=== STUDENT EMAIL AND IDENTIFIER VALIDATION ===")

    email = input("Enter student email: ").strip()
    reg_id = input("Enter registration ID: ").strip()

    report("Email", email, validate_email)
    report("Registration ID", reg_id, validate_registration_id)


if __name__ == "__main__":
    main()
