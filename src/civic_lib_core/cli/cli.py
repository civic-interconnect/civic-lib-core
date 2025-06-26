"""
Stub CLI for civic-lib-core.

To extend this CLI, add more commands to the `app` instance.
"""

import typer

app = typer.Typer(help="CLI tools for civic-lib-core utilities.")


@app.command("hello")
def hello():
    """Basic test command."""
    typer.echo("Hello from civic-lib-core CLI (stub)!")
