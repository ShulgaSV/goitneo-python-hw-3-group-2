

from collections import UserDict
from datetime import datetime
from collections import defaultdict


class Birthday:
    def __init__(self, birthday) -> None:
        self.value = birthday


class Record:
    def __init__(self, name, birthday=None) -> None:
        self.name = name
        self.phones = []
        # if birthday:
        #     self.birthday = Birthday(birthday)
        # else:
        #     self.birthday = None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phone.append(phone) # self.phone.append(Phone(phone))


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record # self.data[record.name.value] = record
        return 'Contact added.'
    
    def show_birthdays_this_week(self):
        result_dict = defaultdict(list)
        # ... today = ...
        for name, record in self.data.items():
            if record.birthday:
                #... 
                birthday_date = datetime.strptime(record.birthday, '%d.%m.%Y')
                #...
                result_dict['Monday'].append(name)


