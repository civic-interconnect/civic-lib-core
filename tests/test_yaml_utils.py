from pathlib import Path
import tempfile

from civic_lib_core.yaml_utils import read_yaml, write_yaml


def test_roundtrip_yaml():
    data = {"a": 1, "b": {"c": 2}}
    tmp = Path(tempfile.gettempdir()) / "test.yaml"
    write_yaml(data, tmp)
    assert read_yaml(tmp) == data
