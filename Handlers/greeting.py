import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

#FSM
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pyexpat.errors import messages


from Tools import cust_json, parser, keyboard_aio
from DataStore import variab
from Handlers.tools_handlers.reg_user import router as router_reg_user
from Handlers.tools_handlers.reg_user import reg_greet, Form




storage = MemoryStorage()
router = Router()

def is_user_reg_now_func(user_id: str) -> bool:
    if len(variab.is_user_reg_now) == 0:
        variab.is_user_reg_now.append(user_id)
        return False
    users_reg_now: list[str] = variab.is_user_reg_now
    for i in users_reg_now:
        if user_id == i:
            return True
    variab.is_user_reg_now.append(user_id)
    return False



@router.message(CommandStart())
async def b_started(message: Message, state: FSMContext):
    file_photo: FSInputFile = FSInputFile("DataStore/photo/для_тусура.jpg")
    await message.answer_photo(caption=variab.mess_hello_str,
                        reply_markup=keyboard_aio.get_reply_keyboard_main(),
                               photo=file_photo)


@router.message(lambda message:(not (cust_json.check_user_in_file(message)) and
                                (not is_user_reg_now_func(str(message.from_user.id)))))
async def check_user(message: Message, state: FSMContext):
    await message.reply(text=variab.mess_reg)
    await asyncio.sleep(1.0)
    await reg_greet(message, state)




router.include_router(router_reg_user)



