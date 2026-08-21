# Обработчик команды /list.
# Выводит список всех задач из базы данных.

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.db import get_all_tasks

router = Router()


@router.message(Command("list"))
async def cmd_list(message: Message):
    """Показывает все задачи из базы данных."""
    # Получаем список задач (каждая задача — кортеж: id, text, user, created_at, status)
    tasks = await get_all_tasks()

    # Если задач нет — сообщаем об этом
    if not tasks:
        await message.answer("Список задач пуст.")
        return

    # Эмодзи для наглядности статуса
    status_icons = {"НОВАЯ": "🆕", "В РАБОТЕ": "🔧", "ВЫПОЛНЕНА": "✅"}

    # Собираем текст со всеми задачами
    text = "📋 Список задач:\n\n"
    for task_id, task_text, user, created_at, status in tasks:
        icon = status_icons.get(status, "❓")
        text += (
            f"{task_id}. {task_text}\n"
            f"   {icon} Статус: {status} | 👤 {user} | 🕐 {created_at}\n\n"
        )

    await message.answer(text)
