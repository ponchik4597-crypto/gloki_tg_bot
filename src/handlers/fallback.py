import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.handlers.keyboard import get_main_keyboard
from src.services.ai_service import get_ai_consultation

logger = logging.getLogger(__name__)
router = Router()


# обработка всего, что не словили другие хэндлеры
@router.message(F.text)
async def fallback_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        return

    logger.info(f"У пользователя {message.from_user.id} сработал ИИ-fallback")

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    ai_answer = await get_ai_consultation(message.text)
    safe_answer = ai_answer[:4000]
    await message.answer(safe_answer, parse_mode="")


@router.message()
async def fallback_media_handler(message: types.Message):
    logger.info(f"У пользователя {message.from_user.id} сработал fallback на медиафайл")
    await message.answer(
        "Извините, я понимаю только текстовые вопросы о компании ИМБИАН или работу через меню:",
        reply_markup=get_main_keyboard(),
    )
