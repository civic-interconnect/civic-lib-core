"""
civic_lib_core/api_utils.py

Core utilities for API authentication, configuration loading, and logging.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import asyncio

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from civic_lib_core import log_utils

__all__ = [
    "async_paged_query",
    "paged_query",
]

logger = log_utils.logger


async def async_paged_query(
    url: str,
    api_key: str,
    query,
    data_path: list[str],
    page_info_path: list[str] | None = None,
) -> list:
    """
    Asynchronously fetch paginated GraphQL results.

    Args:
        url (str): GraphQL endpoint.
        api_key (str): API key.
        query: gql.Query object.
        data_path (list): Path to the list of edges.
        page_info_path (list | None): Path to pageInfo block. If not provided, attempts to infer.

    Returns:
        list: All collected items from all pages.
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

        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return collected


def paged_query(
    url: str,
    api_key: str,
    query,
    data_path: list[str],
) -> list:
    """
    Run a paged GraphQL query synchronously.

    Args:
        url (str): GraphQL endpoint.
        api_key (str): API key.
        query: gql.Query object.
        data_path (list): Path to the list of edges.

    Returns:
        list: All collected items.
    """
    return asyncio.run(async_paged_query(url, api_key, query, data_path))
