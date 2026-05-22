import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=test user=postgres password=secret host=localhost"
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
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
                user_id INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
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
                user_id INTEGER NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
                status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'sent', 'completed', 'cancelled')),
                desired_datetime TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ)
                );
            """)

        self.conn.commit()


if __name__ == "__main__":
    db = Database()
    print("Таблицы успешно созданы")
