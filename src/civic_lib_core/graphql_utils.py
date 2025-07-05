"""
civic_lib_core/graphql_utils.py

Unified GraphQL utilities for Civic Interconnect projects.

Provides:
- Consistent error handling for GraphQL transport errors
- Asynchronous and synchronous helpers for paginated GraphQL queries
- Utilities to fetch all pages of results from GraphQL APIs

Typical usage:

    from civic_lib_core import graphql_utils

    # Run a paginated GraphQL query asynchronously
    data = await graphql_utils.async_paged_query(...)

    # Or synchronously:
    data = graphql_utils.paged_query(...)
"""

import asyncio
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
    """
    Handle GraphQL transport errors with consistent logging and user-friendly feedback.

    Args:
        e (Exception): The exception raised by gql transport.
        resource_name (str): Human-readable name of the queried resource.

    Returns:
        str: Friendly message if known error (e.g., access not granted).

    Raises:
        Exception: Original exception for unhandled errors.
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
    data_path: list[str],
    page_info_path: list[str] | None = None,
) -> list[Any]:
    """
    Asynchronously fetch paginated GraphQL results.

    Args:
        url (str): GraphQL endpoint URL.
        api_key (str): Authorization token.
        query (gql.Query): Query object.
        data_path (list[str]): Path to the list of data edges.
        page_info_path (list[str] | None): Optional explicit path to pageInfo.

    Returns:
        list: Combined list of items from all pages.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    collected = []
    after = None

    while True:
        variables = {"first": 100, "after": after}
        response = await client.execute_async(query, variable_values=variables)

        data = response
        for key in data_path:
            data = data[key]
        collected.extend(data)

        # Locate pageInfo
        if page_info_path is None:
            try:
                page_info = response
                for key in data_path[:-1]:
                    page_info = page_info[key]
                page_info = page_info["pageInfo"]
            except (KeyError, TypeError) as e:
                raise ValueError(
                    "Could not infer page_info path. Please specify page_info_path."
                ) from e
        else:
            page_info = response
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
    data_path: list[str],
) -> list[Any]:
    """
    Run a paged GraphQL query synchronously.

    Args:
        url (str): GraphQL endpoint URL.
        api_key (str): Authorization token.
        query (gql.Query): Query object.
        data_path (list[str]): Path to the list of data edges.

    Returns:
        list: Combined results from all pages.

    Raises:
        Exception: Any error raised by async_paged_query.
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
    variables: dict | None = None,
) -> list[dict]:
    """
    Fetch all pages of a paginated GraphQL query.

    Args:
        client (gql.Client): Initialized GraphQL client.
        query (gql.Query): Query object.
        data_key (str): Key containing the paginated data.
        variables (dict | None): Optional base query variables.

    Returns:
        list[dict]: Combined list of node dicts from all pages.
    """
    all_results = []
    after = None

    while True:
        page_vars = variables.copy() if variables else {}
        page_vars.update({"first": 100, "after": after})

        response = await client.execute_async(query, variable_values=page_vars)
        page = response[data_key]
        edges = page.get("edges", [])

        all_results.extend(edge["node"] for edge in edges)

        if not page.get("pageInfo", {}).get("hasNextPage"):
            break

        after = page["pageInfo"].get("endCursor")

    logger.info(f"Fetched {len(all_results)} total records for '{data_key}'")
    return all_results
