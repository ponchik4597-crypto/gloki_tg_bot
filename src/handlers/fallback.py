import logging

from aiogram import Router, types

from src.handlers.start import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


# обработка всего, что не словили другие хэндлеры
@router.message()
async def fallback_handler(message: types.Message):
    logger.info(f"У пользователя {message.from_user.id} сработал fallback")
    await message.answer(
        "Извините, я настроен на работу через меню. Пожалуйста, выберите нужный пункт ниже:",
        reply_markup=get_main_keyboard(),
    )
