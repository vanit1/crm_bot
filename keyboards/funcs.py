from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.text import Text
from aiogram.types import Message, ContentType
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import ClientOnlyfans
from sqlalchemy import select, delete
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import *
from handlers.statese import *
from aiogram.fsm.context import FSMContext


async def list_users(session : AsyncSession, upt=False):
    users = await session.scalars(select(ClientOnlyfans))
    builder = InlineKeyboardBuilder()
    count_users = users.all()
    if count_users:
        if not upt:
            for user in count_users:
                builder.button(text=f"{user.name} (id: {user.user_id})",
                            callback_data=f"_{user.user_id}")
        else:
            for user in count_users:
                builder.button(text=f"{user.name} (id: {user.user_id})",
                            callback_data=f"upt_{user.user_id}")

        builder.adjust(3)
        return builder
    else:
        return None
    

def cancel_handl():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Отмена", callback_data='cancel')
    return builder

