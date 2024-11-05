import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from DataStore.key_token import token
from Tools import cust_json, all_parser

from Handlers.greeting import router as greeting_router, storage
from Handlers.tools import router as tools_router

async def launch_bot(users: dict, bot: Bot) -> None:
    for i in users.keys():
        try:
            await bot.send_message(chat_id=int(i), text="""Бот парсер обновлен:

+ Быстрее вытаскивает данные с тусура.
+ Более понятный показ расписании.
+ Исправление мелких багов.""")
        except:
            pass


async def main() -> None:
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(greeting_router)
    dp.include_router(tools_router)

    asyncio.create_task(all_parser.auto_update_all_data())
    await launch_bot(cust_json.load_from_file("DataStore/users.json"), bot=bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())