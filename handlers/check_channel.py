from aiogram import Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from db import ClientOnlyfans
from handlers.statese import *
from aiogram.fsm.context import FSMContext
from keyboards.funcs import list_users
import asyncio



router = Router(name='messages')
router.message.filter(F.chat.id==-690172865)



@router.message(Command('add', prefix='/'))
async def cmd_add(message: Message, session: AsyncSession):
    user = message.text.replace('/add', '').strip()
    if message.text == '/add@onlyk_sjidhglkasj_bot':
        await message.reply(text=f'Укажите имя после команды (пример: <code>/add Petr</code>)',
                            parse_mode='html')
    elif len(user)>0:
        try:
            await session.merge(ClientOnlyfans(name=user))
            await session.commit()
        except Exception as ex:
            print(f"{ex}")
        else:
            msg = await message.reply(text=f'{user} успешно добавлен')
            await asyncio.sleep(4)
            await message.delete()
            await msg.delete()
    else:
        await message.reply(text=f'Укажите имя после команды (пример: <code>/add Petr</code>)',
                            parse_mode='html')

@router.message(Command('update', prefix='/'))
async def cmd_update(message: Message, session: AsyncSession, state : FSMContext, bot):
    try:
        await In_user_about(message, bot, state, session)
    except:
        await message.reply('Перейди в бота, чтобы он мог отправлять тебе сообщения')
    await message.delete()


@router.message(Command('all_users', prefix='/'))
async def cmd_all(message: Message, session: AsyncSession):
    keyb = await list_users(session)
    if keyb:
        await message.answer(text='Все клиенты⤵️',
                            reply_markup=keyb.as_markup())
    else:
        await message.answer(text='В базе еще нету клиентов')
    await message.delete()


@router.message(Command('help', prefix='/'))
async def help_message(message: Message, session: AsyncSession):
    await message.answer(text=f"/all_users - команда для вывода списка всех клиентов\
                         \n/add - команда для добавления клиента (пример <code>/add Petr</code>)\
                         \n/help - команда для вывода этого сообщения\
                         \n/update - команда для добавления информации о клиенте или удаления клиента из базы. Чтобы работало все корректно, сначала нужно запустить бот (зайти в бот -> Начать)",
                         parse_mode='html')
    await message.delete()

