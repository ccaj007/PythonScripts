'''
Imagine you are designing a simple contact management system. Write two Python classes:
1.  Contact, which holds information about an individual contact (name, phone number, and email).
    •   It should include a constructor (__init__) that initializes these attributes.
    •   It should have a method (e.g., update_phone) to change the phone number.
2.  ContactBook, which stores multiple Contact objects.
    •   It should include a constructor that initializes an empty list of contacts.
    •   It should allow adding a new contact, but not allow duplicate contacts
    •   It should allow removing a contact by name.
    •   It should allow searching for a contact by name and returning the matching Contact (or None if not found).
'''
from dataclasses import dataclass
@dataclass
class Contact:
    name: str
    phone: str
    email: str

    # def __init__(self, name, phone, email):
    #     self.name = name
    #     self.phone = phone
    #     self.email = email

    def update_phone(self, new_phone):
        self.phone = new_phone

    # def __str__(self):
    #     return f"name: {self.name} phone: {self.phone} email: {self.email}"

@dataclass
class ContactBook:
    contacts = []

    def add_contact(self, contact: Contact):
        if any(c.name == contact.name for c in self.contacts):
            print(f"contact {contact.name} is already in contact book")
        else:
            self.contacts.append(contact)

    def remove_contact(self, contact: Contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
        else:
            print(f"contact: {contact} does not exist in contact book")

    def search_contact(self, contact: Contact):
        if contact in self.contacts:
            print(f"contact found, {self.contacts}")

if __name__ == '__main__':


    # # Create a contact book
    # contact_book = ContactBook()

    # Add contacts
    contact1 = Contact(name="Alice", phone="123-456-7890", email="alice@example.com")
    contact2 = Contact(name="Bob", phone="987-654-3210", email="bob@example.com")
    contact3 = Contact(name="Bob", phone="3210", email="bob2@example.com")
    # print(contact1)
    # contact1.update_phone('555-1211')
    # print(contact1)

    contact_book = ContactBook()

    contact_book.add_contact(contact1)
    contact_book.add_contact(contact2)
    contact_book.add_contact(contact3)  # Attempt to add a duplicate


    print("\nContact Book:")
    print(contact_book)

    # # Remove a contact
    # contact_book.remove_contact("Alice")

    # print("\nContact Book after removal:")
    # print(contact_book)

    # # Find a contact
    # found_contact = contact_book.find_contact("Bob")
    # print("\nFound Contact:", found_contact)
