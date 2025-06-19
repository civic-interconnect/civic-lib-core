"""
Test cases for civic_lib.file_utils module.
"""

from pathlib import Path

from civic_lib import file_utils


def test_resolve_path_returns_absolute_path():
    relative = "some/folder/file.txt"
    result = file_utils.resolve_path(relative)
    assert isinstance(result, Path)
    assert result.is_absolute()
    assert result.as_posix().endswith("some/folder/file.txt")
