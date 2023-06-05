from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats


async def set_ui_commands(bot: Bot):
    """
    Sets bot commands in UI
    :param bot: Bot instance
    """
    commands = [
        BotCommand(command="all_users", description="Список всех клиентов"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="update", description="Добавить информацию о клиенте")
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllGroupChats()
    )