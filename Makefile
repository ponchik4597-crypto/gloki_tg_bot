.PHONY: format lint check

#форматирование кода
format:
	uv run ruff format .

#проверка кода линтером
lint:
	uv run ruff check .

#проверка линтером с автоматическим исправлением мелких ошибок
lint-fix:
	uv run ruff check . --fix

#проверка перед коммитом
check: lint format
