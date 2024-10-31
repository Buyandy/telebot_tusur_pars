import asyncio

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from transliterate import translit

from Tools import cust_json, parser, keyboard_aio
from DataStore import variab

class Form(StatesGroup):
    waiting_faculty = State()
    waiting_num_group = State()




router = Router()

async def reg_greet(message: Message, state: FSMContext):
    mess1 = await message.answer(text="Выберите ваш факультет 🎓",
                                 reply_markup=keyboard_aio.get_inline_keyboard())
    await state.set_state(Form.waiting_faculty)
    await state.update_data(mess1=mess1)


@router.message(lambda message: message.text == "Отменить регистрацию")
async def reg_back(message: Message, state: FSMContext):
    await message.reply(text="Регистрация отменена ❌", reply_markup=keyboard_aio.get_reply_keyboard_main())
    await state.clear()

@router.callback_query(F.data, Form.waiting_faculty)
async def reg_fac(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(faculty=callback_query.data)
    mess1 = await state.get_data()
    await bot.edit_message_text(text="Напишите номер группы 📋", message_id=mess1.get("mess1").message_id,
                                chat_id=mess1.get("mess1").chat.id)
    await state.set_state(Form.waiting_num_group)


@router.message(Form.waiting_num_group)
async def rag_num_group(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    faculty = user_data.get("faculty")
    num_group = translit(value=message.text.lower(), language_code="ru", reversed=True)

    await message.answer(text="Проверяю доступность ссылки...")
    if parser.check_accuraty_reg(faculty=faculty, num_group=num_group):
        cust_json.auto_save_add(message, faculty=faculty, num_group=num_group)
        await message.answer(text="Регистрация пройдена, без багов и ошибок ✅",
                             reply_markup=keyboard_aio.get_reply_keyboard_main())
        if len(variab.is_user_reg_now) != 0:
            variab.is_user_reg_now.remove(str(message.from_user.id))
        await state.clear()
    else:
        await message.answer(text="Такой ссылки не существует ❌\nНачинаю процесс повторной регистрации 🔄")
        await asyncio.sleep(2.0)
        await reg_greet(message, state)


