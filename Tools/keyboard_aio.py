from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from DataStore import variab



def get_inline_keyboard() -> InlineKeyboardMarkup:
    all_faculty = variab.all_faculty
    builder = InlineKeyboardBuilder()
    for i in all_faculty:
        builder.row(
    InlineKeyboardButton(text=i[0][0], callback_data=i[0][1]),
            InlineKeyboardButton(text=i[1][0], callback_data=i[1][1]))

    inline_kb = builder.as_markup()
    return inline_kb

def get_reply_keyboard_main() -> ReplyKeyboardMarkup:
    buttons: list = [[KeyboardButton(text="Расписание на сегодня")],
                     [KeyboardButton(text="Заново регнутся")]]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return kb

def get_reply_keyboard_back_reg() -> ReplyKeyboardMarkup:
    buttons: list = [[KeyboardButton(text="Отменить регистрацию")]]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return kb