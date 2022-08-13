from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN

storage = MemoryStorage()


# машина состояний
class StatesMachine(StatesGroup):
    waiting_for_sites = State()
    waiting_for_categories = State()
    waiting_for_mode = State()
    waiting_for_keywords = State()
    waiting_for_prices = State()
    waiting_for_responses = State()
    waiting_for_frequency = State()
    active_searching = State()


# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
