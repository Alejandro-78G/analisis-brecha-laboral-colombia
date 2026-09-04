import logging
import sys
from rich.logging import RichHandler
from src.core.config import settings


def setup_logger(name: str = "pipeline") -> logging.Logger:
    """
    Configura un logger profesional con RichHandler para consola.
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL.upper())

    if not logger.handlers:
        console_handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=False,
            markup=True
        )
        console_handler.setLevel(settings.LOG_LEVEL.upper())

        formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
