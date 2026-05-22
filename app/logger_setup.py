"""
Logging configuration.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
def setup_logging():
    logger = logging.getLogger("churn-api")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5_000_000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging initialized")
    return logger