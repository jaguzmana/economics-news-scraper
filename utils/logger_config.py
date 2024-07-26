import logging

def logger_config():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")

    formatter = logging.Formatter(
        "{asctime} | {levelname} | {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = logger_config()
