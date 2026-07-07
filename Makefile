.PHONY: format lint lint-fix check

#форматирование кода
format:
	uv run ruff format .
	uv run ruff check . --fix

#проверка кода линтером
lint:
	uv run ruff check .

#проверка линтером с автоматическим исправлением мелких ошибок
lint-fix:
	uv run ruff check . --fix

#проверка перед коммитом
check:
	uv run ruff format --check .
	uv run ruff check .
