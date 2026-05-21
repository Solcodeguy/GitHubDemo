age = int(input("How old are you? "))

if age < 18:
    print("Access denied. Too young!")
elif age <= 20:
    print("You can come in, but no drinking! 🚫🍷")
else:
    print("Welcome in! Enjoy your night.")
