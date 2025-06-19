"""
Test cases for civic_lib.api_utils module.
"""

from unittest.mock import AsyncMock, patch

import pytest

from civic_lib import api_utils


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

    with patch("civic_lib.api_utils.Client") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.execute_async = AsyncMock(return_value=fake_data["data"])

        result = await api_utils.async_paged_query(
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
        "civic_lib.api_utils.async_paged_query", return_value=["item1", "item2"]
    ) as mock_async:
        result = api_utils.paged_query(
            url="https://fake.url/graphql", api_key="key", query={}, data_path=["items"]
        )
        assert result == ["item1", "item2"]
        mock_async.assert_called_once()
