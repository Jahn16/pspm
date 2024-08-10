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
        self._main_requirements_file = "requirements.lock"
        self._group_requirements_file = "requirements-{}.lock"

    def _get_group_requirements_files(self) -> list[str]:
        groups = self._pyproject.get_extra_groups()
        return [self._group_requirements_file.format(g) for g in groups]

    def install(self) -> None:
        """Install all dependencies and the package itself."""
        self._installer.sync([
            self._main_requirements_file,
            *self._get_group_requirements_files(),
        ])
        self._installer.install(".", editable=True)

    def add_dependency(self, package: str, group: str | None = None) -> None:
        """Add dependency to pyproject.

        Args:
            package: Package to install
            group: Group to insert package
        """
        (
            self._pyproject.add_dependency(package)
            if not group
            else self._pyproject.add_group_dependency(package, group)
        )
        groups = self._pyproject.get_extra_groups()
        self._resolver.compile(self._main_requirements_file)
        for f, g in zip(self._get_group_requirements_files(), groups):
            self._resolver.compile(f, g)
        self.install()
