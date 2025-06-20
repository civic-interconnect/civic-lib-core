"""
civic_lib_core/report_constants.py

Shared constants for report generation, reading, validation, and indexing.
Used across Civic Interconnect agents and admin tools.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

# ----------------------
# Path-related constants
# ----------------------

# Path to the top-level index file listing latest agent reports
OUTPUT_FILE = Path("reports") / "index.md"

# Path where archived reports (e.g., older than 30 days) may be moved
ARCHIVE_DIR = Path("reports") / "archive"

# Root directory where reports are stored
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------
# Format and extension constants
# ----------------------

# Date-only format used in report filenames
DATE_ONLY_FORMAT = "%Y-%m-%d"

# File extension used for agent reports
REPORT_EXTENSION = ".json"

# Default timestamp format (UTC, consistent across agents)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S UTC"

# ----------------------
# Validation constants
# ----------------------

# Expected keys in every valid agent report
EXPECTED_REPORT_KEYS = {
    "agent",
    "timestamp",
    "record_count",
    "agent_version",
    "schema_version",
    "lib_version",
    "results",
}
