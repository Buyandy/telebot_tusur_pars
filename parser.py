import requests
from bs4 import BeautifulSoup
import json


def get_data_tusur() -> dict:
    link = "https://timetable.tusur.ru/faculties/rkf/groups/234-2"

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

    return DATA






