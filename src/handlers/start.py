import logging

from aiogram import Router, types
from aiogram.filters import CommandStart

from src.handlers.keyboard import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")
    await message.answer(
        f"<b>Привет, {message.from_user.full_name}!</b> Я персональный ассистент Имбиан.",
        reply_markup=get_main_keyboard(),
    )
