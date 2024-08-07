"""Module to handle dependencies."""

from __future__ import annotations

from pathlib import Path

from rich import print

from pspm.entities.installer import BaseInstaller, UVInstaller
from pspm.entities.pyproject import Pyproject
from pspm.entities.toml import Toml
from pspm.errors.dependencies import InstallError


def _get_pyproject() -> Pyproject:
    path = Path(Path.cwd()) / "pyproject.toml"
    parser = Toml(str(path))
    return Pyproject(parser)


def _get_installer() -> BaseInstaller:
    return UVInstaller()


def add_dependency(package: str, group: str | None = None) -> None:
    """Add dependency to pyproject.

    :param package: Package to install
    :param group: Group to insert package
    """
    installer = _get_installer()
    try:
        installer.install(package)
    except InstallError:
        print(f":boom: [red]Failed to install {package}[/red]")
        return

    pyproject = _get_pyproject()
    if not group:
        pyproject.add_dependency(package)
    else:
        pyproject.add_group_dependency(package, group)
