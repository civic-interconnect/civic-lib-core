# Module `query_utils`

## Classes

### `Any(self, /, *args, **kwargs)`

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

## Functions

### `fetch_paginated(client: Any, query: Any, data_key: str, variables: dict | None = None) -> list[dict]`

Fetch all pages of a paginated GraphQL query.

Args:
    client (gql.Client): Initialized GraphQL client.
    query (gql.Query): The GraphQL query object.
    data_key (str): Key in response that contains the paginated data.
    variables (dict, optional): Initial query variables.

Returns:
    list[dict]: Combined list of all 'node' objects from paginated results.
