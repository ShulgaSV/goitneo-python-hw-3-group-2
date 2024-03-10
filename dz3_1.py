

# Система для управління адресною книгою.


from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):            # Реалізовано валідацію номера телефону (має бути 10 цифр).
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):           # Додавання номера телефону до запису
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):         # Видалення номера телефону з запису
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):  # Редагування номера телефону у записі
        for phone_num, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[phone_num] = Phone(new_phone)
                break

    def find_phone(self, phone):            # Пошук номера телефону у записі
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record):              # Додавання записів
        
        self.data[record.name.value] = record

    def find(self, name):                     # Пошук записів за іменем
        
        return self.data.get(name)

    def delete(self, name):                    # Видалення записів за іменем
        
        del self.data[name]

if __name__ == "__main__":                   # Створення нової адресної книги
    
    book = AddressBook()