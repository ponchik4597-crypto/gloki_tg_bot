import logging

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

logger = logging.getLogger(__name__)
router = Router()


# клавиатура
def get_main_keyboard():
    keyboard = [
        [
            KeyboardButton(text="🧬 Каталог продукции"),
            KeyboardButton(text="📨 Создать заявку"),
        ],
        [KeyboardButton(text="🏢 Контакты"), KeyboardButton(text="💬 Задать вопрос")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# для команды /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"<b>Привет, {message.from_user.full_name}!</b> Я персональный ассистент Имбиан.",
        reply_markup=get_main_keyboard(),
    )


# для каталога
@router.message(F.text == "🧬 Каталог продукции")
async def cmd_catalog(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} открыл каталог")
    await message.answer("Здесь будет каталог продукции", reply_markup=get_main_keyboard())


# для создания заявки
@router.message(F.text == "📨 Создать заявку")
async def cmd_create(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} хочет создать заявку")
    await message.answer("Здесь будет возможность создать заявку", reply_markup=get_main_keyboard())


# для контактов
@router.message(F.text == "🏢 Контакты")
async def cmd_contacts(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запросил контактную информацию")

    # Переносим длинный текст через круглые скобки, чтобы ruff не выдавал ошибку E501
    contacts_text = (
        "<b>🏢 Контакты компании ИМБИАН</b>\n\n"
        "• <b>Горячая линия:</b> 8 (800) 600-90-77\n"
        "• <b>Email:</b> info@imbian.ru\n\n"
        "<b>📍 Офисы и производство:</b>\n"
        "• <b>Москва (Зеленоград):</b> ул. Конструктора Лукина, д. 14 с.12\n"
        "• <b>Новосибирская обл. (р.п. Кольцово):</b> ул. Садовая, 2/7\n"
        "• <b>Славянск-на-Кубани:</b> ул. Дружбы Народов, 13"
    )

    await message.answer(
        text=contacts_text,
        reply_markup=get_main_keyboard(),
    )


# задать вопрос
@router.message(F.text == "💬 Задать вопрос")
async def cmd_help(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} перешел к форме вопроса")
    await message.answer("Тут будет возможность задать вопрос", reply_markup=get_main_keyboard())
