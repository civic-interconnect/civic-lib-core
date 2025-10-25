"""
Test cases for civic-lib-core.path_utils module.
"""

from pathlib import Path
import tempfile

from civic_lib_core import fs_utils


def test_resolve_path_returns_absolute_path():
    relative = "some/folder/file.txt"
    result = fs_utils.resolve_path(relative)
    assert isinstance(result, Path)
    assert result.is_absolute()
    assert result.as_posix().endswith("some/folder/file.txt")


def test_safe_filename():
    assert fs_utils.safe_filename("My Report/Name") == "my_report_name"
    assert fs_utils.safe_filename("AGENT NAME") == "agent_name"
    assert fs_utils.safe_filename("already_safe") == "already_safe"


def test_ensure_dir(tmp_path: Path):
    test_dir = tmp_path / "nested" / "folder"
    result = fs_utils.ensure_dir(test_dir)
    assert result.exists()
    assert result.is_dir()


def test_ensure_dir_creates_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        new_folder = Path(tmpdir) / "new_folder"
        assert not new_folder.exists()
        result = fs_utils.ensure_dir(new_folder)
        assert result.exists()
        assert result.is_dir()
        assert result == new_folder


def test_ensure_dir_on_existing_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        result = fs_utils.ensure_dir(tmp_path)
        assert result.exists()
        assert result.is_dir()
        assert result == tmp_path
