# -----------------------------------------
# Phone Book Directory Script
# -----------------------------------------

# Create the phone book dictionary
phone_book = {
    "Alice": "555-1234",
    "Bob": "555-9876",
    "Charlie": "555-2468"
}

# Look up and print Bob's phone number
print("Bob's number:", phone_book["Bob"])

# Update Alice's phone number
phone_book["Alice"] = "555-0000"

# Add David to the phone book
phone_book["David"] = "555-4321"

# Print the updated phone book
print("Updated phone book:", phone_book)
