from pathlib import Path

from civic_lib_core import log_utils
from civic_lib_core.path_utils import ensure_dir
from civic_lib_core.report_constants import REPORTS_DIR
from civic_lib_core.report_reader import get_latest_report
from civic_lib_core.report_utils import get_agent_name_from_path

__all__ = ["generate_index"]

logger = log_utils.logger


def generate_index(report_dir: Path = REPORTS_DIR) -> None:
    """
    Generate a Markdown index listing the latest report from each agent.

    Args:
        report_dir (Path): The base `reports/` directory to scan.
    """
    logger.info("Generating index of agent reports...")

    index_file = report_dir / "index.md"
    ensure_dir(index_file.parent)

    if index_file.exists():
        logger.debug(f"Removing old index file at {index_file}")
        index_file.unlink()

    logger.debug(f"Creating new index file at {index_file}")
    lines = ["# Civic Interconnect Agent Reports\n"]

    for agent_dir in sorted(report_dir.iterdir(), key=lambda p: p.name.lower()):
        if agent_dir.is_dir():
            latest = get_latest_report(agent_dir)
            if latest:
                relative_path = latest.relative_to(report_dir)
                agent_display = get_agent_name_from_path(latest) or agent_dir.name
                lines.append(f"- **{agent_display}**: [Latest Report]({relative_path})")

    index_file.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Index written to {index_file}")
