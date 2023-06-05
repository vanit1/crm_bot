from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import ClientOnlyfans
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.funcs import *


router = Router(name="callbacks-router")

class UserInfo(StatesGroup):
    info_user = State()


@router.callback_query(F.data.startswith('upt_'))
async def actions(callback: CallbackQuery, session : AsyncSession):
    await callback.message.delete()
    id_us = int(callback.data.split('_')[1])
    users = await session.scalar(select(ClientOnlyfans).where(ClientOnlyfans.user_id == id_us))
    txt = users.info_user if users.info_user else 'Нету информации'
    #----------------------------------------------------------------
    #Клавиатура для действий с юзером
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Удалить клиента из базы",
                        callback_data=f"del_{id_us}")
    builder.button(text=f"Добавить данные о клиенте",
                        callback_data=f"add_{id_us}")
    builder.adjust(2)
    #----------------------------------------------------------------

    username = ''
    try:
        username = callback.from_user.username
    except:
        pass
    await callback.message.answer(text=f"Клиент: {users.name} 🆔{users.user_id}\nИнформация о пользователе: {txt}",
                                  disable_web_page_preview=True,
                                  reply_markup=builder.as_markup())
    

@router.callback_query(F.data.startswith('add_'))
async def add_user_from_base(callback: CallbackQuery, session : AsyncSession, state : FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    id_us = int(callback.data.split('_')[1])
    users = await session.scalar(select(ClientOnlyfans).where(ClientOnlyfans.user_id == id_us))
    us_name = users.name
    kb = cancel_handl()
    mess = await callback.message.answer(text=f"Введите информацию для 👤Пользователь: {us_name}",
                                  reply_markup=kb.as_markup())
    data['id_key'] = id_us
    data['messag'] = mess
    await state.set_data(data)
    await state.set_state(UserInfo.info_user)

@router.message(UserInfo.info_user)
async def fsm_user_from_base(message: Message, session : AsyncSession, state : FSMContext):
    txt = message.html_text
    inf_of_user = await state.get_data()
    await inf_of_user['messag'].delete()
    id_of_user = inf_of_user['id_key']
    user = await session.scalar(select(ClientOnlyfans).where(ClientOnlyfans.user_id == id_of_user))
    user_name = user.name
    user_text = user.info_user if user.info_user else ''
    await session.execute(update(ClientOnlyfans).where(ClientOnlyfans.user_id == id_of_user).values(info_user=f"{user_text}\n{txt}"))
    await session.commit()
    await message.answer(text=f"Информация о {user_name} обновлена")
    await state.clear()
    
@router.callback_query(F.data.startswith('del_'))
async def del_user_from_base(callback: CallbackQuery, session : AsyncSession):
    await callback.message.delete()
    id_us = int(callback.data.split('_')[1])
    users = await session.scalar(select(ClientOnlyfans).where(ClientOnlyfans.user_id == id_us))
    us_name = users.name
    try:
        sql = delete(ClientOnlyfans).where(ClientOnlyfans.user_id ==id_us)
        await session.execute(sql)
        await session.commit()
        await callback.message.answer(text=f"Пользователь: {us_name} был успешно удален с базы")
    except Exception as ex:
        await callback.message.answer(text=f"Ошибка: {ex}")


@router.callback_query(F.data == 'cancel')
async def add_user_from_base(callback: CallbackQuery, session : AsyncSession, state : FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(
        text="Действие отменено"
    )


@router.callback_query(F.data.startswith('_'))
async def full_users_list(callback: CallbackQuery, session : AsyncSession):
    await callback.message.delete()
    id_us = int(callback.data.split('_')[1])
    users = await session.scalar(select(ClientOnlyfans).where(ClientOnlyfans.user_id == id_us))
    txt = users.info_user if users.info_user else 'Нету информации'
    username = ''
    try:
        username = callback.from_user.username
    except:
        pass
    await callback.message.answer(text=f"Клиент: {users.name} 🆔{users.user_id}\nИнформация о пользователе: {txt}",
                                  disable_web_page_preview=True,
                                  parse_mode='html')