"""
Satellite Transmission Decoder
================================
Tasks 1, 2, and 4 from the challenge (Task 3 is the deliberate crash demo,
included as a commented-out block with an explanation).
"""

# ----------------------------------------------------------------------
# THE CORRUPTED SATELLITE DATA FEED
# ----------------------------------------------------------------------
satellite_feed = [
    "72-69-76-76-79",       # Encrypted Word 1 (ASCII decimal codes)
    "87-79-82-76-68",       # Encrypted Word 2 (ASCII decimal codes)
    42,                     # Global positioning float code (Corrupted data!)
    "  _sYstEm_oNlInE_  ",  # System status string
    "0"                     # Battery critical override multiplier
]


# ----------------------------------------------------------------------
# TASK 1: Decode ASCII-code strings into words
# ----------------------------------------------------------------------
def decode_word(code_string):
    """
    Takes a dash-separated string of ASCII decimal codes
    (e.g. "72-69-76-76-79") and returns the decoded word (e.g. "HELLO").
    """
    codes = code_string.split("-")                   # "72-69-76-76-79" -> ["72","69","76","76","79"]
    characters = [chr(int(code)) for code in codes]  # ["72",...] -> ["H","E","L","L","O"]
    return "".join(characters)                       # ["H","E","L","L","O"] -> "HELLO"


print("=" * 50)
print("TASK 1: Decoding ASCII words")
print("=" * 50)
word1 = decode_word(satellite_feed[0])
word2 = decode_word(satellite_feed[1])
print(f"Word 1 decoded: {word1}")
print(f"Word 2 decoded: {word2}")
print(f"Hidden message: {word1} {word2}")


# ----------------------------------------------------------------------
# TASK 2: Clean up the messy status string
# ----------------------------------------------------------------------
print()
print("=" * 50)
print("TASK 2: Cleaning the system status string")
print("=" * 50)

raw_status = satellite_feed[3]                # "  _sYstEm_oNlInE_  "
stripped = raw_status.strip()                 # remove leading/trailing whitespace -> "_sYstEm_oNlInE_"
no_underscores = stripped.replace("_", "")    # remove underscores         -> "sYstEmoNlInE"
cleaned_status = no_underscores.lower()       # lowercase                 -> "systemonline"

print(f"Raw status:     {raw_status!r}")
print(f"Cleaned status: {cleaned_status!r}")


# ----------------------------------------------------------------------
# TASK 3: The Crash Test (intentionally NOT run by default)
# ----------------------------------------------------------------------
# Uncomment the block below to watch it crash on item #3 (the integer 42):
#
# print("\nTASK 3: Crash test")
# for item in satellite_feed:
#     decoded = decode_word(item)
#     print(decoded)
#
# Final line of the traceback you'll see:
#
#   AttributeError: 'int' object has no attribute 'split'
#
# WHY: decode_word() immediately calls code_string.split("-"). .split() is a
# STRING method - it only exists on str objects. Item #3, 42, is an int, not
# a string. Python has no implicit type coercion, so calling a string method
# on an int isn't quietly "fixed" for you - the interpreter raises
# AttributeError because int objects simply don't have a .split attribute.


# ----------------------------------------------------------------------
# TASK 4: The Bulletproof Shield (try/except version)
# ----------------------------------------------------------------------
print()
print("=" * 50)
print("TASK 4: Bulletproof processing loop")
print("=" * 50)

for index, item in enumerate(satellite_feed):
    # --- Attempt 1: decode the item as an ASCII-code string ---
    try:
        decoded = decode_word(item)
        print(f"Item {index}: Decoded -> {decoded!r}")
    except AttributeError:
        print("[SYSTEM WARNING]: Skipped corrupted non-string data.")
    except ValueError:
        # Bonus catch: the cleaned status string has no dashes, so it gets
        # treated as one giant "code" that can't convert to int either.
        print("[SYSTEM WARNING]: Skipped data with invalid ASCII codes.")

    # --- Attempt 2: battery override division check (100 / item) ---
    try:
        override_factor = 100 / int(item)
        print(f"Item {index}: Battery override factor -> {override_factor}")
    except ZeroDivisionError:
        print("[SYSTEM WARNING]: Cannot divide by zero override.")
    except (ValueError, TypeError):
        # Bonus bulletproofing: words/strings that aren't pure numbers can't
        # convert to int at all - not part of the original ask, but it keeps
        # the script from crashing on those items too.
        pass

print()
print("Transmission processing complete. No crashes. Mission successful.")
