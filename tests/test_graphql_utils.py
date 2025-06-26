"""
Test cases for civic-lib-core.api_utils module.
"""

from unittest.mock import AsyncMock, patch

import pytest
from gql.transport.exceptions import (
    TransportProtocolError,
    TransportQueryError,
    TransportServerError,
)

from civic_lib_core import graphql_utils


@pytest.mark.asyncio
async def test_async_paged_query_single_page():
    fake_data = {
        "data": {
            "items": {
                "edges": [{"node": {"id": 1}}],
                "pageInfo": {"hasNextPage": False, "endCursor": None},
            }
        }
    }

    with patch("civic_lib_core.graphql_utils.Client") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.execute_async = AsyncMock(return_value=fake_data["data"])

        result = await graphql_utils.async_paged_query(
            url="https://fake.url/graphql",
            api_key="fakekey",
            query={},
            data_path=["items", "edges"],
            page_info_path=["items", "pageInfo"],
        )

        assert isinstance(result, list)
        assert result == [{"node": {"id": 1}}]


def test_paged_query_sync_wrapper():
    with patch(
        "civic_lib_core.graphql_utils.async_paged_query", return_value=["item1", "item2"]
    ) as mock_async:
        result = graphql_utils.paged_query(
            url="https://fake.url/graphql", api_key="key", query={}, data_path=["items"]
        )
        assert result == ["item1", "item2"]
        mock_async.assert_called_once()


def test_handle_transport_server_error_forbidden():
    error = TransportServerError("403 Forbidden")
    result = graphql_utils.handle_transport_errors(error, resource_name="TestResource")
    assert result == "TestResource access not yet granted"


def test_handle_transport_query_error():
    error = TransportQueryError("GraphQL query failed")
    with pytest.raises(TransportQueryError):
        graphql_utils.handle_transport_errors(error, resource_name="TestResource")


def test_handle_transport_protocol_error():
    error = TransportProtocolError("Transport failed")
    with pytest.raises(TransportProtocolError):
        graphql_utils.handle_transport_errors(error, resource_name="TestResource")


def test_handle_generic_exception():
    error = Exception("Something went wrong")
    with pytest.raises(Exception) as exc_info:
        graphql_utils.handle_transport_errors(error, resource_name="TestResource")
    assert str(exc_info.value) == "Something went wrong"


@pytest.mark.asyncio
async def test_fetch_paginated_mock():
    """
    Simulate a paginated GraphQL response using a mock client.
    Ensures data is fetched across multiple pages.
    """

    class MockClient:
        def __init__(self):
            self.call_count = 0

        async def execute_async(self, query, variable_values=None):
            self.call_count += 1
            if self.call_count == 1:
                return {
                    "testData": {
                        "edges": [{"node": {"id": 1}}],
                        "pageInfo": {"hasNextPage": True, "endCursor": "cursor1"},
                    }
                }
            elif self.call_count == 2:
                return {
                    "testData": {
                        "edges": [{"node": {"id": 2}}],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            else:
                raise Exception("Too many pages requested")

    mock_client = MockClient()
    fake_query = object()  # Simulated query object
    results = await graphql_utils.fetch_paginated(mock_client, fake_query, data_key="testData")

    assert isinstance(results, list)
    assert results == [{"id": 1}, {"id": 2}]
    assert mock_client.call_count == 2
