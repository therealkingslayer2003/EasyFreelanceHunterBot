from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from keyboards.settings import sites_kb, categories_kb, mode_kb, currency_kb, settings_default_kb, prices_kb, \
    responses_kb
from utils import edited, is_valid


class StatesMachine(StatesGroup):
    waiting_for_sites = State()
    waiting_for_categories = State()
    waiting_for_mode = State()
    waiting_for_keywords = State()
    waiting_for_currency = State()
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

    # при нажатии на сайт
    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") in chosen_sites:
            chosen_sites.remove(callback.data.replace("chosen ", ""))
        else:
            chosen_sites.append(callback.data.replace("chosen ", ""))
        await state.update_data(chosen_sites=chosen_sites)

    # при нажатии "дальше"
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
        await state.update_data(chosen_category=None)

    await callback.answer()
    chosen_category = (await state.get_data())["chosen_category"]

    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") == chosen_category:
            await callback.answer()
            return
        else:
            chosen_category = callback.data.replace("chosen ", "")
            await state.update_data(chosen_category=chosen_category)

    elif callback.data == "step_ahead":
        callback.data = "first_start"
        await StatesMachine.next()
        await choose_mode(callback, state)
        return

    await callback.message.edit_text("Выберите категории:", reply_markup=categories_kb(chosen_category))


# выбор режима
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
            mode = callback.data.replace("chosen ", "")
        await state.update_data(mode=mode)

    elif callback.data == "step_ahead":
        callback.data = "first_start"
        if mode == "keywords":
            await StatesMachine.next()
            await choose_keywords(callback, state)
        else:
            await StatesMachine.waiting_for_currency.set()
            await choose_currency(callback, state)
        return

    await callback.message.edit_text("Выберите режим:", reply_markup=mode_kb(mode))


async def choose_keywords(callback, state: FSMContext):
    # первый запуск функции
    if type(callback) == CallbackQuery:
        if callback.data == "first_start":
            await state.update_data(keywords=[])
            message_id = \
                await callback.message.edit_text(f"Напишите ключевые слова:\n\n💡 Используйте слова или словосочетания"
                                                 f" без спецсимволов\. Только буквы, цифры и пробелы\n\n💡 Для добавления "
                                                 f"отправьте каждое ключевое слово отдельным сообщением\.\n\n"
                                                 f"💡 Для удаления отправьте ключевое слово, которое хотите удалить\n\n"
                                                 f"Ваши ключевые слова:\n", parse_mode="MarkDownV2",
                                                 reply_markup=settings_default_kb)

            await state.update_data(message_id=message_id)
        elif callback.data == "step_ahead":
            callback.data = "first_start"
            await StatesMachine.next()
            await choose_currency(callback, state)
            return
    else:
        message_id = (await state.get_data())["message_id"]
        keywords = (await state.get_data())["keywords"]
        if not is_valid(callback.text):
            await callback.delete()
            return
        callback.text = callback.text.lower()
        if callback.text in keywords:
            keywords.remove(callback.text)
        else:
            keywords.append(callback.text)
        await state.update_data(keywords=keywords)
        await callback.delete()

        text = ''
        for word in keywords:
            text += "🔘 " + word + "\n"

        await message_id.edit_text(f"Напишите ключевые слова:\n\n💡 Используйте слова или словосочетания"
                                   f" без спецсимволов\. Только буквы, цифры и пробелы\n\n💡 Для добавления "
                                   f"отправьте каждое ключевое слово отдельным сообщением\.\n\n"
                                   f"💡 Для удаления отправьте ключевое слово, которое хотите удалить\n\n"
                                   f"Ваши ключевые слова:\n*{text}*", parse_mode="MarkDownV2",
                                   reply_markup=settings_default_kb)


async def choose_currency(callback: CallbackQuery, state: FSMContext):
    # первый запуск функции
    if callback.data == "first_start":
        await state.update_data(chosen_currency=None)

    await callback.answer()
    chosen_currency = (await state.get_data())["chosen_currency"]

    # при нажатии на валюту
    if callback.data.startswith("chosen"):
        if callback.data.replace("chosen ", "") == chosen_currency:
            await callback.answer()
            return
        else:
            chosen_currency = callback.data.replace("chosen ", "")
            await state.update_data(chosen_currency=chosen_currency)

    # при нажатии "дальше"
    elif callback.data == "step_ahead":
        callback.data = "first_start"
        await StatesMachine.next()
        await choose_prices(callback, state)
        return

    await callback.message.edit_text("Выберите валюту, в которой будут отображаться заказы:\n\n"
                                     "💡 При отображении заказов с различных фриланс бирж, цена будет конвертироваться "
                                     "в выбранную вами валюту по актуальному курсу\.\n\n"
                                     "💡 Мы используем официальные курсы валют из доверенного и всемирно признанного"
                                     " [источника](https://www.xe.com/company/)\.", disable_web_page_preview=True,
                                     parse_mode="MarkDownV2",
                                     reply_markup=currency_kb(chosen_currency))


async def choose_prices(callback, state: FSMContext):
    if type(callback) == CallbackQuery:
        if callback.data == "first_start":
            await state.update_data(prices=[None, None])

            message_id = \
                await callback.message.edit_text(f"Напишите ценовой диапазон поиска заказов:\n\n💡 Вам будут показаны "
                                                 f"заказы только в выбранном вам ценновом диапазоне\. Для отображения "
                                                 f"заказов с любой ценой нажмите соотвествующую кнопку снизу\.\n\n"
                                                 f"💡 Для добавления минимальной цены заказа напишите \"от \*цена\*\" и"
                                                 f" отправьте данное сообщение боту\.\n*Например:*\n_от 500_\n\n"
                                                 f"💡 Для добавления маскимальной цены заказа напишите \"до \*цена\*\" и"
                                                 f" отправьте данное сообщение боту\.\n*Например:*\n_до 5000_\n\n"
                                                 f"*Выбранный вами ценовой диапазон:*\nОтображать заказы с любой ценой ✅",
                                                 parse_mode="MarkDownV2",
                                                 reply_markup=prices_kb)
        elif callback.data == "step_ahead":
            callback.data = "first_start"
            await StatesMachine.next()
            await choose_responses(callback, state)
            return

    else:
        pass


async def choose_responses(callback: CallbackQuery, state: FSMContext):
    if type(callback) == CallbackQuery:
        if callback.data == "first_start":
            await state.update_data(responses=None)

            message_id = \
                await callback.message.edit_text(f"Напишите максимальное количество откликов :\n\n💡 Вам *НЕ* будут "
                                                 f"показаны заказы, в которых количество откликов превышает выбранное"
                                                 f"Вами значение\. Для отображения заказов с любым количеством откликов"
                                                 f" нажмите соотвествующую кнопку снизу\.\n\n"
                                                 f"💡 Для добавления маскимального количества откликов отправьте"
                                                 f" сообщение боту, содержащее максимальное число откликов\."
                                                 f"\n*Например:*\n7\n\n"
                                                 f"*Выбранное Вами максимальное значение:*\n"
                                                 f"Отображать заказы с любым количеством откликов ✅",
                                                 parse_mode="MarkDownV2",
                                                 reply_markup=responses_kb)
        elif callback.data == "step_ahead":
            callback.data = "first_start"
            await StatesMachine.next()
            await choose_frequency(callback, state)
            return

    else:
        pass


async def choose_frequency(callback: CallbackQuery, state: FSMContext):
    pass


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
    dp.register_callback_query_handler(choose_keywords,
                                       lambda call: call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_keywords)
    dp.register_message_handler(choose_keywords,
                                state=StatesMachine.waiting_for_keywords)
    dp.register_callback_query_handler(choose_currency,
                                       lambda call: call.data.startswith("chosen") or call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_currency)
    dp.register_callback_query_handler(choose_prices,
                                       lambda call: call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_prices)
    dp.register_message_handler(choose_prices,
                                state=StatesMachine.waiting_for_prices)
    dp.register_callback_query_handler(choose_responses,
                                       lambda call: call.data == "step_ahead",
                                       state=StatesMachine.waiting_for_responses)
    dp.register_message_handler(choose_responses,
                                state=StatesMachine.waiting_for_responses)
