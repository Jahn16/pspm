"""Module to define PackageManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pspm.errors.dependencies import InstallError

if TYPE_CHECKING:
    from pspm.entities.installer import BaseInstaller
    from pspm.entities.pyproject import Pyproject
    from pspm.entities.resolver import BaseResolver


class PackageManager:
    """Manage project dependencies."""

    def __init__(
        self,
        pyproject: Pyproject,
        installer: BaseInstaller,
        resolver: BaseResolver,
    ) -> None:
        """Initialize PackageManager.

        Args:
            pyproject: BasePyproject to manipulate pyproject file
            installer: BaseInstaller to install depencies
            resolver: BaseResolver to resolve dependencies
        """
        self._pyproject = pyproject
        self._installer = installer
        self._resolver = resolver

    def add_dependency(self, package: str, group: str | None = None) -> None:
        """Add dependency to pyproject.

        Args:
            package: Package to install
            group: Group to insert package
        """
        try:
            self._installer.install(package)
        except InstallError:
            return

        if not group:
            self._pyproject.add_dependency(package)
        else:
            self._pyproject.add_group_dependency(package, group)
        output_file = f"requirements{'-' + group if group else ''}.lock"
        self._resolver.compile(output_file, group)
