"""
Test cases for civic_lib.path_utils module.
"""

import tempfile
from pathlib import Path

from civic_lib import path_utils


def test_safe_filename():
    assert path_utils.safe_filename("My Report/Name") == "my_report_name"
    assert path_utils.safe_filename("AGENT NAME") == "agent_name"
    assert path_utils.safe_filename("already_safe") == "already_safe"


def test_ensure_dir(tmp_path: Path):
    test_dir = tmp_path / "nested" / "folder"
    result = path_utils.ensure_dir(test_dir)
    assert result.exists()
    assert result.is_dir()


def test_ensure_dir_creates_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        new_folder = Path(tmpdir) / "new_folder"
        assert not new_folder.exists()
        result = path_utils.ensure_dir(new_folder)
        assert result.exists()
        assert result.is_dir()
        assert result == new_folder


def test_ensure_dir_on_existing_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        result = path_utils.ensure_dir(tmp_path)
        assert result.exists()
        assert result.is_dir()
        assert result == tmp_path
