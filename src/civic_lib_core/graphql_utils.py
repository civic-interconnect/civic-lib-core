"""civic_lib_core/graphql_utils.py.

Unified GraphQL utilities for Civic Interconnect projects.

Provides:
- Consistent error handling for GraphQL transport errors
- Asynchronous and synchronous helpers for paginated GraphQL queries
- Utilities to fetch all pages of results from GraphQL APIs

"""

import asyncio
from collections.abc import Mapping, Sequence
from typing import Any

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import (
    TransportProtocolError,
    TransportQueryError,
    TransportServerError,
)

from civic_lib_core import log_utils

__all__ = [
    "async_paged_query",
    "paged_query",
    "fetch_paginated",
    "handle_transport_errors",
]

logger = log_utils.logger


def handle_transport_errors(e: Exception, resource_name: str = "resource") -> str:
    """Handle GraphQL transport errors with appropriate logging and re-raising.

    Args:
        e (Exception): The exception to handle, typically a GraphQL transport error.
        resource_name (str, optional): Name of the resource being accessed for
            logging context. Defaults to "resource".

    Returns:
        str: Error message for 403 Forbidden errors, indicating access not granted.

    Raises:
        Exception: Re-raises the original exception after logging the appropriate
            error message based on the exception type.
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


async def async_paged_query(
    url: str,
    api_key: str,
    query: Any,
    data_path: Sequence[str],
    page_info_path: Sequence[str] | None = None,
) -> list[dict[str, Any]]:
    """Execute a paginated GraphQL query asynchronously and fetch all results.

    Args:
        url (str): The GraphQL endpoint URL.
        api_key (str): Bearer token for API authentication.
        query (Any): The GraphQL query object to execute.
        data_path (Sequence[str]): Path to the data array in the response.
        page_info_path (Sequence[str] | None, optional): Path to pageInfo in the response.
            If None, will attempt to infer from data_path. Defaults to None.

    Returns:
        list[dict[str, Any]]: List of all records collected from all pages.

    Raises:
        ValueError: If page_info_path is None and pageInfo cannot be inferred.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)

    async with Client(transport=transport, fetch_schema_from_transport=False) as client:
        collected: list[dict[str, Any]] = []
        after = None

        while True:
            variables = {"first": 100, "after": after}
            response = await client.execute(query, variable_values=variables)

            data: Any = response
            for key in data_path:
                data = data[key]
            collected.extend(data)

            if page_info_path is None:
                try:
                    page_info: Any = response
                    for key in data_path[:-1]:
                        page_info = page_info[key]
                    page_info = page_info["pageInfo"]
                except (KeyError, TypeError) as e:
                    raise ValueError(
                        "Could not infer page_info path. Please specify page_info_path."
                    ) from e
            else:
                page_info: Any = response
                for key in page_info_path:
                    page_info = page_info[key]

            if not page_info.get("hasNextPage"):
                break

            after = page_info.get("endCursor")

        logger.info(f"Fetched {len(collected)} records from {url}.")
        return collected


def paged_query(
    url: str,
    api_key: str,
    query: Any,
    data_path: Sequence[str],
) -> list[dict[str, Any]]:
    """Execute a paginated GraphQL query synchronously and fetch all results.

    This is a synchronous wrapper around async_paged_query that uses asyncio.run
    to execute the asynchronous query in a blocking manner.

    Args:
        url (str): The GraphQL endpoint URL.
        api_key (str): Bearer token for API authentication.
        query (Any): The GraphQL query object to execute.
        data_path (Sequence[str]): Path to the data array in the response.

    Returns:
        list[dict[str, Any]]: List of all records collected from all pages,
            or empty list if an error occurs.
    """
    try:
        return asyncio.run(async_paged_query(url, api_key, query, data_path))
    except Exception as e:
        handle_transport_errors(e, resource_name=url)
        return []


async def fetch_paginated(
    client: Any,
    query: Any,
    data_key: str,
    variables: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Fetch all paginated results from a GraphQL query using cursor-based pagination.

    This function automatically handles pagination by making multiple requests to fetch
    all available data, using the standard GraphQL cursor-based pagination pattern with
    'first', 'after', 'edges', 'pageInfo', 'hasNextPage', and 'endCursor' fields.

    Args:
        client (Any): The GraphQL client instance that supports async execution.
        query (Any): The GraphQL query object to execute.
        data_key (str): The key in the response data that contains the paginated results.
        variables (Mapping[str, Any] | None, optional): Additional variables to pass
            with the query. Defaults to None.

    Returns:
        list[dict[str, Any]]: A list containing all the 'node' objects from all pages
            of results combined.

    Example:
        ```python
        query = gql("query { users(first: $first, after: $after) { ... } }")
        users = await fetch_paginated(client, query, "users", {"status": "active"})
        ```

    Note:
        - Uses a fixed page size of 100 items per request
        - Automatically extracts 'node' objects from GraphQL 'edges'
        - Logs the total number of records fetched upon completion
    """
    all_results: list[dict[str, Any]] = []
    after = None

    while True:
        page_vars = dict(variables) if variables else {}
        page_vars.update({"first": 100, "after": after})

        response = await client.execute_async(query, variable_values=page_vars)
        page = response[data_key]
        edges = page.get("edges", [])

        all_results.extend(edge["node"] for edge in edges)

        if not page.get("pageInfo", {}).get("hasNextPage"):
            break

        after = page["pageInfo"].get("endCursor")

    logger.info(f"Fetched {len(all_results)} total records for '{data_key}'.")
    return all_results
