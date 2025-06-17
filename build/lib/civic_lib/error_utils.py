"""
civic_lib/error_utils.py

Centralized error handling for GraphQL and network operations.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from gql.transport.exceptions import (
    TransportServerError,
    TransportQueryError,
    TransportProtocolError
)
from loguru import logger


def handle_transport_errors(e, resource_name="resource"):
    """
    Handle GraphQL transport errors with consistent logging and messaging.

    Args:
        e (Exception): The exception raised by gql transport.
        resource_name (str): The name of the resource being queried (used for cleaner logs).

    Returns:
        str: If known 403 error occurs, returns a friendly message.
    """
    if isinstance(e, TransportServerError):
        if "403" in str(e):
            logger.warning(f"{resource_name} access not yet enabled (403 Forbidden).")
            return f"{resource_name} access not yet granted"
        logger.error(f"Server error: {e}")

    elif isinstance(e, TransportQueryError):
        logger.error(f"GraphQL query error: {e}")

    elif isinstance(e, TransportProtocolError):
        logger.error(f"Transport protocol error: {e}")

    else:
        logger.error(f"Unexpected error: {e}")

    raise e
