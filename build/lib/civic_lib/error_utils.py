"""
civic_lib/error_utils.py

Centralized error handling for GraphQL and network operations.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from gql.transport.exceptions import (
    TransportProtocolError,
    TransportQueryError,
    TransportServerError,
)

from civic_lib import log_utils


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
            log_utils.logger.warning(f"{resource_name} access not yet enabled (403 Forbidden).")
            return f"{resource_name} access not yet granted"
        log_utils.logger.error(f"Server error: {e}")

    elif isinstance(e, TransportQueryError):
        log_utils.logger.error(f"GraphQL query error: {e}")

    elif isinstance(e, TransportProtocolError):
        log_utils.logger.error(f"Transport protocol error: {e}")

    else:
        log_utils.logger.error(f"Unexpected error: {e}")

    raise e
