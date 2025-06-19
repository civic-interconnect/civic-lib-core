"""
civic_lib/error_utils.py

Centralized error handling for GraphQL and network operations.
Used by agents to log and surface helpful messages when API errors occur.

MIT License — maintained by Civic Interconnect
"""

from gql.transport.exceptions import (
    TransportProtocolError,
    TransportQueryError,
    TransportServerError,
)

from civic_lib import log_utils

__all__ = ["handle_transport_errors"]

logger = log_utils.logger


def handle_transport_errors(e: Exception, resource_name: str = "resource") -> str:
    """
    Handle GraphQL transport errors with consistent logging and friendly feedback.

    Args:
        e (Exception): The exception raised by gql transport.
        resource_name (str): Human-readable name of the queried resource (for logs and user messages).

    Returns:
        str: A message if the error is a known access denial (403). Re-raises otherwise.

    Raises:
        Exception: The original error, unless a known handled case.
    """
    if isinstance(e, TransportServerError):
        if "403" in str(e):
            logger.warning(f"{resource_name} access not yet enabled (403 Forbidden).")
            return f"{resource_name} access not yet granted"
        logger.error(f"Server error while accessing {resource_name}: {e}")

    elif isinstance(e, TransportQueryError):
        logger.error(f"GraphQL query error while accessing {resource_name}: {e}")

    elif isinstance(e, TransportProtocolError):
        logger.error(f"Transport protocol error during {resource_name} query: {e}")

    else:
        logger.error(f"Unexpected error during {resource_name} query: {e}")

    raise e
