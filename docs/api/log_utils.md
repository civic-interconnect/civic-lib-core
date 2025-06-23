# Module `log_utils`

## Functions

### `init_logger(log_level=None, log_to_console=True)`

Initialize loguru logging once per session.

If no log level is provided, attempts to load it from config.yaml as 'log_level'.
Defaults to INFO if not found or config is missing.

Args:
    log_level (str | None): Optional log level override (default: config.yaml or "INFO").
    log_to_console (bool): If True, logs to stderr in addition to file.

### `log_agent_end(agent_name, status='success')`

Log the end of an agent with its status and UTC timestamp.

### `log_agent_start(agent_name)`

Log the start of an agent by name.
