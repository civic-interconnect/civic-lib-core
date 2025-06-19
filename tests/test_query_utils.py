"""
Test cases for civic_lib.query_utils module.
"""

import pytest

from civic_lib import query_utils


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
    results = await query_utils.fetch_paginated(mock_client, fake_query, data_key="testData")

    assert isinstance(results, list)
    assert results == [{"id": 1}, {"id": 2}]
    assert mock_client.call_count == 2
