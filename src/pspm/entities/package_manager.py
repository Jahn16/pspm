"""Module to define PackageManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pspm.entities.installer import BaseInstaller
    from pspm.entities.pyproject import BasePyproject
    from pspm.entities.resolver import BaseResolver


class PackageManager:
    """Manage project dependencies."""

    def __init__(
        self,
        pyproject: BasePyproject,
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

    def add_dependency(self, package: str) -> None:
        """Add dependency to pyproject.

        Args:
            package: Package to install
            group: Group to insert package
        """
        self._pyproject.add_dependency(package)
        main_file = "requirements.lock"
        group_file_format = "requirements-{}.lock"
        all_groups = self._pyproject.get_extra_groups()
        group_files = [group_file_format.format(g) for g in all_groups]
        self._resolver.compile(main_file)
        for f, g in zip(group_files, all_groups):
            self._resolver.compile(f, g)
        self._installer.sync([main_file, *group_files])
        self._installer.install(".")

    def add_dependency_with_group(self, package: str, group: str) -> None:
        """Add dependency to pyproject with group.

        Args:
            package: Package to install
            group: Group to insert package
        """
        group_file = f"requirements-{group}.lock"
        self._pyproject.add_group_dependency(package, group)
        self._resolver.compile(group_file, group)
        self._installer.sync([group_file])
        self._installer.install(".")
