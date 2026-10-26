

WEAK_SUBJECT_THRESHOLD = 40

def analyze_student(name, scores):
    subjects = list(scores.keys())
    exams = list(scores[subjects[0]].keys())

    total_scores = []
    print(f"\nStudent: {name}")
    print("-" * 65)

    for subject in subjects:
        marks = list(scores[subject].values())
        improvement = marks[-1] - marks[0]

        if improvement > 0:
            trend = f"Improved by {improvement} marks"
        elif improvement < 0:
            trend = f"Declined by {abs(improvement)} marks"
        else:
            trend = "No change"

        print(f"{subject}: {marks} -> {trend}")
        total_scores.extend(marks)

    weak_subjects = []

    for subject in subjects:
        marks = list(scores[subject].values())

        if all(mark < WEAK_SUBJECT_THRESHOLD for mark in marks):
            weak_subjects.append(subject)

    average = sum(total_scores) / len(total_scores)

    if average >= 85:
        category = "Excellent"
    elif average >= 70:
        category = "Good"
    elif average >= 50:
        category = "Average"
    else:
        category = "Needs Improvement"

    print(f"\nOverall Average: {average:.2f}%")
    print(f"Performance Category: {category}")

    if weak_subjects:
        print("Consistently Weak Subjects:", ", ".join(weak_subjects))
    else:
        print("Consistently Weak Subjects: None")

    first_total = sum(scores[s][exams[0]] for s in subjects)
    last_total = sum(scores[s][exams[-1]] for s in subjects)

    print(f"First Exam Total: {first_total}")
    print(f"Last Exam Total: {last_total}")
    print(f"Overall Change: {last_total - first_total} marks")


def main():
    students = {
        "Ananya": {
            "Mathematics": {"Exam 1": 65, "Exam 2": 75, "Exam 3": 90},
            "Science": {"Exam 1": 70, "Exam 2": 80, "Exam 3": 85},
            "English": {"Exam 1": 80, "Exam 2": 78, "Exam 3": 88}
        },
        "Rahul": {
            "Mathematics": {"Exam 1": 30, "Exam 2": 35, "Exam 3": 38},
            "Science": {"Exam 1": 45, "Exam 2": 50, "Exam 3": 48},
            "English": {"Exam 1": 60, "Exam 2": 65, "Exam 3": 70}
        },
        "Priya": {
            "Mathematics": {"Exam 1": 75, "Exam 2": 68, "Exam 3": 60},
            "Science": {"Exam 1": 80, "Exam 2": 75, "Exam 3": 70},
            "English": {"Exam 1": 85, "Exam 2": 88, "Exam 3": 90}
        }
    }

    print("=== STUDENT PERFORMANCE TREND ANALYSIS ===")

    for name, scores in students.items():
        analyze_student(name, scores)

    print("\n" + "=" * 65)
    print("CLASS PERFORMANCE SUMMARY")
    print("=" * 65)

    averages = {}

    for name, scores in students.items():
        marks = [
            mark
            for subject_scores in scores.values()
            for mark in subject_scores.values()
        ]
        averages[name] = sum(marks) / len(marks)

    ranked_students = sorted(
        averages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for rank, (name, average) in enumerate(ranked_students, start=1):
        print(f"{rank}. {name}: {average:.2f}%")

    class_average = sum(averages.values()) / len(averages)
    print(f"\nClass Average: {class_average:.2f}%")


if __name__ == "__main__":
    main()
