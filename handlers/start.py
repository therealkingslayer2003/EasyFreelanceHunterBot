from aiogram import types, Dispatcher

from create_bot import bot
from keyboards.start import start_new_user_kb, start_old_user_KB
from data_base import sqlite_base


# команда старт
async def command_start(message: types.Message):
    start_text = f"*Добро пожаловать, {message.from_user.full_name} 🚀*\n\nС помощью этого бота ты сможешь с лёгкостью " \
                 f"искать заказы сразу на всех фриланс биражах, используя фильтры и ключевые слова\.\n" \
                 f"Для корректной работы бота нужно пройти начальную настройку ⬇️"

    # проверка, новый ли пользователь
    if sqlite_base.sql_get(message.from_user.id):
        start_keyboard = start_old_user_KB
        start_text += "\n\n*Похоже ты уже использовал нашего бота\!*\nТы можешь заново настроить бота или сразу " \
                      "перейти к поиску заказов по заранее заданым настройкам ⬇️"
    else:
        start_keyboard = start_new_user_kb

    await bot.send_message(message.from_user.id, text=start_text, parse_mode="MarkDownV2", reply_markup=start_keyboard)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
