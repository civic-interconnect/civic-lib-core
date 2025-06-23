# Module `api_utils`

## Functions

### `paged_query(url, api_key, query, data_path)`

Run a paged GraphQL query synchronously.

Args:
    url (str): GraphQL endpoint.
    api_key (str): API key.
    query: gql.Query object.
    data_path (list): Path to the list of edges.

Returns:
    list: All collected items.
