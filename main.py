from pprint import pprint
from ab_classes import AddressBook, Record
from collections import defaultdict

phone_book = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except TypeError:
            return "Not enough params. Try again"
        except KeyError:
            return "Unknown name. Try again"
        except ValueError:
            return "Wrong phone number. Try again"
    return inner

def greeting(*args):
    return "How can I help you?"
    

@input_error
def add_record(name: str, phone:str):
    record = Record(name, phone)
    phone_book.add_record(record)
    # if not phone.isdecimal():
    #     raise ValueError
    # phone_book[name] = phone
    return f"{record}"

@input_error
def change_record(name:str, phone: str, new_phone: str):
    rec: Record = phone_book.find(name)
    if rec:
        return rec.edit_phone(phone, new_phone)
    # if not new_phone.isdecimal():
    #     raise ValueError
    # rec = phone_book[name]
    # if rec:
    #     phone_book[name] = new_phone
    # return f"Changed phone {name=} {new_phone=}"

@input_error
def find_phone(name):
    rec: Record = phone_book[name]
    if rec:
        phones = "; ".join(rec.phones)
        return f"Finded {rec.name}: {phones}"

def show_all():
    for p in phone_book.iterator():
        input(">>>Press Enter for next record")
        print(p)

def stop_command(*args):
    return "Good bye!"

def unknown(*args):
    return "Unknown command. Try again."

COMMANDS = {greeting: "hello",
            add_record: "add",
            change_record: "change",
            find_phone: "phone",
            show_all: "show all",
            stop_command: ("good bye", "close", "exit")
            }

def parcer(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(">>>")
        func, data = parcer(user_input)
        result = func(*data)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()