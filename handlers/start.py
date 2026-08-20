# Обработчик команды /start.
# Это первая команда, с которой начинает пользователь.

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.reply_kb import get_main_keyboard

# Роутер — это "контейнер" для обработчиков.
# Позже мы подключим его к главному диспетчеру в main.py.
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Срабатывает, когда пользователь отправляет команду /start."""
    await message.answer(
        "Привет! 👋 Я бот для командной работы с задачами.\n\n"
        "Доступные команды:\n"
        "/add — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — получить список задач файлом в формате CSV",
        # Прикрепляем клавиатуру с кнопками
        reply_markup=get_main_keyboard(),
    )
