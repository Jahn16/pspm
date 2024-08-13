"""main."""

from __future__ import annotations

from typing import Annotated

import typer
from rich import print as rprint

from pspm.services.bootstrap import bootstrap_project
from pspm.services.dependencies import (
    install_dependencies,
    manage_dependency,
)

app = typer.Typer()


@app.callback()
def callback() -> None:
    """Python simple package manager."""


@app.command()
def init(name: str, description: str = "") -> None:
    """Create initial project structure.

    Args:
        name: Project name
        description: Project description
    """
    bootstrap_project(name, description or None)


@app.command()
def install() -> None:
    """Install all dependencies and the package itself."""
    rprint("Installing project")
    install_dependencies()


@app.command()
def add(
    package: str, group: Annotated[str, typer.Option("--group", "-g")] = ""
) -> None:
    """Add package to pyproject, install it and lock version."""
    rprint(f"Adding package {package}")
    manage_dependency("add", package, group or None)


@app.command()
def remove(
    package: str, group: Annotated[str, typer.Option("--group", "-g")] = ""
) -> None:
    """Remove package from pyproject, uninstall it and lock version."""
    rprint(f"Removing package {package}")
    manage_dependency("remove", package, group or None)
