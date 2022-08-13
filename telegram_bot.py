from aiogram.utils import executor

from handlers import settings, start
from create_bot import dp, bot
from data_base import sqlite_base


async def on_startup(_):
    print("Bot successfully started")
    sqlite_base.sql_start()


async def on_shutdown(_):
    print("Bot shutdown")

start.register_handlers_start(dp)
settings.register_handlers_settings(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
