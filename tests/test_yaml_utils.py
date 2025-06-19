from civic_lib import yaml_utils


def test_write_and_read_yaml(tmp_path):
    data = {"name": "Test Agent", "version": "1.2.3"}
    file_path = tmp_path / "sample.yaml"

    # Write YAML
    yaml_utils.write_yaml(data, file_path)
    assert file_path.exists()

    # Read YAML
    result = yaml_utils.read_yaml(file_path)
    assert result == data
