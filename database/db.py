# Модуль для работы с базой данных SQLite.
# Используем aiosqlite — асинхронную версию стандартной библиотеки sqlite3.
# Это нужно, чтобы бот не "зависал" во время обращения к базе.

import aiosqlite
from datetime import datetime

from config import DB_PATH


# Возможные статусы задачи.
# Используем как значения по умолчанию и при проверке ввода пользователя.
STATUSES = ("НОВАЯ", "В РАБОТЕ", "ВЫПОЛНЕНА")


async def init_db():
    """Создаёт таблицу tasks, если её ещё нет.

    Также добавляет колонку status, если база была создана раньше
    (миграция: старые задачи получат статус "НОВАЯ").

    Эту функцию нужно вызывать один раз при запуске бота.
    """
    # Подключаемся к базе данных (файл создастся автоматически)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- уникальный номер задачи
                text TEXT NOT NULL,                     -- текст задачи
                user TEXT NOT NULL,                     -- имя пользователя, добавившего задачу
                created_at TEXT NOT NULL,               -- дата и время добавления
                status TEXT NOT NULL DEFAULT 'НОВАЯ'    -- статус задачи
            )
        """)

        # МИГРАЦИЯ: если таблица существовала без колонки status — добавляем её.
        # Проверяем наличие колонки через PRAGMA table_info.
        async with db.execute("PRAGMA table_info(tasks)") as cursor:
            columns = await cursor.fetchall()
        # columns — список кортежей; индекс 1 — имя колонки.
        column_names = [col[1] for col in columns]
        if "status" not in column_names:
            # ALTER TABLE добавляет новую колонку во все существующие строки.
            await db.execute(
                "ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'НОВАЯ'"
            )

        await db.commit()  # сохраняем изменения


async def add_task(text: str, user: str):
    """Добавляет новую задачу в базу данных.

    Новая задача всегда получает статус "НОВАЯ".

    :param text: текст задачи
    :param user: имя пользователя, который добавил задачу
    """
    # Получаем текущую дату и время в виде строки
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async with aiosqlite.connect(DB_PATH) as db:
        # Знак ? — это плейсхолдер. Он защищает от SQL-инъекций.
        await db.execute(
            "INSERT INTO tasks (text, user, created_at, status) VALUES (?, ?, ?, ?)",
            (text, user, created_at, "НОВАЯ"),
        )
        await db.commit()


async def get_all_tasks():
    """Возвращает список всех задач из базы.

    Каждый элемент списка — это кортеж (id, text, user, created_at, status).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, text, user, created_at, status FROM tasks ORDER BY id"
        ) as cursor:
            return await cursor.fetchall()


async def change_status(task_id: int, status: str):
    """Меняет статус задачи по её ID.

    :param task_id: номер задачи
    :param status: новый статус ("НОВАЯ", "В РАБОТЕ", "ВЫПОЛНЕНА")
    :return: True — если задача найдена и статус изменён, False — если задачи нет
    """
    async with aiosqlite.connect(DB_PATH) as db:
        # cursor.rowcount покажет, сколько строк изменилось (0 = задача не найдена)
        cursor = await db.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id),
        )
        await db.commit()
        return cursor.rowcount > 0
