"""Module to handle dependencies."""

from __future__ import annotations

from pathlib import Path

from rich import print as rprint

from pspm.entities.installer import BaseInstaller, UVInstaller
from pspm.entities.pyproject import Pyproject
from pspm.entities.resolver import BaseResolver, UVResolver
from pspm.entities.toml import Toml
from pspm.errors.dependencies import InstallError


def _get_pyproject_path() -> str:
    path = Path(Path.cwd()) / "pyproject.toml"
    return str(path)


def _get_pyproject() -> Pyproject:
    path = _get_pyproject_path()
    parser = Toml(str(path))
    return Pyproject(parser)


def _get_resolver() -> BaseResolver:
    path = _get_pyproject_path()
    return UVResolver(path)


def _get_installer() -> BaseInstaller:
    return UVInstaller()


def add_dependency(package: str, group: str | None = None) -> None:
    """Add dependency to pyproject.

    Args:
        package: Package to install
        group: Group to insert package
    """
    installer = _get_installer()
    try:
        installer.install(package)
    except InstallError:
        rprint(f":boom: [red]Failed to install {package}[/red]")
        return

    pyproject = _get_pyproject()
    if not group:
        pyproject.add_dependency(package)
    else:
        pyproject.add_group_dependency(package, group)
    resolver = _get_resolver()
    output_file = f"requirements{'-' + group if group else ''}.lock"
    resolver.compile(output_file, group)
