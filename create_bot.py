from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from config import TOKEN

storage = MemoryStorage()


# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
