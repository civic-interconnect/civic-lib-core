"""
serve_app.py

Serve the web application locally using Python's built-in HTTP server.

This command launches a local development server from the `docs/` directory,
allowing you to preview the static web application at http://localhost:8000.

This is intended for local testing and does not require a production web server.

Usage:
    app-agents serve-app
"""

import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="Serve the local web app from the docs directory.")


@app.command("serve-app")
def main():
    """
    Launch the local development server for the static web app.

    Serves the `docs/` directory using `python -m http.server 8000`.
    """
    docs_dir = Path("docs")

    if not docs_dir.exists():
        typer.echo("'docs/' directory not found.")
        raise typer.Exit(1)

    typer.echo("Serving app at http://localhost:8000 ...")
    subprocess.run(["python", "-m", "http.server", "8000"], cwd=docs_dir)


if __name__ == "__main__":
    main()
