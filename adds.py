def add_birthday(args, book):
    name, birthday = args
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

def show_birthday(args, book):
    name = args[0]
    contact = book.find(name)
    if contact and contact.birthday:
        return f"{contact.name}'s birthday: {contact.birthday}"
    elif contact:
        return "Birthday not set for this contact."
    else:
        return "Contact not found."

def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return "\n".join(f"{name}'s birthday: {bday}" for name, bday in upcoming_birthdays)
    else:
        return "No