import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from DataStore import variab
from DataStore.key_token import token
from Tools import parser, cust_json

from Handlers.greeting import router as greeting_router, storage
from Handlers.tools import router as tools_router

async def main() -> None:
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(greeting_router)
    dp.include_router(tools_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())