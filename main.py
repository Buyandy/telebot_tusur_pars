from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import env
import parser

token = "7400947530:AAHd_93JgvWv-44HzbC38hIMohIxSgZymDM"
bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def b_started(message: Message):
    await message.reply(text=env.mess_hello_str)

@dp.message(Command(commands='pars'))
async def b_parsing_and_send(message: Message):
    mess1 = await message.answer(text="Вытаскиваю данные из сайта...")
    DATA = parser.get_data_for_message()
    await bot.edit_message_text(text=DATA,
                                chat_id=message.chat.id,
                                message_id=mess1.message_id)


if __name__ == "__main__":
    dp.run_polling(bot)