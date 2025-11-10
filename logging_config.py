"""Centralized logging configuration for the FASTMCP project."""

from __future__ import annotations

import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.logging import RichHandler

DEFAULT_LOG_LEVEL = "INFO"


def _rich_handler_factory() -> RichHandler:
    """Build a Rich handler that writes exclusively to stderr (safe for STDIO)."""
    return RichHandler(
        console=Console(file=sys.stderr),
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True,
    )


def _build_config(log_level: str = DEFAULT_LOG_LEVEL) -> Dict[str, Any]:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "()": "logging_config._rich_handler_factory",
                "level": log_level,
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "plain",
                "filename": str(log_dir / "fastmcp.log"),
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["console", "file"],
        },
    }


def setup_logging(log_level: str = DEFAULT_LOG_LEVEL) -> None:
    """Configure Python logging with console and rotating file handlers."""
    logging.config.dictConfig(_build_config(log_level))
