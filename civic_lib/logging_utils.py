"""
civic_lib/logging_utils.py

Centralized logger initialization for Civic Interconnect agents.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import os
from loguru import logger


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
