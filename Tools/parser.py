import requests
from bs4 import BeautifulSoup
import json
from time import localtime

from Tools.all_parser import link_from_user, all_links, update_data_json
from Tools.cust_json import load_all_users, load_from_file


def get_data_tusur(link: str) -> dict:

    responce = requests.get(link).text
    soup = BeautifulSoup(responce, "lxml")
    all_block = soup.find_all("table")
    all_block.pop(0)
    all_block.pop(0)

    DATA = {}

    def clean_str(stroke, time_bool=False):
        day_data = stroke.replace(" ", "")
        if time_bool == False:
            day_data = day_data.replace("\n", "")
        else:
            day_data = day_data.replace("\n", "|")
        day_data = day_data.replace(".", "")
        return  day_data

    def day_f(day_block):
        day_data = day_block.find_all("tr")[0].text
        day_data = clean_str(day_data)

        ls_data = day_data.split(",")
        return ls_data

    def time_l(lecs_data):
        stroke = lecs_data.find_all("th")[0].text
        stroke = clean_str(stroke, True)
        time_ls = stroke.split("|")
        time_ls.remove('')
        time_ls.remove('')
        time_sl = {"start_time":time_ls[0], "end_time":time_ls[1]}
        return  time_sl

    def all_data_day(day_block):
        name = ""
        type = ""
        adress = ""
        prepod = ""
        note = ""
        stroke = day_block.find_all('td')[0]
        try:
            stroke = stroke.find_all("div")[0]
            stroke = stroke.find_all("div")[0]
            stroke = stroke.find_all("div")[1]
            stroke = stroke.find_all("span")
            name = stroke[0].text
            type = stroke[1].text
            adress = stroke[2].text
            prepod = stroke[3].text
            note = stroke[4].text
        except:
            stroke = ""

        data_sl = {"name":name, "type":type, "adress":adress, "prepod":prepod, "note":note}
        return data_sl


    def lecsion(day_block):
        day_data = day_block.find_all("tr")
        day_data.pop(0)
        count = 0
        finish_data = {}
        for i in day_data:
            count += 1

            time = time_l(day_data[0])
            data = all_data_day(i)
            finish_data[count] = {"time":time, "data":data}

        return finish_data



    # Перебор всех дней
    for i in all_block:
        day_block = i.find_all("tbody")[0]
        DATA[day_f(day_block)[1]] = lecsion(day_block)

    DATA_links: dict = {}
    DATA_links[link] = DATA.copy()
    update_data_json(DATA_links)

    return DATA


def sorted_data_for_message(data: dict) -> str:
    pass


# для отправки сообщении
def get_data_for_message(faculty: str = "rkf", num_group: str = '234-2',
                         mode_json: bool = False) -> str:
    def format_schedule_simple(schedule):
        times_ls: list[str] = ["08:50 \\- 10:25",
                               "10:40 \\- 12:15",
                               "13:15 \\- 14:50",
                               "15:00 \\- 16:35",
                               "16:45 \\- 18:20",
                               "18:30 \\- 20:05",
                               "20:15 \\- 21:50"]
        result = []
        for key, value in schedule.items():
            data_info = value['data']


            if data_info['name']:  # Проверяем, есть ли название предмета
                entry = f"""\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_
*№ {key}: \\| {data_info['name']}*
{times_ls[int(key)-1]} \\|  {data_info['type']}
{data_info['adress']}"""
                result.append(entry)
            else:
                entry = (
                    f"№{key}: {times_ls[int(key) - 1]} \\| пустота\n"
                    ""
                )
                result.append(entry)

        return "\n".join(result)


    mounts: list[str] = ["янв", "фев", "мар", "апр",
                         "май", "июн", "июл", "авг",
                         "сен", "окт", "нояб", "дек"]
    count_day = str(localtime().tm_mday)
    if len(count_day) == 1:
        count_day = "0"+count_day
    time_data_str: str = count_day+str(mounts[localtime().tm_mon-1])

    if localtime().tm_wday == 6:
        return "Сегодня выходной, отдохните как следует!"

    my_link = f"https://timetable.tusur.ru/faculties/{faculty}/groups/{num_group}"
    try:
        datas = load_from_file("DataStore/all_data.json")
        DATA: dict = datas[my_link]
    except:
        DATA: dict = get_data_tusur(my_link)


    data_day: dict = DATA[time_data_str]



    # перебор расписании
    for i in data_day.copy():
        i = int(i)
        bol: bool

        try:
            bol = data_day[8-i]["data"]["name"] == ""
        except:
            bol = data_day[str(8 - i)]["data"]["name"] == ""

        if bol:
            try:
                del data_day[8-i]
            except:
                del data_day[str(8 - i)]
        else:
            break




    return format_schedule_simple(data_day)


def check_accuraty_reg(faculty: str, num_group: str) -> bool:
    status: int = requests.get(f'https://timetable.tusur.ru/faculties/{faculty}/groups/{num_group}').status_code
    if status == 200:
        return True
    else:
        return False



if __name__ == "__main__":
    print(get_data_for_message())



