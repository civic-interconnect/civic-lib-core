# Module `api_utils`

## Classes

### `AIOHTTPTransport(self, url: str, headers: Union[Mapping[str, str], Mapping[multidict._multidict.istr, str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, Iterable[Tuple[Union[str, multidict._multidict.istr], str]], NoneType] = None, cookies: Union[Mapping[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]], Iterable[Tuple[str, Union[str, ForwardRef('BaseCookie[str]'), ForwardRef('Morsel[Any]')]]], ForwardRef('BaseCookie[str]'), NoneType] = None, auth: Union[aiohttp.helpers.BasicAuth, ForwardRef('AppSyncAuthentication'), NoneType] = None, ssl: Union[ssl.SSLContext, bool, aiohttp.client_reqrep.Fingerprint, str] = 'ssl_warning', timeout: Optional[int] = None, ssl_close_timeout: Union[int, float, NoneType] = 10, json_serialize: Callable = <function dumps at 0x0000018C0234D4E0>, client_session_args: Optional[Dict[str, Any]] = None) -> None`

:ref:`Async Transport <async_transports>` to execute GraphQL queries
on remote servers with an HTTP connection.

This transport use the aiohttp library with asyncio.

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

## Functions

### `async_paged_query(url: str, api_key: str, query, data_path: list[str], page_info_path: list[str] | None = None) -> list`

Asynchronously fetch paginated GraphQL results.

Args:
    url (str): GraphQL endpoint.
    api_key (str): API key.
    query: gql.Query object.
    data_path (list): Path to the list of edges.
    page_info_path (list | None): Path to pageInfo block. If not provided, attempts to infer.

Returns:
    list: All collected items from all pages.

### `paged_query(url: str, api_key: str, query, data_path: list[str]) -> list`

Run a paged GraphQL query synchronously.

Args:
    url (str): GraphQL endpoint.
    api_key (str): API key.
    query: gql.Query object.
    data_path (list): Path to the list of edges.

Returns:
    list: All collected items.
