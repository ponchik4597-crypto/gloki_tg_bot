import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models import Message, User

logger = logging.getLogger(__name__)
router = Router()


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()


@router.message(F.text == "💬 Оставить отзыв")
async def cmd_feedback(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} собирается оставить отзыв")
    await message.answer(
        "Нам очень важно ваше мнение! Пожалуйста, напишите ваш отзыв в одном сообщении.\n\n"
    )
    await state.set_state(FeedbackForm.waiting_for_feedback)


@router.message(FeedbackForm.waiting_for_feedback)
async def process_feedback(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    user_telegram_id = message.from_user.id
    user_feedback = message.text.strip()
    user_name = (
        f"@{message.from_user.username}" if message.from_user.username else "Скрыт"
    )

    logger.info(
        f"Новый отзыв от пользователя {message.from_user.id} ({user_name}): {user_feedback}"
    )

    # для сохранения логов в базу данных
    try:
        statement = select(User).where(User.telegram_id == user_telegram_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=user_telegram_id, username=message.from_user.username
            )
            session.add(user)
            await session.flush()

        new_message = Message(
            user_id=user.id, message_text=user_feedback, category="feedback"
        )
        session.add(new_message)
        await session.commit()

        logger.info(f"Отзыв пользователя {user.id} успешно сохранен в базу данных")
    except Exception as e:
        await session.rollback()
        logger.error(f"Не удалось сохранить отзыв пользователя {user_telegram_id}: {e}")

    await message.answer("Спасибо за ваш отзыв! Мы передали его компании ИМБИАН!")
    await state.clear()
