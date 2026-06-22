# use_utilities.py
# Demonstrates importing and using a custom package module

from mypackage import utilities

# Call greet()
message = utilities.greet("Shawn")
print("Greeting:", message)

# Call factorial()
result = utilities.factorial(5)
print("Factorial of 5:", result)
