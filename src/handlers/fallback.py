from aiogram import Router, types

from src.handlers.start import get_main_keyboard

router = Router()


# копирует все что скажет пользователь
@router.message()
async def echo_handler(message: types.Message):
    await message.answer(
        "Извините, я настроен на работу через меню. Пожалуйста, выберите нужный пункт ниже:",
        reply_markup=get_main_keyboard(),
    )
