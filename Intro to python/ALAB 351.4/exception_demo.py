# exception_demo.py
# Demonstrates raising exceptions, catching them, and using finally.

def safe_divide(a, b):
    """Divides a by b, raising ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# --- Testing safe_divide ---
try:
    print("10 / 2 =", safe_divide(10, 2))
    print("10 / 0 =", safe_divide(10, 0))  # will raise error
except ValueError as e:
    print("Error:", e)
finally:
    print("Division operation completed")


# --- Generic Exception Example ---
try:
    num = int("not_a_number")  # invalid conversion
except Exception as e:
    print("A generic exception occurred:", e)
