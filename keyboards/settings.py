from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import SITES, CATEGORIES, CURRENCIES, CURRENCIES_SIGNS

# кнопки для навигации
button_next = InlineKeyboardButton(text="Дальше ➡️", callback_data="step_ahead")
button_previous = InlineKeyboardButton(text="⬅️ Назад", callback_data="step_back")
button_done = InlineKeyboardButton(text="Готово ✅", callback_data="setting_done")


def sites_kb(list_of_chosen_sites):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for site in SITES:
        if site in list_of_chosen_sites:
            keyboard.insert(InlineKeyboardButton(text=f"{site} 🟢", callback_data=f"chosen {site}"))
        else:
            keyboard.insert(InlineKeyboardButton(text=f"{site} 🔴", callback_data=f"chosen {site}"))
    keyboard.add(button_next)

    return keyboard


def categories_kb(chosen_category):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for category in CATEGORIES:
        if category == chosen_category:
            keyboard.insert(InlineKeyboardButton(text=f"{category} 🟢", callback_data=f"chosen {category}"))
        else:
            keyboard.insert(InlineKeyboardButton(text=f"{category} 🔴", callback_data=f"chosen {category}"))
    keyboard.add(button_previous, button_next)

    return keyboard


settings_default_kb = InlineKeyboardMarkup(row_width=2).add(button_previous, button_next)


def currency_kb(selected_currency):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for currency in CURRENCIES:
        if currency == selected_currency:
            keyboard.insert(InlineKeyboardButton(text=f"🟩  {currency}  {CURRENCIES_SIGNS.get(currency)}  🟩",
                                                 callback_data=f"chosen {currency}"))
        else:
            keyboard.insert(InlineKeyboardButton(text=f"{currency}  {CURRENCIES_SIGNS.get(currency)}",
                                                 callback_data=f"chosen {currency}"))
    keyboard.add(button_previous, button_next)

    return keyboard


any_prices_button = InlineKeyboardButton(text="Отображать заказы с любой ценой ✅", callback_data="chosen_any")
prices_kb = InlineKeyboardMarkup().add(any_prices_button).add(button_previous, button_next)

any_responses_button = InlineKeyboardButton(text="Отображать заказы с любым кол-вом откликов ✅", callback_data="chosen_any")
responses_kb = InlineKeyboardMarkup().add(any_responses_button).add(button_previous, button_done)

