import logging
from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.handlers.keyboard import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


class OrderForm(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()


@router.message(F.text == "📨 Создать заявку")
async def cmd_order(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} хочет создать заявку")

    await message.answer(
        "Введите желаемую дату для связи с менеджером в формате dd.mm.yyyy:",
        reply_markup=get_main_keyboard(),
    )
    await state.set_state(OrderForm.waiting_for_date)


@router.message(OrderForm.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    user_input = message.text.strip()

    try:
        valid_date = datetime.strptime(user_input, "%d.%m.%Y").date()
        if valid_date < datetime.today().date():
            await message.answer(
                "Нельзя выбрать дату из прошлого. Введите актуальную дату"
            )
            return
    except ValueError:
        await message.answer(
            "Неверный формат даты! Пожалуйста, введите дату в формате dd.mm.yyyy:"
        )
        return
    await state.update_data(chosen_date=message.text)
    await message.answer("Отлично! теперь введите удобное время в формате hh:mm:")
    await state.set_state(OrderForm.waiting_for_time)


@router.message(OrderForm.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    user_data = await state.get_data()
    chosen_date_str = user_data.get("chosen_date")

    try:
        valid_date = datetime.strptime(user_input, "%H:%M").time()
        if chosen_date_str == datetime.today().strftime("%d.%m.%Y"):
            if valid_date < datetime.today().time():
                await message.answer(
                    "Нельзя выбрать время из прошлого! Пожалуйста, введите актуальное время"
                )
                return
    except ValueError:
        await message.answer(
            "Неверный формат времени! Пожалуйста, введите дату в формате dd.mm.yyyy:"
        )
        return

    chosen_date = user_data["chosen_date"]
    chosen_time = message.text

    logger.info(
        f"Заявка пользователя {message.from_user.id} создана. Дата: {chosen_date}, {chosen_time}"
    )
    # Добавить отправку на email + хранение в БД
    await message.answer(
        f"Заявка успешно создана на {chosen_date} в {chosen_time}!",
        reply_markup=get_main_keyboard(),
    )

    await state.clear()
