def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = input("Enter contact name: ").strip()

    # Check duplicate
    if name in contacts:
        print("This name already exists. Contact not added.")
        return

    phone = input("Enter phone number: ").strip()

    # Basic phone validation (digits only)
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

    # Optional enhancement: alphabetical sorting
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
