"""
civic_lib/logging_utils.py

Centralized logger functions for Civic Interconnect agents.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import os
from datetime import UTC, datetime
from pathlib import Path

from loguru import logger

LIB_DIR = Path(__file__).parent
ROOT_DIR = LIB_DIR.parent
VERSION_FILE = ROOT_DIR / "VERSION"


def init_logger():
    """
    Initialize loguru logging.

    - Creates the logs/ directory if it doesn't exist.
    - Sets up daily log rotation.
    - Retains logs for 7 days.
    - Logs agent start message.
    """
    os.makedirs("logs", exist_ok=True)
    logger.add("logs/{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days", level="INFO")
    logger.info("===== Agent started =====")


def log_agent_start(agent_name):
    """
    Log the start of an agent with its name.
    Args:
        agent_name (str): The name of the agent starting.
    """
    logger.info(f"===== Starting {agent_name} =====")


def log_agent_end(agent_name, status="success"):
    """
    Log the end of an agent with its name and status.
    Args:
        agent_name (str): The name of the agent ending.
        status (str): The status of the agent at the end (default is "success").
    """
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    logger.info(f"===== {agent_name} completed with status: {status} at {timestamp} =====")


def lib_version():
    """
    Return the version of the Civic Interconnect library.

    Reads the VERSION file in the parent directory.
    Returns:
        str: The version string.
    """
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error(
            "VERSION file not found in root folder of library repository. Please create a file named VERSION in the root folder of the library repository with the version number, e.g. v0.1.0."
        )
        return "unknown"
