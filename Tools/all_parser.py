from asyncio import sleep
from datetime import datetime

from Tools import parser, cust_json
from Tools.cust_json import load_from_file






if __name__ == "__main__":
    data = pars_all_links()
    update_data_json(data)