"""
cli.py

Command-line interface (CLI) for civic-lib-core.

Provides repo-specific commands for:
- Starting the application locally for development or preview
- Running other local tasks specific to this repository

This CLI is intended for maintainers or users of this repository.

Run `civic-lib-core --help` for usage.
"""

import typer

from . import serve_app

app = typer.Typer(help="App Agents CLI")


@app.command("serve-app")
def serve_local_app():
    """
    Start the application locally for development or preview.
    """
    serve_app.main()


def main():
    app()


if __name__ == "__main__":
    main()
