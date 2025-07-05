"""
civic_lib_core/log_utils.py

Centralized logging for Civic Interconnect agents and libraries.

Integrates with Loguru for flexible logging and reads config
from the Civic Interconnect project policy.

Typical usage:

    from civic_lib_core import log_utils

    log_utils.init_logger("INFO")
    logger = log_utils.logger

MIT License — maintained by Civic Interconnect
"""

import sys
from pathlib import Path

from loguru import logger

from civic_lib_core import fs_utils, project_policy
from civic_lib_core.date_utils import now_utc_str

__all__ = [
    "init_logger",
    "log_agent_end",
    "log_agent_start",
    "logger",
]

_logger_initialized = False


def init_logger(log_level: str | None = None, log_to_console: bool = True) -> None:
    """
    Initialize Loguru logging once per session.

    Automatically loads logging config from project_policy.yaml
    if available. Defaults to INFO and logs/{date}.log if not found.

    Args:
        log_level (str | None): Optional log level override.
        log_to_console (bool): Whether to also log to stderr.

    Example:
        from civic_lib_core import log_utils
        log_utils.init_logger("INFO")
    """
    global _logger_initialized
    if _logger_initialized:
        logger.debug("Logger already initialized.")
        return

    # Remove any existing loguru handlers to prevent duplicate logs
    logger.remove()

    # Discover the project root
    layout = fs_utils.discover_project_layout()
    project_root = layout[0]
    if not isinstance(project_root, Path):
        raise TypeError(f"project_root is not a Path: {project_root}")

    # Load project policy for logging settings
    policy = project_policy.load_project_policy(project_root)

    log_subdir = policy.get("log_subdir", "logs")
    log_file_template = policy.get("log_file_template", "{time:YYYY-MM-DD}.log")

    logs_dir = project_root / log_subdir
    fs_utils.ensure_dir(logs_dir)

    log_file_path = logs_dir / log_file_template

    # Load log level from policy if not overridden
    if log_level is None:
        log_level = policy.get("log_level", "INFO")

    level = (log_level or "INFO").upper().strip()

    # Add file sink
    logger.add(
        str(log_file_path),
        rotation="1 day",
        retention="7 days",
        level=level,
        backtrace=True,
        diagnose=True,
    )

    # Optionally add console sink
    if log_to_console:
        logger.add(
            sink=sys.stderr,
            level=level,
            backtrace=True,
            diagnose=True,
        )

    logger.info(f"===== Civic Interconnect logger initialized (level: {level}) =====")
    _logger_initialized = True


def log_agent_end(agent_name: str, status: str = "success") -> None:
    """
    Log the end of an agent with its status and UTC timestamp.

    Args:
        agent_name (str): Name of the agent.
        status (str): e.g. "success" or "error".
    """
    timestamp = now_utc_str()
    logger.info(f"===== {agent_name} completed with status: {status} at {timestamp} =====")


def log_agent_start(agent_name: str) -> None:
    """
    Log the start of an agent by name.

    Args:
        agent_name (str): Name of the agent.
    """
    logger.info(f"===== Starting {agent_name} =====")
