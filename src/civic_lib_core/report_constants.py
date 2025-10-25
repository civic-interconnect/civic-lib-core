"""civic_lib_core/report_constants.py.

Shared constants for report generation, reading, validation, and indexing.
Used across Civic Interconnect agents and admin tools.

"""

from pathlib import Path

# ----------------------
# Path-related constants
# ----------------------

# Root directory where reports are stored
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Path to the top-level index file listing latest agent reports
OUTPUT_FILE = REPORTS_DIR / "index.md"

# Path where archived reports (e.g., older than 30 days) are moved
ARCHIVE_DIR = REPORTS_DIR / "archive"

# ----------------------
# Format and extension constants
# ----------------------

# Date-only format used in report filenames (e.g. "2024-07-01")
DATE_ONLY_FORMAT = "%Y-%m-%d"

# Default timestamp format (UTC, consistent across agents)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S UTC"

# File extension used for agent reports
REPORT_EXTENSION = ".json"

# Suffix for archived report files
ARCHIVED_SUFFIX = ".archived.json"

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
