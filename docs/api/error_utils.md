# Module `error_utils`

## Functions

### `handle_transport_errors(e, resource_name='resource')`

Handle GraphQL transport errors with consistent logging and friendly feedback.

Args:
    e (Exception): The exception raised by gql transport.
    resource_name (str): Human-readable name of the queried resource (for logs and user messages).

Returns:
    str: A message if the error is a known access denial (403). Re-raises otherwise.

Raises:
    Exception: The original error, unless a known handled case.
