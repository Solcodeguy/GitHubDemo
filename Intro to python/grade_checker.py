# grade_checker.py

grade = int(input("Enter your numeric grade (0-100): "))

# Determine letter grade
if 90 <= grade <= 100:
    letter = "A"
elif 80 <= grade <= 89:
    letter = "B"
elif 70 <= grade <= 79:
    letter = "C"
elif 60 <= grade <= 69:
    letter = "D"
else:
    letter = "F"

print(f"Your grade is: {letter}")

# Conditional expression for final message
message = "Great job, keep it up!" if letter in ("A", "B", "C") else "Don't give up — try again!"
print(message)
90