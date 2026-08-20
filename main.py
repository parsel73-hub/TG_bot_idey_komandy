# Точка входа в программу.
# Этот файл запускает бота.

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import BOT_TOKEN, PROXY_URL
from database.db import init_db
from handlers import start, add, list_tasks, csv_export


async def main():
    """Главная асинхронная функция — здесь запускается бот."""
    # 1. Инициализируем базу данных (создаём таблицу tasks, если её нет)
    await init_db()

    # 2. Создаём сессию. Если задан прокси — подключаемся к Telegram через него
    #    (это помогает, когда api.telegram.org заблокирован провайдером).
    session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None

    # 3. Создаём объект бота.
    #    ParseMode.HTML разрешает использовать HTML-теги в текстах сообщений.
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # 4. Создаём диспетчер — он распределяет входящие сообщения по обработчикам.
    dp = Dispatcher()

    # 5. Подключаем роутеры (обработчики команд) к диспетчеру.
    #    Порядок важен: обработчики проверяются по очереди.
    dp.include_router(start.router)
    dp.include_router(add.router)
    dp.include_router(list_tasks.router)
    dp.include_router(csv_export.router)

    # 6. Запускаем бота.
    #    delete_webhook — сбрасывает накопившиеся сообщения перед запуском.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Этот блок срабатывает, когда файл запускают напрямую:  python main.py
if __name__ == "__main__":
    asyncio.run(main())
