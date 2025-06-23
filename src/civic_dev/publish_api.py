"""
publish_api.py

Generate and update application interface documentation.

This script:
- Initializes logging
- Generates a summary YAML file
- Generates Markdown documentation of public API
- Writes results to the appropriate locations

Intended for developer use via CLI or automation:
    civic-dev publish-api
"""

import typer

from civic_lib_core import doc_utils, log_utils

logger = log_utils.logger

app = typer.Typer(help="Generate API summary and reference documentation.")


@app.command("publish-api")
def main():
    """
    Regenerate summary and reference API documentation.
    """
    typer.echo("Generating API documentation...")
    try:
        doc_utils.generate_summary_yaml()
        doc_utils.generate_api_docs()
        doc_utils.generate_mkdocs_config()
        typer.echo("Update complete.")
    except Exception as e:
        logger.error(f"Error during API generation: {e}")
        typer.echo(f"Error during publish-api: {e}")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    main()
