import json
import dataclasses
from aiogram.types import Message

def load_from_file(file_dir: str) -> dict:
    try:
        with open(file_dir, "r", encoding="utf-8") as file:
            user_data: dict = json.load(file)
        return user_data
    except:
        return {"":""}

def save_add_from_file(file_dir: str, message_new: Message, users_data_old: dict,
                       faculty: str = "", num_group: str = "") -> None:

    is_user_new: bool = True

    for i in users_data_old.keys():
        if i == str(message_new.from_user.id):
            is_user_new = False

    file_for_save: dict[str:str] = {
        "id": str(message_new.from_user.id),
        "first_name": message_new.from_user.first_name,
        "last_name": message_new.from_user.last_name,
        "username": message_new.from_user.username,
        "is_bot": message_new.from_user.is_bot,
        "language_code": message_new.from_user.language_code
    }

    if faculty != "":
        file_for_save["faculty"] = faculty
    if num_group != "":
        file_for_save["num_group"] = num_group


    users_data_old[str(message_new.from_user.id)] = file_for_save

    with open(file_dir, "w", encoding="utf-8") as file:
        json.dump(users_data_old, file, ensure_ascii=False, indent=4)


def check_user_in_file(message: Message) -> bool:
    users_data: dict = load_from_file("DataStore/users.json")
    for i in users_data.keys():
        print(i)
        if i == str(message.from_user.id):
            return True

    return False

def auto_save_add(message: Message, faculty: str = "", num_group: str = "") -> None:
    users_data: dict = load_from_file("DataStore/users.json")
    save_add_from_file("DataStore/users.json", message, users_data,
                       faculty, num_group)

def load_data_user(id_user: str) -> dict:
    try:
        return load_from_file("DataStore/users.json")[id_user]
    except:
        return {"id":""}

