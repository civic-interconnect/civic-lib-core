# Module `error_utils`

## Classes

### `TransportProtocolError(self, /, *args, **kwargs)`

Transport protocol error.

The answer received from the server does not correspond to the transport protocol.

### `TransportQueryError(self, msg: str, query_id: Optional[int] = None, errors: Optional[List[Any]] = None, data: Optional[Any] = None, extensions: Optional[Any] = None)`

The server returned an error for a specific query.

This exception should not close the transport connection.

### `TransportServerError(self, message: str, code: Optional[int] = None)`

The server returned a global error.

This exception will close the transport connection.

## Functions

### `handle_transport_errors(e: Exception, resource_name: str = 'resource') -> str`

Handle GraphQL transport errors with consistent logging and friendly feedback.

Args:
    e (Exception): The exception raised by gql transport.
    resource_name (str): Human-readable name of the queried resource (for logs and user messages).

Returns:
    str: A message if the error is a known access denial (403). Re-raises otherwise.

Raises:
    Exception: The original error, unless a known handled case.
