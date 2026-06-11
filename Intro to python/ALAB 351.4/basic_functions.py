# basic_functions.py
# Demonstrates defining and using simple functions.

# --- Function 1: Greet the user ---
def greet_user(name=""):
    """Prints a greeting. If no name is provided, prints a generic greeting."""
    if name.strip() == "":
        print("Hello! Welcome!")
    else:
        print(f"Hello, {name}! Welcome!")


# --- Function 2: Add two numbers ---
def add_two_numbers(a, b):
    """Returns the sum of two numbers."""
    return a + b


# --- Function 3: Check if a number is even ---
def is_even(num):
    """Returns True if num is even, otherwise False."""
    return num % 2 == 0


# --- Main Program Demonstration ---
# Calling greet_user
greet_user("Shawn")
greet_user()  # no name provided

# Using add_two_numbers
result = add_two_numbers(10, 5)
print("10 + 5 =", result)

# Using is_even
print(f"4 is even: {is_even(4)}")
print(f"7 is even: {is_even(7)}")
