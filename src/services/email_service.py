import asyncio
import logging

logger = logging.getLogger(__name__)


class MailService:
    """генерирует ответ, используя LLM или SearchEngine
    атрибуты:
    llm - экземпляр LLMService
    search_engine_template - системный промт
    методы:
    generate_response(user_id, chat_id, user_message, context_history) -> str
    """

    async def send_email(self, to: str, subject: str, body: str):
        logger.info(f"Письмо для {to}: {subject} – {body}")
        await asyncio.sleep(0.5)  # имитация
