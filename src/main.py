import asyncio
import logging

from src.bot import bot, dp
from src.core.logger import setup_logging
from src.handlers import all_routers

logger = logging.getLogger(__name__)


async def main():
    dp.include_routers(*all_routers)

    logger.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот выключен")
