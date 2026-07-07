---
name: sqlite_migration
description: Convert project to SQLite‑only, adjust Alembic config and provide migration commands
source: auto-skill
extracted_at: '2026-05-31T12:40:00.000Z'
---

## Goal
Replace all PostgreSQL references with SQLite, configure Alembic for SQLite, and give the exact commands to generate and apply migrations.

## Steps performed
1. **`src/core/db/env.py`** – forced SQLite:
   ```python
   db_type = os.getenv('DB_TYPE', 'sqlite')
   if db_type == 'sqlite':
       db_url = f"sqlite:///{os.getenv('SQLITE_PATH', 'sqlite.db')}"
   config.set_main_option('sqlalchemy.url', db_url)
   ```
   Removed the `else` branch that built a PostgreSQL URL.
2. **`alembic.ini`** – set the default URL to SQLite:
   ```ini
   sqlalchemy.url = sqlite:///sqlite.db
   ```
3. Updated the default `DB_TYPE` environment variable to `sqlite`.
4. Documented the two Alembic commands:
   - Generate migration: `alembic revision --autogenerate -m "initial SQLite schema"`
   - Apply migration: `alembic upgrade head`
   These create a `sqlite.db` file (or custom path via `SQLITE_PATH`).
5. Verified that no remaining `postgresql` strings existed in `src/core/db/env.py`.
6. Added a placeholder AI token in `src/handlers/fallback.py`:
   ```python
   import os
   AI_TOKEN = os.getenv('AI_TOKEN')
   ```
   Allows the fallback handler to access the token via environment.

## Result
The project now runs solely on SQLite, Alembic is correctly configured, and developers have clear commands to create and apply migrations. The AI fallback handler is ready to use an `AI_TOKEN` without hard‑coding it.
