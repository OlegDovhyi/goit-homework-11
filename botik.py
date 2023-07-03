import datetime
from collections import UserDict


class Field:
    def __init__(self):
        self.value = None

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):
    def __set__(self, instance, value):
        if value:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
                self.value = value
            except ValueError:
                raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD' format.")
        else:
            self.value = None


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name()
        self.name.value = name
        self.phones = []
        if birthday:
            self.birthday = Birthday()
            self.birthday.value = birthday
        else:
            self.birthday = None

    def add_phone(self, number):
        phone = Phone()
        phone.value = number
        self.phones.append(phone)

    def remove_phone(self, number):
        self.phones = [phone for phone in self.phones if str(phone) != number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if str(phone) == old_number:
                phone.value = new_number
                return f"Changed phone number for contact: {self.name.value}, {new_number}"
        return f"Phone number '{old_number}' not found for contact: {self.name.value}"

    def set_birthday(self, birthday):
        self.birthday.value = birthday

    def days_to_birthday(self):
        if self.birthday and self.birthday.value:
            today = datetime.date.today()
            next_birthday = datetime.datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return "Birthday not set"


    def __str__(self):
        result = f"Name: {self.name}\n"
        result += f"Birthday: {self.birthday}\n"
        result += "Phones:\n"
        for phone in self.phones:
            result += f"- {phone}\n"
        return result.strip()


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def remove_record(self, name):
        del self.data[name]

    def __str__(self):
        result = ""
        for record in self.data.values():
            result += f"{record}\n\n"
        return result.strip()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Invalid command."

    return inner


contacts = AddressBook()


@input_error
def add_contact(name, phone=None, birthday=None):
    if name in contacts:
        return f"Contact '{name}' already exists."
    record = Record(name, birthday)
    if phone:
        record.add_phone(phone)
    contacts.add_record(record)
    return f"Added contact: {name}, {phone}, {birthday}"


@input_error
def change_phone(name, new_phone):
    if name not in contacts:
        return f"Contact '{name}' not found."
    record = contacts[name]
    old_phone = record.phones[0].value if record.phones else None
    if old_phone:
        record.edit_phone(old_phone, new_phone)
        return f"Changed phone number for contact: {name}, {new_phone}"
    else:
        return f"No phone number found for contact: {name}. Cannot change."


@input_error
def get_phone(name):
    if name not in contacts:
        return f"Contact '{name}' not found."
    record = contacts[name]
    return f"Phone number for contact '{name}': {', '.join(str(phone) for phone in record.phones)}"


@input_error
def remove_contact(name):
    if name not in contacts:
        return f"Contact '{name}' not found."
    contacts.remove_record(name)
    return f"Removed contact: {name}"


def show_all_contacts():
    if not contacts:
        return "No contacts found."
    return str(contacts)


def main():
    print("How can I help you?")

    while True:
        command = input("> ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, *phone_birthday = command.split()
                phone = None
                birthday = None
                if phone_birthday:
                    phone = phone_birthday[0]
                if len(phone_birthday) > 1:
                    birthday = phone_birthday[1]
                print(add_contact(name, phone, birthday))
            except ValueError:
                print("Enter name and optional phone number and birthday, separated by a space.")
        elif command.startswith("change"):
            try:
                _, name, phone = command.split()
                print(change_phone(name, phone))
            except ValueError:
                print("Enter name and new phone number, separated by a space.")
        elif command.startswith("phone"):
            try:
                _, name = command.split()
                print(get_phone(name))
            except ValueError:
                print("Enter a name.")
        elif command.startswith("remove"):
            try:
                _, name = command.split()
                print(remove_contact(name))
            except ValueError:
                print("Enter a name.")
        elif command == "show all":
            print(show_all_contacts())
        elif command.startswith("birthday"):
            try:
                _, name = command.split()
                record = contacts[name]
                days_left = record.days_to_birthday()
                if days_left != "Birthday not set":
                    print(f"{days_left} days to {name}'s birthday")
                else:
                    print("Birthday not set for this contact.")
            except ValueError:
                print("Enter a name.")
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()

