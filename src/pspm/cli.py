"""Module to define cli commands."""

# ruff: noqa: FBT001 FBT002 B006 UP007
from __future__ import annotations

import importlib.metadata
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from pspm.services.bootstrap import (
    bootstrap_project,
    update_project,
)
from pspm.services.dependencies import (
    change_version,
    get_version,
    lock_dependencies,
    manage_dependency,
    sync_dependencies,
)
from pspm.services.run import run_command
from pspm.utils.printing import print_file_tree

app = typer.Typer(no_args_is_help=True, invoke_without_command=True)
project_app = typer.Typer()
app.add_typer(project_app, name="project", help="Manage project templates")


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
def sync() -> None:
    """Sync environment with all dependencies and the package itself."""
    rprint("Installing project")
    sync_dependencies()
    rprint(
        "\n:sparkles: Installed [blue]current package[/blue] and dependencies"
    )


@app.command()
def add(
    package: str,
    group: Annotated[Optional[str], typer.Option("--group", "-g")] = None,
) -> None:
    """Add package to pyproject, install it and lock version."""
    rprint(f"Adding package {package}")
    manage_dependency("add", package, group)
    rprint(f"\n:sparkles: Added package [blue]{package}[/blue]")


@app.command()
def remove(
    package: str,
    group: Annotated[Optional[str], typer.Option("--group", "-g")] = None,
) -> None:
    """Remove package from pyproject, uninstall it and lock version."""
    rprint(f"Removing package {package}")
    manage_dependency("remove", package, group or None)
    rprint(f"\n:sparkles: Removed package [blue]{package}[/blue]")


@app.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_interspersed_args": False,
    }
)
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
    rprint(":lock: Locked dependencies")


@app.command()
def upgrade() -> None:
    """Upgrade dependencies to latest version."""
    lock_dependencies(update=True)
    sync_dependencies()
    rprint("\n:sparkles: Upgraded dependencies")


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


@app.command("init")
@project_app.command("init")
def project_init(
    path: Annotated[Path, typer.Argument(file_okay=False)] = Path(),
    template: Annotated[
        Optional[str], typer.Option("--template", "-t")
    ] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_installable: Annotated[
        bool, typer.Option("--installable/--not-installable")
    ] = True,
) -> None:
    """Create initial project structure.

    Args:
        path: Where to place the project
        template: Reference to a clicker template, can be a local path or URL
        name: Project name
        description: Project description
        is_installable: Whether the project is instalabble
    """
    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Creating project...", total=None)
        bootstrap_project(
            path, template, name, description, is_installable=is_installable
        )
    panel_title = (
        f"Initialized project [blue]{name or path.absolute().name}[/blue]"
        + (f" in [blue]{path.name}[/blue]" if path.name else "")
    )
    print_file_tree(path, panel_title=panel_title)


@project_app.command("update")
def project_update(
    path: Annotated[Path, typer.Argument(file_okay=False)] = Path(),
) -> None:
    """Update project template.

    Args:
        path: Path to project
    """
    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Updating project...", total=None)
        update_project(path)
