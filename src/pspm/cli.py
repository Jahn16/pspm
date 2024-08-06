"""main."""

from typing import Annotated

import typer
from rich import print

from pspm.services.dependencies import add_dependency

app = typer.Typer()


@app.callback()
def callback() -> None:
    """Python simple package manager."""


@app.command()
def add(
    package: str, group: Annotated[str, typer.Option("--group", "-g")] = ""
) -> None:
    """Add package to pyproject, install it and lock version."""
    print(f"Adding package {package}")
    add_dependency(package, group or None)
