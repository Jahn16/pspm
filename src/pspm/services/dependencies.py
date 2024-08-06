"""Module to handle dependencies."""

from __future__ import annotations

from pathlib import Path

from pspm.entities.pyproject import Pyproject
from pspm.entities.toml import Toml


def _get_pyproject() -> Pyproject:
    path = Path(Path.cwd()) / "pyproject.toml"
    parser = Toml(str(path))
    return Pyproject(parser)


def add_dependency(package: str, group: str | None = None) -> None:
    """Add dependency to pyproject.

    :param package: Package to install
    :param group: Group to insert package
    """
    pyproject = _get_pyproject()
    if not group:
        pyproject.add_dependency(package)
    else:
        pyproject.add_group_dependency(package, group)
