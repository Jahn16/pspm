"""Module to handle dependencies."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pspm.entities.installer import BaseInstaller, UVInstaller
from pspm.entities.package_manager import PackageManager
from pspm.entities.pyproject import Pyproject
from pspm.entities.resolver import BaseResolver, UVResolver
from pspm.entities.toml import Toml
from pspm.entities.virtual_env import VirtualEnv


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
    virtual_env = VirtualEnv()
    return PackageManager(
        _get_pyproject(), _get_installer(), _get_resolver(), virtual_env
    )


def install_dependencies() -> None:
    """Install all dependencies and the package itself."""
    package_manager = _get_package_manager()
    package_manager.install()


def manage_dependency(
    action: Literal["add", "remove"], package: str, group: str | None = None
) -> None:
    """Add dependency to pyproject.

    Args:
        action: Action to take can be either add or remove
        package: Package to install
        group: Group to insert package
    """
    package_manager = _get_package_manager()
    package_manager.manage_dependency(action, package, group)


def lock_dependencies(*, update: bool = False) -> None:
    """Lock dependencies."""
    package_manager = _get_package_manager()
    package_manager.compile_requirements(upgrade=update)
    package_manager.install()


def get_version() -> str:
    """Retrive pyproject version.

    Returns:
        Project version.
    """
    pyproject = _get_pyproject()
    return pyproject.version


def change_version(
    new_version: str | None = None,
    bump_rule: Literal["major", "minor", "patch"] | None = None,
) -> str:
    """Change project version.

    Args:
        new_version: Version to change to
        bump_rule: Rule to change version

    Raises:
        ValueError: If neither argument were provided

    Returns:
        Updated version
    """
    pyproject = _get_pyproject()
    if new_version:
        return pyproject.change_version(new_version)
    if bump_rule:
        return pyproject.bump_version(bump_rule)
    error_message = "Missing action to change version"
    raise ValueError(error_message)
