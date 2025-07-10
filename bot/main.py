import readline
from .messages import MESSAGES
from .decorators import input_error
from .utils import parse_input
from address_book import AddressBook, Record


@input_error
def add_contact(args, contacts: AddressBook):
    try:
        name, phone, *_ = args
    except ValueError:
        raise ValueError("Expected: name and phone.")

    contact = contacts.find(name)
    if contact is None:
        contact = Record(name)
        contacts.add_record(contact)
    if phone:
        contact.add_phone(phone)
    return MESSAGES["add_success"]


@input_error
def change_contact(args, contacts):
    try:
        name, old_phone, new_phone, *_ = args
    except ValueError:
        raise ValueError("Expected: name, old phone, new phone.")

    contact = contacts.find(name)
    if contact:
        contact.edit_phone(old_phone, new_phone)
        return MESSAGES["change_success"]
    else:
        return MESSAGES["contact_not_found"]


@input_error
def show_phone(args, contacts):
    try:
        name, *_ = args
    except ValueError:
        raise ValueError("Expected: name.")

    contact = contacts.find(name)
    if contact:
        phones = contact.phones

        if not phones:
            return f"No phone numbers found for {name}."

        result = [f"\n📱 {name}'s phone numbers:"]
        
        for phone in phones:
            result.append(f" - {str(phone)}")

        return "\n".join(result)
    else:
        return MESSAGES["contact_not_found"]


@input_error
def show_all(contacts):
    if not contacts:
        return MESSAGES["all_empty"]
    result = [MESSAGES["all_header"]]

    for name, contact in contacts.items():
        result.append(MESSAGES["all_entry"](contact))
    return "\n".join(result)


@input_error
def show_help():
    return MESSAGES["help"]


@input_error
def add_birthday(args, contacts: AddressBook):
    try:
        name, birthday, *_ = args
    except ValueError:
        raise ValueError("Expected: name and birthday (in DD.MM.YYYY format).")

    contact = contacts.find(name)
    if contact is None:
        return MESSAGES["contact_not_found"]
    contact.add_birthday(birthday)
    return MESSAGES["birthday_added"]


@input_error
def show_birthday(args, contacts: AddressBook):
    try:
        name, *_ = args
    except ValueError:
        raise ValueError("Expected: name.")

    contact = contacts.find(name)
    if contact:
        birthday = contact.birthday
        if birthday is None:
            return MESSAGES["birthday_not_found"](name)
        return MESSAGES["birthday_found"](name, birthday.value)
    else:
        return MESSAGES["contact_not_found"]


@input_error
def birthdays(contacts: AddressBook):
    upcoming_birthdays = contacts.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "🎉 No birthdays in the next 7 days."

    result = ["\n📅 Upcoming birthdays next week:"]

    for user in upcoming_birthdays:
        result.append(f" - {user['name']}: {user['congratulation_date']}")

    return "\n".join(result)


def main():
    contacts = AddressBook()
    print(MESSAGES["welcome"])

    while True:
        user_input = input(MESSAGES["prompt"])
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            print(MESSAGES["goodbye"])
            break
        elif command == "hello":
            print(MESSAGES["greeting"])
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        elif command in ["help", "-h"]:
            print(show_help())
        else:
            print(MESSAGES["invalid"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(MESSAGES["goodbye"])
