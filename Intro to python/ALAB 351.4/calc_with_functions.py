# calc_with_functions.py
# A calculator refactored using functions and exception handling.

# --- Operation Functions ---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


# --- Calculate Function ---
def calculate(a, b, op):
    """Chooses the correct operation based on the symbol."""
    if op == "+":
        return add(a, b)
    elif op == "-":
        return subtract(a, b)
    elif op == "*":
        return multiply(a, b)
    elif op == "/":
        return divide(a, b)
    else:
        return "Error: Invalid operation."


# --- Main Program ---
try:
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    operation = input("Choose an operation (+, -, *, /): ")

    result = calculate(num1, num2, operation)
    print("Result:", result)

except ValueError:
    print("Error: Please enter valid numbers.")
except ZeroDivisionError as e:
    print("Error:", e)
