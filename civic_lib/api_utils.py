"""
civic_lib/api_utils.py

Core utilities for API authentication, configuration loading, and logging.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import os
import sys
from loguru import logger


def load_openstates_api_key():
    """
    Load the OpenStates API key from environment variables.

    Reads the OPENSTATES_API_KEY environment variable.
    If missing, logs an error and exits the program.

    Returns:
        str: The API key if found.

    Exits:
        If the API key is not found, exits with an error message.
    """
    key = os.getenv("OPENSTATES_API_KEY")

    if not key:
        logger.error(
            "OpenStates API key missing. is missing.\n"
            "Fix: Add OPENSTATES_API_KEY to your .env file or system environment variables."
        )
        sys.exit("Error: OPENSTATES_API_KEY is required.")
        
    logger.debug("OpenStates API key loaded successfully.")
    return key
