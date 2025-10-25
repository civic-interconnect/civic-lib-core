"""
Test cases for civic-lib-core.graphql_utils module.
"""

from unittest.mock import patch

from gql.transport.exceptions import (
    TransportProtocolError,
    TransportQueryError,
    TransportServerError,
)
import pytest

from civic_lib_core import graphql_utils


def test_paged_query_sync_wrapper():
    """
    Test the synchronous wrapper for async_paged_query.
    """
    with patch(
        "civic_lib_core.graphql_utils.async_paged_query", return_value=["item1", "item2"]
    ) as mock_async:
        result = graphql_utils.paged_query(
            url="https://fake.url/graphql",
            api_key="key",
            query={},
            data_path=["items"],
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
