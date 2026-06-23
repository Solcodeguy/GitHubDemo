# ============================================
# PART 1 — The corrupted satellite data feed
# ============================================

satellite_feed = [
    "72-69-76-76-79",       # Encrypted Word 1 (ASCII decimal codes)
    "87-79-82-76-68",       # Encrypted Word 2 (ASCII decimal codes)
    42,                     # Corrupted data!
    "  _sYstEm_oNlInE_  ",  # System status string
    "0"                     # Battery critical override multiplier
]


# ============================================
# TASK 1 — ASCII DECODER FUNCTION
# ============================================

def decode_ascii_block(block):
    """
    Takes a string like '72-69-76-76-79'
    Splits it by '-', converts each number to a character,
    and returns the decoded word.
    """
    parts = block.split("-")
    chars = [chr(int(num)) for num in parts]
    return "".join(chars)


# ============================================
# TASK 2 — CLEAN THE SYSTEM STATUS STRING
# ============================================

raw_status = satellite_feed[3]

cleaned_status = (
    raw_status.strip()        # remove leading/trailing whitespace
             .replace("_", "")  # remove underscores
             .lower()          # convert to lowercase
)

print("=== TASK 2 OUTPUT ===")
print("Cleaned System Status:", cleaned_status)


# ============================================
# TASK 3 — CRASH TEST (NO ERROR HANDLING)
# ============================================

print("\n=== TASK 3: EXPECTED CRASH ===")

try:
    for item in satellite_feed:
        # This will crash when item == 42
        print(decode_ascii_block(item))
except Exception as e:
    print("Crash Exception Name:", type(e).__name__)
    print("Why it happened: decode_ascii_block() expects a STRING with .split(), "
          "but 42 is an INTEGER and integers do not have .split().")


# ============================================
# TASK 4 — BULLETPROOF VERSION WITH EXCEPTIONS
# ============================================

for item in satellite_feed:
    try:
        decoded = decode_ascii_block(item)
        print("Decoded:", decoded)

        result = 100 / int(satellite_feed[4])
        print("Battery Override Result:", result)

    except AttributeError:
        print("[SYSTEM WARNING]: Skipped corrupted non-string data.")

    except ValueError:
        print("[SYSTEM WARNING]: Non-numeric data cannot be decoded.")

    except ZeroDivisionError:
        print("[SYSTEM WARNING]: Cannot divide by zero override.")
