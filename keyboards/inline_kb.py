# Модуль с inline-клавиатурами (кнопки под сообщением, а не внизу экрана).
# Inline-кнопки удобны для выбора варианта — например, статуса задачи.

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# callback_data — это короткая строка, которую бот получит при нажатии кнопки.
# Мы кодируем в ней выбранный статус: "status:НОВАЯ", "status:В РАБОТЕ" и т.д.
_STATUSES = ["НОВАЯ", "В РАБОТЕ", "ВЫПОЛНЕНА"]


def get_status_keyboard() -> InlineKeyboardMarkup:
    """Создаёт inline-клавиатуру для выбора статуса задачи."""
    buttons = []
    for status in _STATUSES:
        # Каждая кнопка — в своей строке (сверху вниз).
        buttons.append(
            [InlineKeyboardButton(text=status, callback_data=f"status:{status}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
