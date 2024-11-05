import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Handlers.tools_handlers.reg_user import reg_greet
from Tools import cust_json, parser
from DataStore import variab
from Tools.cust_json import load_from_file, load_data_user
from Tools.keyboard_aio import get_reply_keyboard_back_reg

router = Router()

@router.message(lambda message: message.text == "Расписание на сегодня")
async def b_parsing_and_send(message: Message, bot, state: FSMContext):


    user_data = load_data_user(str(message.from_user.id))
    if user_data["id"] == str(message.from_user.id):
        if not str(message.from_user.id) in variab.is_user_get_pars:
            try:
                variab.is_user_get_pars.append(str(message.from_user.id))
                mess1 = await message.answer(text="Вытаскиваю данные из сайта...")
                DATA: str = parser.get_data_for_message(faculty=user_data["faculty"], num_group=user_data["num_group"])
                await bot.edit_message_text(text=DATA,
                                            chat_id=message.chat.id,
                                            message_id=mess1.message_id,
                                            parse_mode="MarkdownV2")
                variab.is_user_get_pars.remove(str(message.from_user.id))
            except:
                await message.answer(text="Ошибка!\nЯ не смог стырить у тусура расписание,\nпростите(")
                variab.is_user_get_pars.remove(str(message.from_user.id))

        else:
            await message.answer(text="Ваш запрос еще не обработан!")
    else:
        await message.answer("У нас нету данных о вас, чтобы показать вам расписания 😕\nЗарегистрируем вас! 😊")
        await asyncio.sleep(1.0)
        await reg_greet(message,state)

@router.message(lambda message: message.text == "Заново регнутся")
async def restart_reg(message: Message, state: FSMContext):
    await message.answer(text="🔄 Restarting регистрация начата: 🔄", reply_markup=get_reply_keyboard_back_reg())
    await reg_greet(message, state)