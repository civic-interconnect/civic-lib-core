"""
log_utils.py

Centralized logging for Civic Interconnect agents and libraries.

In config.yaml:
    log_level: info  # or debug, warning, error, critical

In code:
    from civic_lib_core import log_utils
    log_utils.init_logger()
    logger = log_utils.logger


MIT License — maintained by Civic Interconnect
"""

import sys

from loguru import logger

from civic_lib_core.date_utils import now_utc_str
from civic_lib_core.path_utils import ensure_dir

__all__ = [
    "init_logger",
    "log_agent_end",
    "log_agent_start",
    "logger",
]

_logger_initialized = False

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_PATH = "logs/{time:YYYY-MM-DD}.log"


def init_logger(log_level: str | None = None, log_to_console: bool = True) -> None:
    """
    Initialize loguru logging once per session.

    If no log level is provided, attempts to load it from config.yaml as 'log_level'.
    Defaults to INFO if not found or config is missing.

    Args:
        log_level (str | None): Optional log level override (default: config.yaml or "INFO").
        log_to_console (bool): If True, logs to stderr in addition to file.
    """
    global _logger_initialized
    if _logger_initialized:
        logger.debug("Logger already initialized.")
        return

    # Remove the default loguru handler to prevent duplicates
    logger.remove()

    if log_level is None:
        try:
            from civic_lib_core.config_utils import load_yaml_config

            cfg = load_yaml_config()
            log_level = cfg.get("log_level", DEFAULT_LOG_LEVEL)
        except Exception as e:
            logger.warning(f"Could not load config.yaml for log level: {e}")
            log_level = DEFAULT_LOG_LEVEL

    ensure_dir("logs")
    level = (log_level or DEFAULT_LOG_LEVEL).upper().strip()

    logger.add(
        DEFAULT_LOG_PATH,
        rotation="1 day",
        retention="7 days",
        level=level,
        backtrace=True,
        diagnose=True,
    )

    if log_to_console:
        logger.add(
            sink=sys.stderr,
            level=level,
            backtrace=True,
            diagnose=True,
        )

    logger.info(f"===== Agent logger initialized (level: {level}) =====")
    _logger_initialized = True


def log_agent_end(agent_name: str, status: str = "success") -> None:
    """
    Log the end of an agent with its status and UTC timestamp.
    """
    timestamp = now_utc_str()
    logger.info(f"===== {agent_name} completed with status: {status} at {timestamp} =====")


def log_agent_start(agent_name: str) -> None:
    """
    Log the start of an agent by name.
    """
    logger.info(f"===== Starting {agent_name} =====")
