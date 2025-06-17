"""
civic_lib/query_utils.py

Generic pagination helper for GraphQL queries using gql client.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from loguru import logger


async def fetch_paginated(client, query, data_key, variables=None):
    """
    Fetch all pages of a paginated GraphQL query.

    Args:
        client (gql.Client): Initialized GraphQL client.
        query (gql.Query): The GraphQL query object.
        data_key (str): The key under which results are stored in the response.
        variables (dict, optional): Additional query variables.

    Returns:
        list: Complete list of records across all pages.
    """
    all_results = []
    after = None

    while True:
        page_vars = variables.copy() if variables else {}
        page_vars.update({"first": 100, "after": after})

        response = await client.execute_async(query, variable_values=page_vars)
        page = response[data_key]
        edges = page["edges"]

        for edge in edges:
            all_results.append(edge["node"])

        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    logger.info(f"Fetched {len(all_results)} total records for {data_key}")
    return all_results
