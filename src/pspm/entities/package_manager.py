"""Module to define PackageManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from rich.progress import Progress, SpinnerColumn, TextColumn

from pspm.errors.dependencies import AddError, ResolveError

if TYPE_CHECKING:
    from pspm.entities.installer import BaseInstaller
    from pspm.entities.pyproject import BasePyproject
    from pspm.entities.resolver import BaseResolver
    from pspm.entities.virtual_env import BaseVirtualEnv


class PackageManager:
    """Manage project dependencies."""

    def __init__(
        self,
        pyproject: BasePyproject,
        installer: BaseInstaller,
        resolver: BaseResolver,
        virtual_env: BaseVirtualEnv,
    ) -> None:
        """Initialize PackageManager.

        Args:
            pyproject: BasePyproject to manipulate pyproject file
            installer: BaseInstaller to install depencies
            resolver: BaseResolver to resolve dependencies
            virtual_env: BaseVirtualEnv to manage venv
        """
        self._pyproject = pyproject
        self._installer = installer
        self._resolver = resolver
        self._virtual_env = virtual_env

        self._main_requirements_file = "requirements.lock"
        self._group_requirements_file = "requirements-{}.lock"

    def _get_group_requirements_files(self) -> list[str]:
        groups = self._pyproject.get_extra_groups()
        return [self._group_requirements_file.format(g) for g in groups]

    def sync(self) -> None:
        """Sync environment with all dependencies and the package itself."""
        if not self._virtual_env.already_created():
            self._virtual_env.create()

        self._installer.sync([
            self._main_requirements_file,
            *self._get_group_requirements_files(),
        ])
        if self._pyproject.is_installable():
            self._installer.install(".", editable=True)

    def manage_dependency(
        self,
        action: Literal["add", "remove"],
        package: str,
        group: str | None = None,
    ) -> None:
        """Add dependency to pyproject.

        Args:
            action: Action to take can be either add or remove
            package: Package to install
            group: Group to insert package

        Raises:
            AddError: If can't add dependency
        """
        self._pyproject.manage_dependency(action, package, group)
        try:
            self.compile_requirements()
        except ResolveError as e:
            if action == "add":
                self._pyproject.manage_dependency("remove", package, group)
                raise AddError(package) from e
            return
        self.sync()

    def compile_requirements(self, *, upgrade: bool = False) -> None:
        """Compile all requirements files.

        Args:
            upgrade: Whether to upgrade package versions
        """
        groups = self._pyproject.get_extra_groups()
        with Progress(
            SpinnerColumn(style="blue"),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Resolving dependencies...")
            self._resolver.compile(
                self._main_requirements_file, upgrade=upgrade
            )
            for file, group in zip(
                self._get_group_requirements_files(), groups
            ):
                self._resolver.compile(
                    file,
                    group,
                    constraint_file=self._main_requirements_file,
                    upgrade=upgrade,
                )
