FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY requirements.txt ./

RUN uv pip install --system --no-cache -r requirements.txt

COPY src/ ./src/

ENV PYTHONPATH=/app/src

CMD ["python3", "main.py"]