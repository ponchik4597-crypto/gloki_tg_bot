import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Инициализируем ИИ
ai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IMBIAN_KNOWLEDGE_BASE = """
ИМБИАН» — российская научно-производственная компания,основанная в 2019 году и специализирующаяся на разработке и серийном выпуске медицинских тест-систем (ИХА, ИФА, ПЦР) и БАДов. Производственные мощности расположены в Кольцово и Славянске-на-Кубани,обеспечивая выпуск продукции под собственными брендами и контрактное производство,Более подробную информацию можно найти на сайте imbian.ru.
"""


async def get_ai_consultation(user_question: str) -> str:
    try:
        response = await ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — официальный ИИ-консультант компании ИМБИАН (IMBIAN).\n"
                        "Твоя задача — отвечать на вопросы клиентов строго на основе предоставленной Базы Знаний.\n\n"
                        f"--- НАЧАЛО БАЗЫ ЗНАНИЙ ---\n{IMBIAN_KNOWLEDGE_BASE}\n--- КОНЕЦ БАЗЫ ЗНАНИЙ ---\n\n"
                        "КРИТИЧЕСКИЕ ПРАВИЛА:\n"
                        "1. Отвечай вежливо, профессионально и лаконично.\n"
                        "2. Если вопрос НЕ связан с компанией ИМБИАН, её продукцией, контактами или контрактами, "
                        "ты должен строго, но вежливо отказать в ответе.\n"
                        "3. Не придумывай факты, которых нет в Базе Знаний."
                    ),
                },
                {"role": "user", "content": user_question},
            ],
            temperature=0.3,
        )
        return response.choices.message.content
    except Exception as e:
        logger.error(f"Ошибка при обращении к OpenAI API: {e}")
        return "Извините, сейчас я испытываю временные трудности с ответом. Пожалуйста, попробуйте позже."
