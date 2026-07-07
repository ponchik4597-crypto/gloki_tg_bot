from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def get_main_keyboard():
    keyboard = [
        [
            KeyboardButton(text="🧬 Каталог продукции"),
            KeyboardButton(text="🤝 Контрактное производство"),
        ],
        [
            KeyboardButton(text="📨 Создать заявку"),
            KeyboardButton(text="💬 Оставить отзыв"),
        ],
        [
            KeyboardButton(text="🏢 О компании и контакты"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_categories_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="ИХЛА", callback_data="cat_ihla"),
            InlineKeyboardButton(text="ПЦР", callback_data="cat_pcr"),
        ],
        [
            InlineKeyboardButton(text="БАД", callback_data="cat_bad"),
            InlineKeyboardButton(text="Коллаген", callback_data="cat_collagen"),
        ],
        [
            InlineKeyboardButton(
                text="Диагностические системы", callback_data="cat_diag"
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)


def get_category_keyboard(product_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📨 Оставить заявку на этот товар",
                callback_data=f"order_prod_{product_id}",
            ),
            InlineKeyboardButton(
                text="⬅️ Назад к списку товаров", callback_data="back_to_list"
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
