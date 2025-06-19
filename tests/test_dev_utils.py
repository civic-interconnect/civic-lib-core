"""
tests/test_dev_utils.py

Unit tests for civic_lib.dev_utils functions.
"""

from civic_lib.dev_utils import suggest_paths


def test_suggest_paths_simple_dict():
    response = {"data": {"items": [{"id": 1}, {"id": 2}], "meta": {"count": 2}}}
    paths = suggest_paths(response)
    path_strings = [" -> ".join(p[0]) for p in paths]

    assert any("data -> items" in s for s in path_strings)
    assert any("data -> meta -> count" in s for s in path_strings)


def test_suggest_paths_non_dict():
    assert suggest_paths("not a dict") == []  # type: ignore
