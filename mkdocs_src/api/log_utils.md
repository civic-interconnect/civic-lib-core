# Module `log_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `init_logger(log_level: str | None = None, log_to_console: bool = True) -> None`

Initialize Loguru logging once per session.

Automatically loads logging config from project_policy.yaml
if available. Defaults to INFO and logs/{date}.log if not found.

Args:
    log_level (str | None): Optional log level override.
    log_to_console (bool): Whether to also log to stderr.

Example:
    from civic_lib_core import log_utils
    log_utils.init_logger("INFO")

### `log_agent_end(agent_name: str, status: str = 'success') -> None`

Log the end of an agent with its status and UTC timestamp.

Args:
    agent_name (str): Name of the agent.
    status (str): e.g. "success" or "error".

### `log_agent_start(agent_name: str) -> None`

Log the start of an agent by name.

Args:
    agent_name (str): Name of the agent.

### `now_utc_str(fmt: str = '%Y-%m-%d %H:%M:%S UTC') -> str`

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.
