import httpx
from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bs4 import BeautifulSoup

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
    await message.answer(
        f"Здесь будет каталог продукции", reply_markup=get_main_keyboard()
    )


# для создания заявки
@router.message(F.text == "📨 Создать заявку")
async def cmd_create(message: types.Message):
    await message.answer(
        f"Здесь будет возможность создать заявку", reply_markup=get_main_keyboard()
    )


# для контактов
@router.message(F.text == "🏢 Контакты")
async def cmd_contacts(message: types.Message):
    url = "https://imbian.ru"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # телефон
            phone_tag = soup.find("a", href=lambda href: href and "tel:" in href)
            if phone_tag:
                raw_phone = phone_tag.get("href").replace("tel:", "").strip()
                if len(raw_phone) == 11 and raw_phone.startswith(("8", "7")):
                    phone = f"{raw_phone[0]} ({raw_phone[1:4]}) {raw_phone[4:7]}-{raw_phone[7:9]}-{raw_phone[9:11]}"
                else:
                    phone = (
                        phone_tag.text.strip() if phone_tag.text.strip() else raw_phone
                    )
            else:
                phone = "8 (800) 600-90-77"
            # email
            email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
            if email_tag:
                email = email_tag.text.strip()
                if not email:
                    email = email_tag.get("href").replace("mailto:", "").strip()
            else:
                email = "info@imbian.ru"

            contacts_text = (
                f"<b>🏢 Контакты компании ИМБИАН</b>\n\n"
                f"• <b>Горячая линия:</b> {phone}\n"
                f"• <b>Email:</b> {email}\n"
                "<b>📍 Офисы и производство:</b>\n"
                "• <b>Москва (Зеленоград):</b> ул. Конструктора Лукина, д. 14 с.12\n"
                "• <b>Новосибирская обл. (Кольцово):</b> ул. Садовая, 2/7\n"
                "• <b>Славянск-на-Кубани:</b> ул. Дружбы Народов, 13\n\n"
                "<i>Данные синхронизированы с сайтом imbian.ru</i>"
            )
        else:
            contacts_text = (
                "⚠️ Не удалось подключиться к сайту. Актуальный Email: info@imbian.ru"
            )
    except Exception:
        contacts_text = "<b>🏢 Контакты компании ИМБИАН:</b>\n\n• Тел: 8 (800) 600-90-77\n• Email: info@imbian.ru"

    await message.answer(contacts_text, reply_markup=get_main_keyboard())


# задать вопрос
@router.message(F.text == "💬 Задать вопрос")
async def cmd_help(message: types.Message):
    await message.answer(
        "Тут будет возможность задать вопрос", reply_markup=get_main_keyboard()
    )
