from functools import wraps

from collections import UserDict

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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Error: Give me name and phone please"
        except KeyError as e:
            return f"Contact '{e.args[0]}' not found"
        except IndexError:
            return f"Error: Enter user name"
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
    
    if record is not None:
        record.edit_phone(phone_old, phone_new)
        return "Contact updated"
    return f"contact '{name}' not founde"


@input_error
def find_phone(args, book: AddressBook):
    # name_to_find = args[0]
    # for name, phone in contacts.items():
    #     if name.lower() == name_to_find.lower():
    #         return f"The phone number for {name}: {phone}"
    # raise KeyError(name_to_find)
    name_to_find = args[0]
    record = book.find(name_to_find)
    if record is not None:
        return record
    return f"Contact '{name_to_find} note founde"

# def show_all(contacts):
    # if not contacts:
    #     return "Your contact list is empty."
    
    # result = []
    # for name, phone in contacts.items():
    #     result.append(f"{name}: {phone}")
    # return "\n".join(result)

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
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()