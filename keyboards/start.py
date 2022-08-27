from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_settings_button = InlineKeyboardButton(text="Начать настройку ⚙️", callback_data="start_settings")
start_finding_button = InlineKeyboardButton(text="Вернуться к поиску 🚀", callback_data="start_finding")

# клавиатура для новых пользователей (нет данных в БД)
start_new_user_kb = InlineKeyboardMarkup().add(start_settings_button)

# клавиатура для старых пользователей (есть данные в БД)
start_old_user_KB = InlineKeyboardMarkup(row_width=1).add(start_finding_button, start_settings_button)
