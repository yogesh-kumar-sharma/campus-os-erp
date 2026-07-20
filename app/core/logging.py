"""Logging configuration shared by the API and background processes."""

import logging.config

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure concise, structured-enough console logging for the application."""
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {"handlers": ["console"], "level": settings.log_level.upper()},
        }
    )

