# Module `civic_lib_core.error_utils`

## Functions

### `handle_transport_errors(e: Exception, resource_name: str = 'resource') -> str`

Handle GraphQL transport errors with consistent logging and user-friendly feedback.

Args:
    e (Exception): The exception raised by gql transport.
    resource_name (str): Human-readable name of the queried resource.

Returns:
    str: Friendly message if known error (e.g., access not granted).

Raises:
    Exception: Original exception for unhandled errors.
