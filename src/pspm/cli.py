"""Module to define cli commands."""

# ruff: noqa: FBT001 FBT002 B006 UP007
from __future__ import annotations

import importlib.metadata
from typing import Annotated, Optional

import typer
from rich import print as rprint

from pspm.services.bootstrap import bootstrap_project
from pspm.services.dependencies import (
    install_dependencies,
    manage_dependency,
    upgrade_dependencies,
)
from pspm.services.run import run_command

app = typer.Typer(no_args_is_help=True, invoke_without_command=True)


def _version_callback(value: bool) -> None:
    if value:
        version = importlib.metadata.version("pspm")
        rprint(version)


@app.callback()
def callback(
    version: Annotated[  # noqa: ARG001
        Optional[bool],
        typer.Option("--version", callback=_version_callback, is_eager=True),
    ] = None,
) -> None:
    """Python simple package manager."""


@app.command()
def init(
    name: str,
    description: str = "",
    installable: Annotated[
        bool, typer.Option("--installable/--not-installable")
    ] = True,
) -> None:
    """Create initial project structure.

    Args:
        name: Project name
        description: Project description
        installable: Whether the project is instalabble
    """
    bootstrap_project(name, description or None, installable=installable)


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


@app.command()
def run(command: str, arguments: list[str] = []) -> None:
    """Run a command installed in virtual env.

    Args:
        command: Command to run
        arguments: Arguments to pass to command
    """
    run_command(command, arguments)


@app.command()
def update() -> None:
    """Update all dependencies and install."""
    upgrade_dependencies()
