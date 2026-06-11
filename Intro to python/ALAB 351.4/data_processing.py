# data_processing.py
# Simulates simple data processing with tuples and dictionaries.

def get_average_grade(grades_tuple):
    """Returns the average of a tuple of grades. Handles empty tuples."""
    try:
        if len(grades_tuple) == 0:
            raise ZeroDivisionError("No grades available.")
        return sum(grades_tuple) / len(grades_tuple)
    except ZeroDivisionError as e:
        print("Warning:", e)
        return None


# Dictionary of courses and grade tuples
course_grades = {
    "Math": (90, 85, 88),
    "Science": (75, 80, 79),
    "History": (),  # edge case: empty tuple
    "English": (92, 87)
}

# Loop through courses
for course, grades in course_grades.items():
    avg = get_average_grade(grades)
    if avg is not None:
        print(f"The average grade for {course} is {avg:.2f}")
    else:
        print(f"No average available for {course}.")
