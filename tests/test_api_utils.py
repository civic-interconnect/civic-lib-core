import pytest
from civic_lib import api_utils

def test_load_openstates_api_key_success(monkeypatch):
    monkeypatch.setenv("OPENSTATES_API_KEY", "fake_key_123")
    key = api_utils.load_openstates_api_key()
    assert key == "fake_key_123"

def test_load_openstates_api_key_failure(monkeypatch):
    monkeypatch.delenv("OPENSTATES_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        api_utils.load_openstates_api_key()
