import logging
import os
from openai import AsyncOpenAI
from src.core.config import settings

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    base_url="https://openrouter.ai",
    api_key=(settings.ai_token.get_secret_value() if settings.ai_token else None) or os.getenv("OPENAI_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://github.com",
        "X-Title": "Gloki Imbian Bot"
    }
)

SYSTEM_PROMPT = """
Ты — официальный ИИ-консультант компании ИМБИАН.
Твоя задача — отвечать строго по скрипту и базе знаний компании.
Правила:
1. Будь вежлив, отвечай кратко и строго по делу.
2. Не придумывай факты. Если ты чего-то не знаешь, вежливо отправь пользователя к меню.
3. Отвечай только на текстовые вопросы, связанные с ИМБИАН.
"""


async def get_ai_consultation(user_message: str) -> str:
    if not settings.ai_token:
        logger.error("Переменная конфигурации AI_TOKEN не задана!")
        return "Извините, ИИ-консультант сейчас на техобслуживании."

    try:
        response = await client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
        )

        ai_text = ""

        if hasattr(response, 'choices') and response.choices:
            ai_text = response.choices[0].message.content

        elif isinstance(response, dict) and "choices" in response:
            ai_text = response["choices"][0]["message"]["content"]

        elif isinstance(response, str):
            ai_text = response

        else:
            ai_text = str(response)

        if not ai_text:
            return "Не удалось получить текстовый ответ от ИИ."

        if len(ai_text) > 4000:
            ai_text = ai_text[:4000] + "\n\n...[Ответ усечен из-за длины]"

        return ai_text

    except Exception as e:
        logger.error(f"Ошибка OpenRouter API: {e}", exc_info=True)
        return "Произошла ошибка при обработке запроса. Пожалуйста, воспользуйтесь меню."
