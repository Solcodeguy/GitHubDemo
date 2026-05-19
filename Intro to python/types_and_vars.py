# types_and_vars.py
# This script demonstrates variables, data types, printing, and simple calculations.

# --- Basic Variables ---
name = "Shawn"          # string variable
age = 32                # integer variable
height = 1.80           # float variable (meters)

# --- Introduction Sentence ---
print(f"Hello, my name is {name}. I am {age} years old and {height} meters tall.")

# --- Age in 5 Years ---
# Calculate what age will be in 5 years
age_in_5_years = age + 5
print(f"In 5 years, I will be {age_in_5_years} years old.")

# --- Rectangle Area Calculation ---
# Demonstrating arithmetic operators
width = 5.5
height_rect = 2
area = width * height_rect  # multiplication operator

print(f"The area of a {width} x {height_rect} rectangle is {area}.")

# --- Demonstrating Operators ---
addition_example = age + 10
division_example = width / height_rect

print("Age + 10 =", addition_example)
print("Width / Height =", division_example)

# --- String Repetition Example ---
print("Python! " * 3)  # repeats the string 3 times
