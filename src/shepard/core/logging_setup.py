# coding: utf-8
"""Configuration du logger 'discord_bot' (console + fichier rotatif)."""
import logging
from logging.handlers import RotatingFileHandler

from shepard.config import LOG_DIR


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_DIR / "discord_bot.log",
        maxBytes=10 * 1024 * 1024,  # 10 Mo
        backupCount=5,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
