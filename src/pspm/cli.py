"""main."""

import typer

app = typer.Typer()


@app.callback()
def callback() -> None:
    """Python simple package manager."""


@app.command()
def add(package: str) -> None:
    """Add package to pyproject, install it and lock version."""
    typer.echo(f"Adding package {package}")
