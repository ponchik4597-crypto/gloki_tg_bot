import logging

from src.core.config import settings


def setup_logging():
    log_level = logging.DEBUG if settings.debag else logging.info

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logging.getLogger("aiogram").setLevel(logging.warning)
