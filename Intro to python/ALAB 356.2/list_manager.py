# list_manager.py

numbers = []

while True:
    print("\n--- List Manager Menu ---")
    print("(a) Add a number")
    print("(b) Remove a number by index")
    print("(c) Display the list")
    print("(d) Quit")

    choice = input("Choose an option: ").lower()

    if choice == "a":
        try:
            value = int(input("Enter an integer to add: "))
            numbers.append(value)
            print("Number added.")
        except ValueError:
            print("Error: Please enter a valid integer.")

    elif choice == "b":
        try:
            index = int(input("Enter the index to remove: "))
            removed = numbers.pop(index)
            print(f"Removed: {removed}")
        except ValueError:
            print("Error: Index must be an integer.")
        except IndexError:
            print("Error: Invalid index. No item removed.")

    elif choice == "c":
        print("Current List:", numbers)

    elif choice == "d":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose a, b, c, or d.")
