import logging

from aiogram import F, Router, types

from src.handlers.keyboard import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "💬 Оставить отзыв")
async def cmd_help(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} собирается оставить отзыв")
    await message.answer("Тут будет возможность оставить отзыв", reply_markup=get_main_keyboard())
