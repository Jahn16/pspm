"""Module to define PackageManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pspm.errors.dependencies import InstallError

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

        group_file = "requirements-{}.lock"
        if group:
            self._pyproject.add_group_dependency(package, group)
            self._resolver.compile(group_file.format(group), group)
            return

        self._pyproject.add_dependency(package)
        main_file = "requirements.lock"
        file_and_groups = [
            (group_file.format(g), g)
            for g in self._pyproject.get_extra_groups()
        ]
        self._resolver.compile(main_file)
        for f, g in file_and_groups:
            self._resolver.compile(f, g)
