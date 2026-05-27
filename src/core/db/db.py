import logging

import psycopg2

from src.core.config import settings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(settings.database_url.unicode_string())
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        logger.info("Создание таблиц")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL UNIQUE,
                username VARCHAR(255),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ
                );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                message_text TEXT NOT NULL,
                bot_answer TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ,
                feedback VARCHAR(7) CHECK (feedback IN ('like', 'dislike')),
                category VARCHAR(100),
                error TEXT
                );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'sent', 'completed', 'cancelled')),
                desired_datetime TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ
                );
            """)

        self.conn.commit()
        logger.info("Таблицы успешно созданы")

    def close(self):
        self.cursor.close()
        self.conn.close()
        logger.info("Соединение с базой данных закрыто")


if __name__ == "__main__":
    from src.core.logger import setup_logging

    setup_logging()

    db = Database()
