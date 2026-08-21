# Обработчик команды /status.
# Позволяет изменить статус задачи: НОВАЯ, В РАБОТЕ, ВЫПОЛНЕНА.
# Процесс состоит из двух шагов (FSM):
#   1) пользователь вводит ID задачи;
#   2) пользователь выбирает статус через inline-кнопки.

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database.db import change_status, STATUSES
from keyboards.inline_kb import get_status_keyboard

router = Router()


# Состояния для смены статуса задачи.
class StatusStates(StatesGroup):
    # Состояние "ждём ID задачи"
    waiting_for_task_id = State()


@router.message(Command("status"))
async def cmd_status(message: Message, state: FSMContext):
    """Начинаем процесс смены статуса: просим пользователя ввести ID задачи."""
    await message.answer("Введите ID задачи, статус которой хотите изменить:")
    # Переводим бота в состояние ожидания ID
    await state.set_state(StatusStates.waiting_for_task_id)


@router.message(StatusStates.waiting_for_task_id)
async def process_task_id(message: Message, state: FSMContext):
    """Срабатывает, когда пользователь вводит ID задачи.

    Здесь мы проверяем, что введено число, и показываем inline-кнопки.
    """
    # Проверяем, что пользователь ввёл именно число
    if not message.text.isdigit():
        await message.answer("❌ ID задачи — это число. Попробуйте ещё раз:")
        return

    task_id = int(message.text)

    # Сохраняем ID в состоянии, чтобы использовать его при выборе статуса
    await state.update_data(task_id=task_id)

    # Показываем inline-кнопки для выбора статуса
    await message.answer(
        "Выберите новый статус:",
        reply_markup=get_status_keyboard(),
    )
    # Важно: НЕ сбрасываем состояние (state.clear()),
    # потому что мы ещё ждём нажатия кнопки.


@router.callback_query(F.data.startswith("status:"))
async def process_status_choice(callback: CallbackQuery, state: FSMContext):
    """Срабатывает, когда пользователь нажал inline-кнопку со статусом.

    callback.data выглядит так: "status:НОВАЯ"
    """
    # Достаём статус из callback_data (часть после двоеточия)
    new_status = callback.data.split(":", maxsplit=1)[1]

    # Получаем task_id, который мы сохранили на предыдущем шаге
    data = await state.get_data()
    task_id = data.get("task_id")

    # Меняем статус в базе данных
    found = await change_status(task_id, new_status)

    if found:
        await callback.message.answer(
            f"✅ Статус задачи #{task_id} изменён на: <b>{new_status}</b>"
        )
    else:
        await callback.message.answer(
            f"❌ Задача #{task_id} не найдена."
        )

    # Закрываем inline-кнопки (убираем их из сообщения)
    await callback.message.edit_reply_markup(reply_markup=None)
    # Сбрасываем FSM
    await state.clear()
    # Обязательно отвечаем на callback, иначе Telegram будет "крутить" часики
    await callback.answer()
