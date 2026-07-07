import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# переменные из .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Переменная DATABASE_URL не найдена в файле .env")

# асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)

# сессии для бота
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
