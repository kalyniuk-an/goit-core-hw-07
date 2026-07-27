from functools import wraps
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_old = self.find_phone(old_phone)
        if not phone_old:
            raise ValueError(f"Phone number {old_phone} not found.")
        
        new_phone = Phone(new_phone)
        index = self.phones.index(phone_old)
        self.phones[index] = new_phone

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        # return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        phone_str = '; '.join(p.value for p in self.phones) if self.phones else " no phone"
        bday_str = f", brithday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phone: {phone_str}{bday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming = []
        today = datetime.today().date()
        end_date = today + timedelta(days=7)

        for record in self.data.values():
            if not record.birthday:
                continue
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year+1)
            if today <= birthday_this_year <= end_date:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year += timedelta(days=7-birthday_this_year.weekday())
                upcoming.append({
                    "name": record.name.value,
                    "birthday": birthday_this_year.strftime("%d.%m.%Y")
                })

        return upcoming

    def __str__(self):
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            msg = str(e)
            if "not enough values to unpack" in msg or "too many values to unpack" in msg:
                return "Error: Invalid number of arguments. Please provide all required detailes."
            return f"Error: {msg}"
        except KeyError as e:
            return f"Error: Contact '{e.args[0]}' not found"
        except IndexError:
            return "Error: Enter user name"
        except AttributeError:
            return "Error: Contact not found or missing field."
    return inner

def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, phone_old, phone_new = args
    record = book.find(name)
    record.edit_phone(phone_old, phone_new)
    return "Contact updated"

@input_error
def find_phone(args, book: AddressBook):
    name_to_find = args[0]
    record = book.find(name_to_find)
    return record

# def show_all(contacts):
    # if not contacts:
    #     return "Your contact list is empty."
    
    # result = []
    # for name, phone in contacts.items():
    #     result.append(f"{name}: {phone}")
    # return "\n".join(result)
@input_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.find(name)
    record.add_birthday(date)
    return f"Added birthday {date} for contact {name}"

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return f"Contact {name} has no birthday specified"
    return f"{name}'s birthday is on {record.birthday.value}"

@input_error
def birthdays(book: AddressBook):
    birthday_days = book.get_upcoming_birthdays()
    if not birthday_days:
        return "nothin"
    return "\n".join([f"{bd['name']}: {bd['birthday']}" for bd in birthday_days])

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(find_phone(args, contacts))
        elif command == "all":
            # print(show_all(contacts))
            print(contacts)
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
