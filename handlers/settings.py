from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from create_bot import bot
from data_base import sqlite_base
from keyboards.settings import sites_kb, categories_kb, mode_kb


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


# начало настройки
async def setup_settings(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.message.from_user.id)
    await StatesMachine.waiting_for_sites.set()

    callback.data = "first_start"
    await choose_sites(callback, state)


# выбор биржи
async def choose_sites(callback: CallbackQuery, state: FSMContext):
    # первый запуск функции
    if callback.data == "first_start":
        await state.update_data(chosen_sites=[])

    await callback.answer()
    chosen_sites = (await state.get_data())["chosen_sites"]

    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") in chosen_sites:
            chosen_sites.remove(callback.data.replace("chosen ", ""))
        else:
            chosen_sites.append(callback.data.replace("chosen ", ""))
        await state.update_data(chosen_sites=chosen_sites)

    elif callback.data == "step_ahead":
        callback.data = "first_start"
        await StatesMachine.next()
        await choose_categories(callback, state)
        return

    await callback.message.edit_text("Выберите сайты:", reply_markup=sites_kb(chosen_sites))


# выбор категорий
async def choose_categories(callback: CallbackQuery, state: FSMContext):
    # первый запуск функции
    if callback.data == "first_start":
        await state.update_data(chosen_categories=[])

    await callback.answer()
    chosen_categories = (await state.get_data())["chosen_categories"]

    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") in chosen_categories:
            chosen_categories.remove(callback.data.replace("chosen ", ""))
        else:
            chosen_categories.append(callback.data.replace("chosen ", ""))
        await state.update_data(chosen_categories=chosen_categories)

    elif callback.data == "step_ahead":
        callback.data = "first_start"
        await StatesMachine.next()
        await choose_mode(callback, state)
        return

    await callback.message.edit_text("Выберите категории:", reply_markup=categories_kb(chosen_categories))


# выбор категорий
async def choose_mode(callback: CallbackQuery, state: FSMContext):
    # первый запуск функции
    if callback.data == "first_start":
        await state.update_data(mode="keywords")

    await callback.answer()
    mode = (await state.get_data())["mode"]

    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") == mode:
            await callback.answer()
            return
        else:
            if mode == "basic":
                mode = "keywords"
            else:
                mode = "basic"
        await state.update_data(mode=mode)

    elif callback.data == "step_ahead":
        callback.data = "first_start"
        await StatesMachine.next()
        await choose_categories(callback, state)
        return

    await callback.message.edit_text("Выберите режим:", reply_markup=mode_kb(mode))

# # выбор режима
# async def choose_mode(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(mode=message.text)
#     await calmessage.from_user.id, "Выберите ключевые слова:")
#     await StatesMachine.next()


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
    dp.register_callback_query_handler(setup_settings, text="start_settings")
    dp.register_callback_query_handler(choose_sites,
                                       lambda call: call.data.startswith("chosen") or call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_sites)

    dp.register_callback_query_handler(choose_categories,
                                       lambda call: call.data.startswith("chosen") or call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_categories)
    dp.register_callback_query_handler(choose_mode,
                                       lambda call: call.data.startswith("chosen") or call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_mode)
    dp.register_message_handler(choose_keywords, state=StatesMachine.waiting_for_keywords)
    dp.register_message_handler(choose_prices, state=StatesMachine.waiting_for_prices)
    dp.register_message_handler(choose_responses, state=StatesMachine.waiting_for_responses)
    dp.register_message_handler(choose_frequency, state=StatesMachine.waiting_for_frequency)
