# Module `civic_lib_core.graphql_utils`

## Classes

### `AIOHTTPTransport(self, url: str, headers: Union[Mapping[str, str], Mapping[multidict._multidict.istr, str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, Iterable[Tuple[Union[str, multidict._multidict.istr], str]], NoneType] = None, cookies: Union[Mapping[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]], Iterable[Tuple[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]]], ForwardRef('BaseCookie[str]'), NoneType] = None, auth: Union[aiohttp.helpers.BasicAuth, ForwardRef('AppSyncAuthentication'), NoneType] = None, ssl: Union[ssl.SSLContext, bool, aiohttp.client_reqrep.Fingerprint, str] = 'ssl_warning', timeout: Optional[int] = None, ssl_close_timeout: Union[int, float, NoneType] = 10, json_serialize: Callable = <function dumps at 0x000001250ED0D440>, client_session_args: Optional[Dict[str, Any]] = None) -> None`

:ref:`Async Transport <async_transports>` to execute GraphQL queries
on remote servers with an HTTP connection.

This transport use the aiohttp library with asyncio.

### `Any(self, /, *args, **kwargs)`

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

### `Client(self, schema: Union[str, graphql.type.schema.GraphQLSchema, NoneType] = None, introspection: Optional[graphql.utilities.get_introspection_query.IntrospectionQuery] = None, transport: Union[gql.transport.transport.Transport, gql.transport.async_transport.AsyncTransport, NoneType] = None, fetch_schema_from_transport: bool = False, introspection_args: Optional[Dict] = None, execute_timeout: Union[int, float, NoneType] = 10, serialize_variables: bool = False, parse_results: bool = False, batch_interval: float = 0, batch_max: int = 10)`

The Client class is the main entrypoint to execute GraphQL requests
on a GQL transport.

It can take sync or async transports as argument and can either execute
and subscribe to requests itself with the
:func:`execute <gql.client.Client.execute>` and
:func:`subscribe <gql.client.Client.subscribe>` methods
OR can be used to get a sync or async session depending on the
transport type.

To connect to an :ref:`async transport <async_transports>` and get an
:class:`async session <gql.client.AsyncClientSession>`,
use :code:`async with client as session:`

To connect to a :ref:`sync transport <sync_transports>` and get a
:class:`sync session <gql.client.SyncClientSession>`,
use :code:`with client as session:`

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

### `async_paged_query(url: str, api_key: str, query: Any, data_path: list[str], page_info_path: list[str] | None = None) -> list`

Asynchronously fetch paginated GraphQL results.

Args:
    url (str): GraphQL endpoint URL.
    api_key (str): Authorization token.
    query (gql): gql.Query object.
    data_path (list): Path to the list of data edges.
    page_info_path (list | None): Optional path to pageInfo.

Returns:
    list: Combined list of items from all pages.

### `fetch_paginated(client: Any, query: Any, data_key: str, variables: dict | None = None) -> list[dict]`

Fetch all pages of a paginated GraphQL query.

Args:
    client (gql.Client): Initialized GraphQL client.
    query (gql.Query): Query object.
    data_key (str): Key containing the paginated data.
    variables (dict | None): Optional base query variables.

Returns:
    list[dict]: Combined list of node dicts from all pages.

### `handle_transport_errors(e: Exception, resource_name: str = 'resource') -> str`

Handle GraphQL transport errors with consistent logging and user-friendly feedback.

Args:
    e (Exception): The exception raised by gql transport.
    resource_name (str): Human-readable name of the queried resource.

Returns:
    str: Friendly message if known error (e.g., access not granted).

Raises:
    Exception: Original exception for unhandled errors.

### `paged_query(url: str, api_key: str, query: Any, data_path: list[str]) -> list`

Run a paged GraphQL query synchronously.

Args:
    url (str): GraphQL endpoint.
    api_key (str): Authorization token.
    query (gql): gql.Query object.
    data_path (list): Path to data in response.

Returns:
    list: Combined results from all pages.
