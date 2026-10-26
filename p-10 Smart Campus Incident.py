
# Smart Campus Incident and Maintenance Prioritization

# Predefined severity scores
SEVERITY_SCORE = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

# Location importance scores
LOCATION_SCORE = {
    "Classroom": 2,
    "Library": 2,
    "Cafeteria": 3,
    "Hostel": 3,
    "Laboratory": 4,
    "Electrical Room": 5,
    "Main Gate": 3,
    "Corridor": 1
}


def calculate_priority(severity, location, frequency):
    # Higher severity, location importance, and frequency
    # increase the overall priority score.
    score = (
        SEVERITY_SCORE[severity] * 10
        + LOCATION_SCORE[location] * 5
        + min(frequency, 10) * 2
    )

    if severity == "Critical":
        priority = "URGENT"
    elif score >= 55:
        priority = "HIGH"
    elif score >= 35:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return score, priority


def main():
    incidents = [
        {
            "id": 1,
            "issue": "Exposed electrical wiring",
            "severity": "Critical",
            "location": "Electrical Room",
            "frequency": 2
        },
        {
            "id": 2,
            "issue": "Projector not working",
            "severity": "Medium",
            "location": "Classroom",
            "frequency": 5
        },
        {
            "id": 3,
            "issue": "Water leakage",
            "severity": "High",
            "location": "Hostel",
            "frequency": 7
        },
        {
            "id": 4,
            "issue": "Broken corridor light",
            "severity": "Low",
            "location": "Corridor",
            "frequency": 3
        },
        {
            "id": 5,
            "issue": "Damaged laboratory equipment",
            "severity": "High",
            "location": "Laboratory",
            "frequency": 4
        }
    ]

    # Calculate scores and priorities
    for incident in incidents:
        score, priority = calculate_priority(
            incident["severity"],
            incident["location"],
            incident["frequency"]
        )
        incident["score"] = score
        incident["priority"] = priority

    # Sort by score (highest first), then severity
    incidents.sort(
        key=lambda item: (
            item["score"],
            SEVERITY_SCORE[item["severity"]]
        ),
        reverse=True
    )

    print("\nSMART CAMPUS INCIDENT PRIORITIZATION")
    print("=" * 90)

    for rank, incident in enumerate(incidents, start=1):
        print(f"\nRank: {rank}")
        print(f"Incident ID : {incident['id']}")
        print(f"Issue       : {incident['issue']}")
        print(f"Severity    : {incident['severity']}")
        print(f"Location    : {incident['location']}")
        print(f"Frequency   : {incident['frequency']} reports")
        print(f"Score       : {incident['score']}")
        print(f"Priority    : {incident['priority']}")

    # Generate priority summary
    summary = {
        "URGENT": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for incident in incidents:
        summary[incident["priority"]] += 1

    print("\n" + "=" * 90)
    print("PRIORITY SUMMARY")
    print("=" * 90)

    for priority, count in summary.items():
        print(f"{priority:8s}: {count} incident(s)")

    print("\nRECOMMENDED ACTIONS")
    print("-" * 90)

    for incident in incidents:
        if incident["priority"] == "URGENT":
            action = "Take immediate safety action and notify campus authorities."
        elif incident["priority"] == "HIGH":
            action = "Arrange prompt inspection and repair."
        elif incident["priority"] == "MEDIUM":
            action = "Schedule maintenance soon."
        else:
            action = "Add to routine maintenance schedule."

        print(f"{incident['issue']}: {action}")


if __name__ == "__main__":
    main()
