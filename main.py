from classes import Record, AddressBook



def add_record(args, book): # def add_record(args, contacts)
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    return book.add_record(record)


def main():
    book = AddressBook() # contacts = dict()
    while True:
        user_input = input(">>> ")
        command, *args = user_input.strip().split(' ')
        if command == 'add':
            book.add_record(args, book)

