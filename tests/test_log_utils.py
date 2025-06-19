"""
Test cases for civic_lib.log_utils module.
"""

import os
from pathlib import Path

from civic_lib import log_utils


def test_logger_initializes(tmp_path: Path) -> None:
    """
    Test that init_logger creates a logs/ folder and writes a log file.
    """
    # Change working directory to temp
    os.chdir(tmp_path)

    log_utils.init_logger()

    log_dir = tmp_path / "logs"
    assert log_dir.exists()
    files = list(log_dir.iterdir())
    assert len(files) >= 1
    assert files[0].suffix == ".log"


def test_lib_version_reads_expected_version(tmp_path: Path) -> None:
    """
    Test lib_version reads from the VERSION file correctly.
    """
    version_file = tmp_path / "VERSION"
    version_file.write_text("v9.9.9")

    # Patch the internal VERSION_FILE path
    original_version_path = log_utils.VERSION_FILE
    log_utils.VERSION_FILE = version_file

    try:
        result = log_utils.lib_version()
        assert result == "v9.9.9"
    finally:
        # Restore the original VERSION path
        log_utils.VERSION_FILE = original_version_path


def test_lib_version_returns_unknown_if_missing(tmp_path: Path) -> None:
    """
    Test fallback when VERSION file is missing.
    """
    original_version_path = log_utils.VERSION_FILE
    log_utils.VERSION_FILE = tmp_path / "VERSION"

    try:
        result = log_utils.lib_version()
        assert result == "unknown"
    finally:
        log_utils.VERSION_FILE = original_version_path
