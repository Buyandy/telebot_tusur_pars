from asyncio import sleep
from datetime import datetime

from Tools import parser, cust_json
from Tools.cust_json import load_from_file


def link_from_user(user: dict) -> str:
    try:
        faculty: str = user["faculty"]
        num_group: str = user["num_group"]
        link: str = f"https://timetable.tusur.ru/faculties/{faculty}/groups/{num_group}"
        return link
    except:
        return "none"

def all_links(users: dict) -> list:
    links: list = []
    for i in users.keys():
        link: str = link_from_user(users[i])
        if link != "none" and not link in links:
            links.append(link)
    return links


def pars_all_links() -> dict:
    links: list[str] = all_links(cust_json.load_all_users())
    data_link: dict = {}
    for i in links:
        data_link[i] = parser.get_data_tusur(i)
    return data_link

def update_data_json(data_new: dict) -> None:
    old_data = load_from_file("DataStore/all_data.json")
    for i in data_new.keys():
        old_data[i] = data_new[i]
    cust_json.save_in_file("DataStore/all_data.json", old_data)

async def auto_update_all_data() -> None:

    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    all_data: dict = load_from_file("DataStore/all_data.json")
    count = 0
    try:
        for i in all_data.keys():
            count += 1
            if i != "":
                parser.get_data_tusur(i)
        print(f"Данные успешно обновились! {current_date_time}\n"
              f"Обновленно {count} ссылок.")
    except:
        print(f"Данные не обновились из-за ошибок, или из-за отсутствия ссылок.")
    await sleep(3600)



if __name__ == "__main__":
    data = pars_all_links()
    update_data_json(data)