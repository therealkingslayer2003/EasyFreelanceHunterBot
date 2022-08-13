from aiogram import types, Dispatcher
from create_bot import bot
from handlers.settings import setup_settings
from create_bot import StatesMachine


# команда старт
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Добро пожаловать,{message.from_user.full_name} !')
    await setup_settings(message)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
