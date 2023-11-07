import pickle
import json
from pathlib import Path
from pprint import pprint
from ab_classes import AddressBook, Record
from collections import defaultdict

save_file = Path("phone_book.bin")
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
def add_record(name: str, phone: str):
    global phone_book
    record = Record(name, phone)
    phone_book.add_record(record)
    # if not phone.isdecimal():
    #     raise ValueError
    # phone_book[name] = phone
    return f"{record}"


@input_error
def change_record(name: str, phone: str, new_phone: str):
    global phone_book
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
def find(search: str) -> str or None:
    # global phone_book
    rec = []
    if search.isdigit():
        for k, v in phone_book.items():
            if v.find_phone(search):
                rec.append(phone_book[k])
    else:
        for k,v in phone_book.items():
            if search in k: 
                rec = phone_book[k]
    if rec:
        result = "\n".join(list(map(str, rec)))
        return f"Finded \n{result}"


def show_all():
    global phone_book
    for p in phone_book.iterator():
        input(">>>Press Enter for next record")
        print(p)


def save_book() -> str:
    global phone_book
    with open(save_file, "wb") as file:
        pickle.dump(phone_book, file)
    return f"Phonebook saved"


def load_book() -> str:
    global phone_book
    with open(save_file, "rb") as file:
        loaded_book = pickle.load(file)
    for k, v in loaded_book.items():
        phone_book.data[k] = v
    return f"Phonebook loaded"


def stop_command(*args) -> str:
    return f"{save_book()}. Good bye!"


def unknown(*args):
    return "Unknown command. Try again."


COMMANDS = {greeting: "hello",
            add_record: "add",
            change_record: "change",
            find: "find",
            show_all: "show all",
            save_book: "save",
            load_book: "load",
            stop_command: ("good bye", "close", "exit")
            }


def parcer(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    if all([save_file.exists(), save_file.stat().st_size> 0]):
        print(load_book())
    while True:
        user_input = input(">>>")
        func, data = parcer(user_input)
        result = func(*data)
        print(result)
        if result == "Phonebook saved. Good bye!":
            break


if __name__ == "__main__":
    main()
