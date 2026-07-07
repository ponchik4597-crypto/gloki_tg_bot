import logging

from aiogram import F, Router, types

from src.constants.info import PRODUCTS_BY_CATEGORY
from src.handlers.keyboard import get_categories_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "🧬 Каталог продукции")
async def cmd_catalog(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} открыл каталог")
    await message.answer(
        "<b>🧬 Каталог продукции ИМБИАН</b>\n\nПожалуйста, выберите интересующую вас категорию:",
        reply_markup=get_categories_keyboard(),
    )


@router.callback_query(F.data.startswith("cat_"))
async def cat(callback: types.CallbackQuery):
    category_key = callback.data

    category_title = callback.message.reply_markup.inline_keyboard[0][0].text
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == category_key:
                category_title = button.text
                break

    logger.info(
        f"Пользователь {callback.from_user.id} запросил список продукции из категории {category_title}"
    )

    products = PRODUCTS_BY_CATEGORY.get(category_key, [])
    text = f"<b>Список продукции ИМБИАН из категории {category_title}</b>\n\n"

    for product in products:
        text += f"<b>{product['name']}</b>\n"
        text += f"<i>Описание:</i> {product['desc']}\n"

    await callback.message.answer(text, parse_mode="html")

    await callback.answer()
