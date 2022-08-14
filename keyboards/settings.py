from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import SITES, CATEGORIES

button_next = InlineKeyboardButton(text="Дальше ➡️", callback_data="step_ahead")
button_previous = InlineKeyboardButton(text="⬅️ Назад", callback_data="step_back")


def sites_kb(list_of_chosen_sites):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for site in SITES:
        if site in list_of_chosen_sites:
            keyboard.insert(InlineKeyboardButton(text=f"{site} 🟢", callback_data=f"chosen {site}"))
        else:
            keyboard.insert(InlineKeyboardButton(text=f"{site} 🔴", callback_data=f"chosen {site}"))
    keyboard.add(button_next)

    return keyboard


def categories_kb(list_of_chosen_categories):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for category in CATEGORIES:
        if category in list_of_chosen_categories:
            keyboard.insert(InlineKeyboardButton(text=f"{category} 🟢", callback_data=f"chosen {category}"))
        else:
            keyboard.insert(InlineKeyboardButton(text=f"{category} 🔴", callback_data=f"chosen {category}"))
    keyboard.add(button_previous, button_next)

    return keyboard


def mode_kb(selected_mode):
    keyboard = InlineKeyboardMarkup(row_width=1)

    if selected_mode == "basic":
        keyboard.insert(InlineKeyboardButton(text="Поиск по ключевым словам", callback_data="chosen keywords"))
        keyboard.insert(InlineKeyboardButton(text="🟩              Обычный поиск              🟩", callback_data="chosen basic"))
    else:
        keyboard.insert(InlineKeyboardButton(text="🟩 Поиск по ключевым словам  🟩", callback_data="chosen keywords"))
        keyboard.insert(InlineKeyboardButton(text="Обычный поиск", callback_data="chosen basic"))
    keyboard.row(button_previous, button_next)

    return keyboard
