# Обработчик команды /add.
# Здесь используется FSM (Finite State Machine — конечный автомат).
# FSM нужен, чтобы бот "помнил", что мы ждём от пользователя текст задачи.

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.db import add_task

router = Router()


# Описание состояний для добавления задачи.
# StatesGroup — это группа связанных состояний.
class AddTaskStates(StatesGroup):
    # Состояние "ждём текст задачи"
    waiting_for_text = State()


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    """Начинаем процесс добавления задачи: просим пользователя ввести текст."""
    await message.answer("Введите текст задачи:")
    # Переводим бота в состояние ожидания текста
    await state.set_state(AddTaskStates.waiting_for_text)


@router.message(AddTaskStates.waiting_for_text)
async def process_task_text(message: Message, state: FSMContext):
    """Срабатывает, когда пользователь вводит текст задачи.

    Этот обработчик работает только потому, что мы перевели бота
    в состояние waiting_for_text командой /add.
    """
    task_text = message.text  # текст, который прислал пользователь

    # Полное имя пользователя (имя + фамилия, если указаны)
    user_name = message.from_user.full_name

    # Сохраняем задачу в базу данных
    await add_task(task_text, user_name)

    # Отвечаем пользователю
    await message.answer("✅ Задача добавлена!")

    # Выходим из состояния (сбрасываем FSM)
    await state.clear()
