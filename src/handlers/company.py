import logging

from aiogram import F, Router, types

from src.handlers.keyboard import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "🏢 О компании и контакты")
async def cmd_contacts(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запросил контактную информацию")

    contacts_text = (
        "<b>🏢 Контакты компании ИМБИАН</b>\n\n"
        "• <b>Горячая линия:</b> 8 (800) 600-90-77\n"
        "• <b>Email:</b> info@imbian.ru\n\n"
        "<b>📍 Офисы и производство:</b>\n"
        "• <b>Москва (Зеленоград):</b> ул. Конструктора Лукина, д. 14 с.12\n"
        "• <b>Новосибирская обл. (р.п. Кольцово):</b> ул. Садовая, 2/7\n"
        "• <b>Славянск-на-Кубани:</b> ул. Дружбы Народов, 13"
    )

    logger.info(f"Пользователь {message.from_user.id} получил контактную информацию")
    await message.answer(
        text=contacts_text,
        reply_markup=get_main_keyboard(),
    )
