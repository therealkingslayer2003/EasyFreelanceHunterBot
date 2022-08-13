from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data_base import sqlite_base
from create_bot import bot, StatesMachine


async def setup_settings(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите сайты:")
    await StatesMachine.waiting_for_sites.set()


# выбор биржи
async def choose_sites(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(sites=message.text)
    await bot.send_message(message.from_user.id, "Выберите категории:")
    await StatesMachine.next()


# выбор категорий
async def choose_categories(message: types.Message, state: FSMContext):
    await state.update_data(categories=message.text)
    await bot.send_message(message.from_user.id, "Выберите режим:")
    await StatesMachine.next()


# выбор режима
async def choose_mode(message: types.Message, state: FSMContext):
    await state.update_data(mode=message.text)
    await bot.send_message(message.from_user.id, "Выберите ключевые слова:")
    await StatesMachine.next()


# выбор ключевых слов
async def choose_keywords(message: types.Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await bot.send_message(message.from_user.id, "Выберите ценовой диапазон:")
    await StatesMachine.next()


# выбор ценового диапазона
async def choose_prices(message: types.Message, state: FSMContext):
    await state.update_data(prices=message.text)
    await bot.send_message(message.from_user.id, "Выберите кол-во откликов:")
    await StatesMachine.next()


# выбор кол-ва откликов
async def choose_responses(message: types.Message, state: FSMContext):
    await state.update_data(responses=message.text)
    await bot.send_message(message.from_user.id, "Выберите частоту сообщений:")
    await StatesMachine.next()


# выбор частоты сообщений
# уведомление об завершении настройки. Добавление данных в БД
async def choose_frequency(message: types.Message, state: FSMContext):
    await state.update_data(frequency=message.text)
    await sqlite_base.sql_add(state)
    await message.answer("Successfully!")
    await state.finish()


# Регистрация хендлеров
def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(choose_sites, state=StatesMachine.waiting_for_sites)
    dp.register_message_handler(choose_categories, state=StatesMachine.waiting_for_categories)
    dp.register_message_handler(choose_mode, state=StatesMachine.waiting_for_mode)
    dp.register_message_handler(choose_keywords, state=StatesMachine.waiting_for_keywords)
    dp.register_message_handler(choose_prices, state=StatesMachine.waiting_for_prices)
    dp.register_message_handler(choose_responses, state=StatesMachine.waiting_for_responses)
    dp.register_message_handler(choose_frequency, state=StatesMachine.waiting_for_frequency)
