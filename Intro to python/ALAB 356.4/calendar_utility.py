# calendar_utility.py

import calendar
from datetime import datetime

# --- User Input ---
year = int(input("Enter a year (e.g., 2025): "))
month = int(input("Enter a month (1-12): "))

print("\n--- Calendar Output ---")
print(calendar.month(year, month))

# --- Today's Date Check ---
today = datetime.today()

if today.year == year and today.month == month:
    print(f"Today is {today.strftime('%B %d, %Y')}")
else:
    print("Today does not fall within the specified month/year.")
