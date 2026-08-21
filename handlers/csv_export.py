# Обработчик команды /list_csv.
# Отправляет список задач файлом в формате CSV.

import csv
import io

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from database.db import get_all_tasks

router = Router()


@router.message(Command("list_csv"))
async def cmd_list_csv(message: Message):
    """Создаёт CSV-файл с задачами и отправляет его пользователю."""
    tasks = await get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Нечего выгружать в CSV.")
        return

    # Создаём CSV-файл в памяти (не сохраняем на диск)
    output = io.StringIO()

    # BOM-метка в начале файла — чтобы Excel правильно отображал кириллицу
    output.write("\ufeff")

    # writer записывает строки в формате CSV.
    # delimiter=";" — разделяем значения точкой с запятой (так удобнее в Excel)
    writer = csv.writer(output, delimiter=";")
    # Заголовок таблицы (включая колонку "Статус")
    writer.writerow(["ID", "Текст задачи", "Пользователь", "Дата создания", "Статус"])
    # Данные — по одной строке на каждую задачу
    for task in tasks:
        writer.writerow(task)

    # Превращаем текст в байты (так нужно для отправки файла в Telegram)
    csv_bytes = output.getvalue().encode("utf-8")

    # BufferedInputFile — обёртка для отправки файла из памяти
    file = BufferedInputFile(csv_bytes, filename="tasks.csv")

    await message.answer_document(file, caption="📄 Вот список задач в формате CSV.")
