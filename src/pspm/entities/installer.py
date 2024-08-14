"""Module with classes to deal with packages."""

from __future__ import annotations

import abc
import subprocess

from pspm.errors.dependencies import InstallError, SyncError
from pspm.utils.bin_path import get_uv_path


class BaseInstaller(abc.ABC):
    """Package installer."""

    @abc.abstractmethod
    def install(self, package: str, *, editable: bool = False) -> None:
        """Install package.

        Args:
            package: Package to install
            editable: Whether to install in editable mode
        """
        raise NotImplementedError

    @abc.abstractmethod
    def uninstall(self, package: str) -> None:
        """Uninstall package.

        Args:
            package: Package to uninstall
        """
        raise NotImplementedError

    @abc.abstractmethod
    def sync(self, requirements_files: list[str]) -> None:
        """Sync an environment with requirements files.

        Install all dependencies listed in requirements files
        and removes the ones that are not listed.

        Args:
            requirements_files: Path to files containing requirements
        """
        raise NotImplementedError


class UVInstaller(BaseInstaller):
    """Install packages with UV."""

    def __init__(self) -> None:
        """Initialize UV Installer."""
        self._uv_path = get_uv_path()

    def install(self, package: str, *, editable: bool = False) -> None:
        """Install a package.

        Args:
            package: Package to install
            editable: Whether to install in editable mode

        Raises:
            InstallError: If can't install package.
        """
        retcode = subprocess.call([
            self._uv_path,
            "pip",
            "install",
            *(["--editable"] if editable else []),
            package,
        ])
        if retcode != 0:
            raise InstallError(package)

    def uninstall(self, package: str) -> None:
        """Uninstall package.

        Args:
            package: Package to uninstall
        """
        raise NotImplementedError

    def sync(self, requirements_files: list[str]) -> None:
        """Sync an environment with requirements files.

        Install all dependencies listed in requirements files
        and removes the ones that are not listed.

        Args:
            requirements_files: Path to files containing requirements

        Raises:
            SyncError: If cant sync dependencies
        """
        retcode = subprocess.call([
            self._uv_path,
            "pip",
            "sync",
            *requirements_files,
        ])
        if retcode != 0:
            raise SyncError
