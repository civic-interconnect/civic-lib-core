"""
Test cases for civic-lib-core.schema_utils module.
"""

import json
from pathlib import Path

import pytest

from civic_lib_core import schema_utils


def test_load_json_success(tmp_path: Path) -> None:
    file = tmp_path / "test.json"
    file.write_text('{"key": "value"}', encoding="utf-8")
    result = schema_utils.load_json(file)
    assert result == {"key": "value"}


def test_load_json_file_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        schema_utils.load_json(missing)


def test_hash_dict_consistent() -> None:
    data = {"b": 2, "a": 1}
    hash1 = schema_utils.hash_dict(data)
    hash2 = schema_utils.hash_dict({"a": 1, "b": 2})
    assert hash1 == hash2


def test_detect_schema_change_when_file_missing(tmp_path: Path) -> None:
    missing_file = tmp_path / "schema.json"
    changed = schema_utils.detect_schema_change(missing_file, {"x": 1})
    assert changed is True


def test_detect_schema_change_when_different(tmp_path: Path) -> None:
    file = tmp_path / "schema.json"
    file.write_text(json.dumps({"x": 1}), encoding="utf-8")
    changed = schema_utils.detect_schema_change(file, {"x": 2})
    assert changed is True


def test_detect_schema_change_when_same(tmp_path: Path) -> None:
    file = tmp_path / "schema.json"
    file.write_text(json.dumps({"x": 1}), encoding="utf-8")
    changed = schema_utils.detect_schema_change(file, {"x": 1})
    assert changed is False
