"""
Test cases for civic-lib-core.config_utils module.
"""

from pathlib import Path
import tempfile

import pytest
import yaml

from civic_lib_core import config_utils


def test_load_yaml_config_success(tmp_path: Path):
    config_data = {"key1": "value1", "key2": 2}
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data))

    result = config_utils.load_yaml_config("config.yaml", root_dir=tmp_path)
    assert result == config_data


def test_load_yaml_config_not_found(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        config_utils.load_yaml_config("missing.yaml", root_dir=tmp_path)


def test_load_version_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        version_file = tmp_path / "VERSION"
        version_file.write_text("2.3.4")

        version = config_utils.load_version("VERSION", root_dir=tmp_path)
        assert version == "2.3.4"


def test_load_version_missing():
    with pytest.raises(SystemExit):
        config_utils.load_version("VERSION", root_dir=Path("nonexistent_path"))


def test_parse_version_valid():
    assert config_utils.parse_version("1.2.3") == (1, 2, 3)


def test_parse_version_invalid():
    with pytest.raises(ValueError):
        config_utils.parse_version("version_x.y.z")
