import asyncio
import logging

from dotenv import load_dotenv

from db import async_session
from src.bot import bot, dp
from src.core.logger import setup_logging
from src.handlers import all_routers

load_dotenv()
logger = logging.getLogger(__name__)


async def main():
    @dp.message.outer_middleware()
    async def db_session_middleware(handler, event, data):
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)

    dp.include_routers(*all_routers)

    logger.info("Бот запущен...")
    await bot.delete_webhook(drop_pending_updates=True)  # удалить зависшие логи
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот выключен")
