"""Module to handle dependencies."""

from __future__ import annotations

from pathlib import Path

from pspm.entities.installer import BaseInstaller, UVInstaller
from pspm.entities.package_manager import PackageManager
from pspm.entities.pyproject import Pyproject
from pspm.entities.resolver import BaseResolver, UVResolver
from pspm.entities.toml import Toml


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


def _get_package_manager() -> PackageManager:
    return PackageManager(_get_pyproject(), _get_installer(), _get_resolver())


def install_dependencies() -> None:
    """Install all dependencies and the package itself."""
    package_manager = _get_package_manager()
    package_manager.install()


def add_dependency(package: str, group: str | None = None) -> None:
    """Add dependency to pyproject.

    Args:
        package: Package to install
        group: Group to insert package
    """
    package_manager = _get_package_manager()
    package_manager.add_dependency(package, group)
