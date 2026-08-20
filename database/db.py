# Модуль для работы с базой данных SQLite.
# Используем aiosqlite — асинхронную версию стандартной библиотеки sqlite3.
# Это нужно, чтобы бот не "зависал" во время обращения к базе.

import aiosqlite
from datetime import datetime

from config import DB_PATH


async def init_db():
    """Создаёт таблицу tasks, если её ещё нет.

    Эту функцию нужно вызывать один раз при запуске бота.
    """
    # Подключаемся к базе данных (файл создастся автоматически)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- уникальный номер задачи
                text TEXT NOT NULL,                     -- текст задачи
                user TEXT NOT NULL,                     -- имя пользователя, добавившего задачу
                created_at TEXT NOT NULL                -- дата и время добавления
            )
        """)
        await db.commit()  # сохраняем изменения


async def add_task(text: str, user: str):
    """Добавляет новую задачу в базу данных.

    :param text: текст задачи
    :param user: имя пользователя, который добавил задачу
    """
    # Получаем текущую дату и время в виде строки
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async with aiosqlite.connect(DB_PATH) as db:
        # Знак ? — это плейсхолдер. Он защищает от SQL-инъекций.
        await db.execute(
            "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
            (text, user, created_at),
        )
        await db.commit()


async def get_all_tasks():
    """Возвращает список всех задач из базы.

    Каждый элемент списка — это кортеж (id, text, user, created_at).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, text, user, created_at FROM tasks ORDER BY id"
        ) as cursor:
            return await cursor.fetchall()
