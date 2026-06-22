# builtin_usage.py
# Demonstrates usage of math, random, and platform modules

import math
import random
import platform

# 1. Generate a random integer between 1 and 100
random_number = random.randint(1, 100)
print("Random Number:", random_number)

# 2. Calculate the square root and floor it
sqrt_value = math.sqrt(random_number)
sqrt_floored = math.floor(sqrt_value)
print("Square Root (floored):", sqrt_floored)

# 3. Retrieve OS name and Python version
os_name = platform.system()
python_version = platform.python_version()

print("Operating System:", os_name)
print("Python Version:", python_version)
