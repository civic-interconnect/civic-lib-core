"""civic_lib_core/log_utils.py.

Centralized logging for Civic Interconnect agents and libraries.

"""

import sys

from loguru import logger  # type: ignore

from civic_lib_core import fs_utils, project_policy
from civic_lib_core.date_utils import now_utc_str

__all__ = [
    "init_logger",
    "log_agent_end",
    "log_agent_start",
    "logger",
]

_logger_initialized = False


def init_logger(log_level: str | None = None, log_to_console: bool = True) -> None:
    """Initialize Loguru logging once per session.

    Loads config from project_policy.yaml if available.

    Args:
        log_level (Optional[str]): Override log level (e.g. "DEBUG").
        log_to_console (bool): Whether to also log to stderr.
    """
    global _logger_initialized
    if _logger_initialized:
        logger.debug("Logger already initialized.")  # type: ignore[attr-defined]
        return

    # Remove default handlers
    logger.remove()  # type: ignore[attr-defined]

    layout = fs_utils.discover_project_layout()
    project_root = layout.project_root

    try:
        policy = project_policy.load_project_policy(project_root)
    except Exception as e:
        policy = {}
        logger.warning(f"Failed to load project policy: {e}")  # type: ignore[attr-defined]

    log_subdir = policy.get("log_subdir", "logs")
    log_file_template = policy.get("log_file_template", "{time:YYYY-MM-DD}.log")
    retention_days = policy.get("log_retention_days", 7)

    logs_dir = project_root / log_subdir
    fs_utils.ensure_dir(logs_dir)

    log_file_path = logs_dir / log_file_template

    try:
        runtime_config_path = fs_utils.get_runtime_config_path(project_root)
        if runtime_config_path.exists():
            import yaml  # type: ignore

            runtime_cfg = yaml.safe_load(runtime_config_path.read_text())
            runtime_log_level = runtime_cfg.get("log_level")
        else:
            runtime_log_level = None
    except Exception as e:
        logger.warning(f"Failed to load runtime config: {e}")
        runtime_log_level = None

    level = (log_level or runtime_log_level or policy.get("log_level", "INFO")).upper().strip()

    # Add file sink with structured format
    logger.add(
        str(log_file_path),
        format="{time} | {level} | {message}",
        rotation="1 day",
        retention=f"{retention_days} days",
        encoding="utf-8",
        level=level,
        backtrace=True,
        diagnose=True,
    )

    if log_to_console:
        logger.add(
            sink=sys.stderr,
            format="<green>{time}</green> | <level>{level}</level> | {message}",
            level=level,
            backtrace=True,
            diagnose=True,
        )

    logger.info(f"===== Civic Interconnect logger initialized (level: {level}) =====")
    _logger_initialized = True


def log_agent_start(agent_name: str) -> None:
    """Log the start of an agent.

    Args:
        agent_name (str): Name of the agent.
    """
    logger.info(f"===== Starting {agent_name} =====")


def log_agent_end(agent_name: str, status: str = "success") -> None:
    """Log the end of an agent.

    Args:
        agent_name (str): Name of the agent.
        status (str): Status text (e.g. "success" or "error").
    """
    timestamp = now_utc_str()
    logger.info(f"===== {agent_name} completed with status: {status} at {timestamp} =====")
