# Модуль с кнопками (клавиатурой) для бота.
# Reply-клавиатура — это кнопки, которые появляются внизу экрана вместо обычной панели ввода.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт главную клавиатуру с кнопками-командами."""
    # Описание кнопок. Каждая внутренняя скобка — это одна строка кнопок.
    buttons = [
        [KeyboardButton(text="/add"), KeyboardButton(text="/list")],
        [KeyboardButton(text="/list_csv")],
    ]
    # resize_keyboard=True — кнопки будут стандартного размера (не растянутыми)
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
