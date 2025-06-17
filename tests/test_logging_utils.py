import os
from civic_lib import logging_utils

def test_logger_initializes(tmp_path):
    # Use pytest's tmp_path fixture as isolated temp directory
    os.chdir(tmp_path)

    logging_utils.init_logger()

    # Verify log folder created
    log_dir = tmp_path / "logs"
    assert log_dir.exists()
    assert any(log_dir.iterdir()) 
