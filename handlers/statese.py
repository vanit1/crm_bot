from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message
from keyboards.funcs import list_users
from aiogram.types import *
from sqlalchemy.ext.asyncio import AsyncSession

async def In_user_about(message : Message, bot : Bot, state : FSMContext, session : AsyncSession):
    keyb = await list_users(session, upt=True)
    if keyb:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Выбери клиента",
            reply_markup=keyb.as_markup())
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="В базе пока нету ни одного клиента")
    # Устанавливаем пользователю состояние "выбирает название"
