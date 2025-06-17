import pytest
from civic_lib import query_utils

@pytest.mark.asyncio
async def test_fetch_paginated_mock():
    """
    Simple mock test for fetch_paginated.
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
                        "pageInfo": {"hasNextPage": True, "endCursor": "cursor1"}
                    }
                }
            else:
                return {
                    "testData": {
                        "edges": [{"node": {"id": 2}}],
                        "pageInfo": {"hasNextPage": False, "endCursor": None}
                    }
                }

    mock_client = MockClient()
    query = None  # Not used by mock
    results = await query_utils.fetch_paginated(mock_client, query, data_key="testData")
    assert len(results) == 2
