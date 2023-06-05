from aiogram import types
from handlers import *
from db import BaseModel, async_engine_, get_session_maker, process_schemas
import os
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from middlewares import DbSessionMiddleware
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from commands_of_bot import set_ui_commands


load_dotenv()



async def main():
    bot = Bot(token=os.getenv('API_KEY'), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())


    async_engine = async_engine_(os.getenv('DATABASE'))
    session_maker = get_session_maker(async_engine)
    await process_schemas(async_engine, metadata=BaseModel.metadata)

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(callbacks.router)
    dp.include_router(check_channel.router)

    await set_ui_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass