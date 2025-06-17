import pytest
from civic_lib import error_utils
from gql.transport.exceptions import (
    TransportServerError,
    TransportQueryError,
    TransportProtocolError,
)

def test_handle_transport_server_error_forbidden():
    error = TransportServerError("403 Forbidden")
    result = error_utils.handle_transport_errors(error, resource_name="TestResource")
    assert result == "TestResource access not yet granted"

def test_handle_transport_query_error():
    error = TransportQueryError("GraphQL query failed")
    with pytest.raises(TransportQueryError):
        error_utils.handle_transport_errors(error, resource_name="TestResource")

def test_handle_transport_protocol_error():
    error = TransportProtocolError("Transport failed")
    with pytest.raises(TransportProtocolError):
        error_utils.handle_transport_errors(error, resource_name="TestResource")

def test_handle_generic_exception():
    error = Exception("Something went wrong")
    with pytest.raises(Exception):
        error_utils.handle_transport_errors(error, resource_name="TestResource")
