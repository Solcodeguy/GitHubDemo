# diary.py

import os
from datetime import datetime

FILENAME = "diary.txt"

def ensure_diary_exists():
    """Checks if diary.txt exists; creates it if not."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            f.write("=== My Diary ===\n\n")

def write_entry():
    """Prompts user for a diary entry and appends it with a timestamp."""
    entry = input("Write your diary entry: ")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_entry = f"[{timestamp}] {entry}\n"

    try:
        with open(FILENAME, "a") as f:
            f.write(formatted_entry)
    except Exception as e:
        print(f"Error writing to diary: {e}")

def read_diary():
    """Reads and prints the entire diary."""
    try:
        with open(FILENAME, "r") as f:
            print("\n--- Diary Contents ---")
            print(f.read())
    except Exception as e:
        print(f"Error reading diary: {e}")

# --- Main Program ---
ensure_diary_exists()
write_entry()
read_diary()
