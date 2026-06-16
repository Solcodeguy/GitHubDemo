def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = input("Enter contact name: ").strip()

    if name in contacts:
        print("This name already exists. Contact not added.")
        return

    phone = input("Enter phone number: ").strip()

    if not phone.isdigit():
        print("Invalid phone number. Use digits only.")
        return

    contacts[name] = phone
    print(f"Contact '{name}' added successfully.")


def view_contacts(contacts):
    print("\n--- All Contacts ---")
    if not contacts:
        print("The contact list is empty.")
        return

    for name in sorted(contacts):
        print(f"{name}: {contacts[name]}")


def search_contact(contacts):
    print("\n--- Search Contact ---")
    query = input("Enter name or part of name to search: ").strip().lower()

    results = {name: phone for name, phone in contacts.items() if query in name.lower()}

    if results:
        print("Search Results:")
        for name, phone in results.items():
            print(f"{name}: {phone}")
    else:
        print("No matching contacts found.")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")
    name = input("Enter the name of the contact to delete: ").strip()

    if name in contacts:
        del contacts[name]
        print(f"Contact '{name}' deleted successfully.")
    else:
        print("Contact not found.")


def main():
    contacts = {}

    while True:
        print("\nContact Book Menu:")
        print("1. Add New Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            add_contact(contacts)
        elif choice == 2:
            view_contacts(contacts)
        elif choice == 3:
            search_contact(contacts)
        elif choice == 4:
            delete_contact(contacts)
        elif choice == 5:
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


main()
