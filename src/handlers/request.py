import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logger = logging.getLogger(__name__)
router = Router()


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()


@router.message(F.text == "💬 Оставить отзыв")
async def cmd_feedback(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} собирается оставить отзыв")
    await message.answer(
        "Нам очень важно ваше мнение! Пожалуйста, напишите ваш отзыв в одном сообщении.\n\n"
        "Вы можете честно описать, что вам понравилось, или предложить улучшения для продукции ИМБИАН:"
    )
    await state.set_state(FeedbackForm.waiting_for_feedback)


@router.message(FeedbackForm.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    user_feedback = message.text.strip()
    user_name = f"@{message.from_user.username}" if message.from_user.username else "Скрыт"

    logger.warning(f"Новый отзыв от пользователя {message.from_user.id} ({user_name}): {user_feedback}")

    await message.answer("Спасибо за ваш отзыв! Мы передали его компании ИМБИАН!")
    await state.clear()
