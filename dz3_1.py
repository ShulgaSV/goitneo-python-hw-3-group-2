
# Наш бот помічник Повна версія
# Це ОК якщо бот україномовний?


from collections import UserDict
from datetime import datetime, timedelta


class Field:                           # Клас для представлення поля контакту
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):                     # Клас для представлення поля з ім'ям контакту
    pass


class Phone(Field):                      # Клас для представлення поля з номером телефону контакту
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер телефону повинен містити 10 цифр")
        super().__init__(value)


class Birthday(Field):                     # Клас для представлення поля з днем народження контакту
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дня народження, повинен бути DD.MM.YYYY")
        super().__init__(value)


class Record:                             # Клас для представлення запису у адресну книгу
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone_num, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[phone_num] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        if self.birthday:
            return f"Контакт: {self.name}, телефони: {phone_str}, день народження: {self.birthday}"
        else:
            return f"Контакт: {self.name}, телефони: {phone_str}"


class AddressBook(UserDict):                # Клас для представлення адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    # Функція для отримання списку користувачів, яких потрібно привітати наступного тижня
    def get_birthdays_per_week(self):
        birthdays = {}
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                delta_days = (birthday_date - today).days
                if 0 <= delta_days < 7:
                    birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")
                    if birthday_weekday in ["Saturday", "Sunday"]:
                        birthday_weekday = "Monday"
                    if birthday_weekday not in birthdays:
                        birthdays[birthday_weekday] = []
                    birthdays[birthday_weekday].append(record.name.value)
        return birthdays


def input_error(func):                          # Декоратор для обробки помилок вводу
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Введіть ім'я користувача."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Неправильна кількість аргументів."

    return inner


def parse_input(user_input):                    # Функція для розбору введеної команди
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error                                 # Функція для додавання нового контакту
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Контакт додано."


@input_error                           # Функція для зміни номера телефону контакту
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.phones = [Phone(new_phone)]
        return "Контакт оновлено."
    else:
        return "Контакт не знайдено."


def show_phone(args, book):                  # Функція для показу номера телефону контакту
    name, = args
    record = book.find(name)
    if record:
        return f"Номер телефону для {name}: {record.phones[0]}"
    else:
        return "Контакт не знайдено."


def show_all(book):                                # Функція для відображення всіх контактів
    if book:
        for record in book.values():
            print(record)
    else:
        return "Контакти не знайдено."


@input_error
def add_birthday(args, book):                    # Функція для додавання дня народження до контакту
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "День народження додано."
    else:
        return "Контакт не знайдено."


@input_error                                    # Функція для показу дня народження контакту
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"День народження для {name}: {record.birthday}"
    else:
        return "День народження не знайдено."


def birthdays_this_week(book):                           # Функція для показу днів народження, які відбудуться наступного тижня
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        for day, names in birthdays.items():
            print(f"{day}: {', '.join(names)}")
    else:
        return "Немає днів народження на цьому тижні."


def main():                                          # Основна функція бота
    book = AddressBook()
    print("Ласкаво просимо до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Як я можу допомогти вам?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            birthdays_this_week(book)
        else:
            print("Неправильна команда.")

if __name__ == "__main__":
    main()

