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


def _version_callback(value: bool) -> None:
    if value:
        version = importlib.metadata.version("pspm")
        rprint(version)


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=_version_callback, is_eager=True),
    ] = None,
) -> None:
    """Python simple package manager."""


@app.command()
def sync() -> None:
    """Sync environment with all dependencies and the package itself."""
    rprint(":hourglass: Installing [blue]project[/blue] and dependencies")
    sync_dependencies()
    rprint("\n:sparkles: Installed [blue]project[/blue] and dependencies")


@app.command()
def add(
    package: Annotated[str, typer.Argument(help="Package to add")],
    group: Annotated[
        Optional[str],
        typer.Option(
            "--group",
            "-g",
            help="Target dependency group to add into",
        ),
    ] = None,
) -> None:
    """Add package to pyproject, install it and lock version."""
    manage_dependency("add", package, group)
    rprint(f"\n:sparkles: Added package [blue]{package}[/blue]")


@app.command()
def remove(
    package: Annotated[str, typer.Argument(help="Package to remove")],
    group: Annotated[
        Optional[str],
        typer.Option(
            "--group",
            "-g",
            help="Target dependency group to remove from",
        ),
    ] = None,
) -> None:
    """Remove package from pyproject, uninstall it and lock version."""
    manage_dependency("remove", package, group or None)
    rprint(f"\n:boom: Removed package [blue]{package}[/blue]")


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
    """Run a command installed in virtual env."""
    run_command(command, arguments or [])


@app.command()
def lock(
    update: Annotated[
        bool,
        typer.Option(help="Whether to update dependencies to latest version"),
    ] = False,
) -> None:
    """Lock the dependencies without installing."""
    lock_dependencies(update=update)
    rprint(":lock: Locked dependencies")
    rprint(
        "   :arrow_right_hook: Run `[blue]spm sync[/blue]` to install them",
    )


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
    new_version: Annotated[
        Optional[str], typer.Argument(help="Version to change to")
    ] = None,
    bump: Annotated[
        Optional[BumpRules],
        typer.Option("-b", "--bump", help="Bump rule to apply change version"),
    ] = None,
) -> None:
    """Checks or update project version."""
    if new_version:
        version = change_version(new_version)
    elif bump:
        version = change_version(bump_rule=bump.value)
    else:
        version = get_version()
    rprint(version)


class ProjectTypes(str, Enum):  # noqa: D101
    lib = "lib"
    app = "app"
    script = "script"


@app.command()
def init(
    path: Annotated[
        Path,
        typer.Argument(file_okay=False, help="Where to place the project"),
    ] = Path(),
    template: Annotated[
        str,
        typer.Option(
            "--template",
            "-T",
            help="Local path or Git URL to a copier template",
        ),
    ] = "gh:Jahn16/pspm-template",
    name: Annotated[Optional[str], typer.Option(help="Project name")] = None,
    description: Annotated[
        Optional[str], typer.Option(help="Project description")
    ] = None,
    project_type: Annotated[
        ProjectTypes, typer.Option("--type", "-t", help="Project type")
    ] = ProjectTypes.lib,
) -> None:
    """Create initial project structure."""
    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Creating project...", total=None)
        bootstrap_project(path, template, name, description, project_type)
    panel_title = (
        f"Initialized project [blue]{name or path.absolute().name}[/blue]"
        + (f" in [blue]{path.name}[/blue]" if path.name else "")
    )
    print_file_tree(path, panel_title=panel_title)
