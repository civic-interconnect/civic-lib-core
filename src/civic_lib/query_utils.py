"""
civic_lib/query_utils.py

Generic pagination helper for GraphQL queries using gql client.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from typing import Any

from civic_lib import log_utils

__all__ = ["fetch_paginated"]


logger = log_utils.logger


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
        query (gql.Query): The GraphQL query object.
        data_key (str): Key in response that contains the paginated data.
        variables (dict, optional): Initial query variables.

    Returns:
        list[dict]: Combined list of all 'node' objects from paginated results.
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
