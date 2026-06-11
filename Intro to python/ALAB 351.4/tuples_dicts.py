# tuples_dicts.py
# Demonstrates tuples, immutability, and dictionary operations.

# --- Tuple of Months ---
months = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
)

print("First month:", months[0])
print("Last month:", months[-1])

# Attempt to modify tuple
try:
    months[0] = "NewMonth"
except Exception as e:
    print("Tuples are immutable, error:", e)


# --- Dictionary of Students ---
students = {
    "Alice": 90,
    "Bob": 85,
    "Charlie": 92
}

# Add new student
students["Diana"] = 88

# Print all students
print("\nAll students and grades:")
for name, grade in students.items():
    print(f"{name}: {grade}")

# Update a grade
students["Bob"] = 95
print("\nUpdated Bob's grade:", students["Bob"])

# Loop formatted output
print("\nFormatted student list:")
for name, grade in students.items():
    print(f"{name}: {grade}")
