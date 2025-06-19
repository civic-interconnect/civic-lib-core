"""
Test cases for civic_lib.version_utils module.
"""

from civic_lib import version_utils


def test_check_version_match():
    assert version_utils.check_version("1.2.3", "1.0.0") is True


def test_check_version_mismatch():
    assert version_utils.check_version("2.0.0", "1.9.9") is False


def test_check_version_identical():
    assert version_utils.check_version("1.0.0", "1.0.0") is True


def test_check_version_patch_diff():
    assert version_utils.check_version("1.2.3", "1.2.4") is True


def test_check_version_minor_diff():
    assert version_utils.check_version("1.2.3", "1.5.0") is True
