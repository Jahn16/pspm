"""Module to define cli commands."""

# ruff: noqa: FBT001 FBT002 B006 UP007
from __future__ import annotations

import importlib.metadata
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print as rprint

from pspm.services.bootstrap import bootstrap_project
from pspm.services.dependencies import (
    change_version,
    get_version,
    install_dependencies,
    lock_dependencies,
    manage_dependency,
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
    path: Annotated[Path, typer.Argument(file_okay=False)] = Path(),
    name: Optional[str] = None,
    description: Optional[str] = None,
    installable: Annotated[
        bool, typer.Option("--installable/--not-installable")
    ] = True,
) -> None:
    """Create initial project structure.

    Args:
        path: Where to place the project
        name: Project name
        description: Project description
        installable: Whether the project is instalabble
    """
    bootstrap_project(path, name, description, installable=installable)


@app.command()
def install() -> None:
    """Install all dependencies and the package itself."""
    rprint("Installing project")
    install_dependencies()


@app.command()
def add(
    package: str,
    group: Annotated[Optional[str], typer.Option("--group", "-g")] = None,
) -> None:
    """Add package to pyproject, install it and lock version."""
    rprint(f"Adding package {package}")
    manage_dependency("add", package, group)


@app.command()
def remove(
    package: str,
    group: Annotated[Optional[str], typer.Option("--group", "-g")] = None,
) -> None:
    """Remove package from pyproject, uninstall it and lock version."""
    rprint(f"Removing package {package}")
    manage_dependency("remove", package, group or None)


@app.command()
def run(
    command: str,
    arguments: Annotated[Optional[list[str]], typer.Argument()] = None,
) -> None:
    """Run a command installed in virtual env.

    Args:
        command: Command to run
        arguments: Arguments to pass to command
    """
    run_command(command, arguments or [])


@app.command()
def lock(update: bool = False) -> None:
    """Lock the dependencies without installing."""
    lock_dependencies(update=update)


class BumpRules(str, Enum):  # noqa: D101
    major = "major"
    minor = "minor"
    patch = "patch"


@app.command()
def version(
    new_version: Annotated[Optional[str], typer.Argument()] = None,
    bump: Annotated[
        Optional[BumpRules],
        typer.Option("-b", "--bump"),
    ] = None,
) -> None:
    """Checks or update project version.

    Args:
        new_version: Version to change to
        bump: Bump rule to apply change version
    """
    if new_version:
        version = change_version(new_version)
    elif bump:
        version = change_version(bump_rule=bump.value)
    else:
        version = get_version()
    rprint(version)
