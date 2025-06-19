"""
civic_lib/api_utils.py

Core utilities for API authentication, configuration loading, and logging.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import asyncio
import os
import sys

import yaml
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from civic_lib import log_utils


def load_openstates_api_key():
    """
    Load the OpenStates API key from environment variables.

    Reads the OPENSTATES_API_KEY environment variable.
    If missing, logs an error and exits the program.

    Returns:
        str: The API key if found.

    Exits:
        If the API key is not found, exits with an error message.
    """
    key = os.getenv("OPENSTATES_API_KEY")

    if not key:
        log_utils.logger.error(
            "OpenStates API key missing. is missing.\n"
            "Fix: Add OPENSTATES_API_KEY to your .env file or system environment variables."
        )
        sys.exit("Error: OPENSTATES_API_KEY is required.")

    log_utils.logger.debug("OpenStates API key loaded successfully.")
    return key


async def async_paged_query(url, api_key, query, data_path):
    headers = {"Authorization": f"Bearer {api_key}"}
    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    collected = []
    after = None

    while True:
        variables = {"first": 100, "after": after}
        response = await client.execute_async(query, variable_values=variables)

        # Traverse nested data_path to get to edges
        data = response
        for key in data_path:
            data = data[key]

        collected.extend(data)

        page_info = response["bills"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return collected


def paged_query(url, api_key, query, data_path):
    return asyncio.run(async_paged_query(url, api_key, query, data_path))


def load_yaml_config(config_path="config.yaml"):
    """
    Load YAML configuration file.
    """
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        log_utils.logger.info("Config loaded successfully.")
        return config
    except Exception as e:
        log_utils.logger.error(f"Failed to load config file: {str(e)}")
        sys.exit("Error: Failed to load config file.")


def load_version(version_path="VERSION"):
    """
    Load agent version string.
    """
    try:
        with open(version_path) as f:
            version = f.read().strip()
        log_utils.logger.info(f"Agent version: {version}")
        return version
    except Exception as e:
        log_utils.logger.error(f"Failed to load VERSION file: {str(e)}")
        sys.exit("Error: Failed to load VERSION file.")
