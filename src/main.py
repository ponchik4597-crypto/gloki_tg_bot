import asyncio
from src.bot import bot, dp
from src.core.logger import setup_logging
from src.handlers import all_routers


async def main():
    setup_logging()
    dp.include_routers(*all_routers)

    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
