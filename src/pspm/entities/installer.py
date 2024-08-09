"""Module with classes to deal with packages."""

import abc
import subprocess
from shutil import which

import uv

from pspm.errors.dependencies import InstallError


class BaseInstaller(abc.ABC):
    """Package installer."""

    @abc.abstractmethod
    def install(self, package: str) -> None:
        """Install package.

        Args:
            package: Package to install

        """
        raise NotImplementedError

    @abc.abstractmethod
    def uninstall(self, package: str) -> None:
        """Uninstall package.

        Args:
            package: Package to uninstall

        """
        raise NotImplementedError


class UVInstaller(BaseInstaller):
    """Install packages with UV."""

    def __init__(self) -> None:
        """Initialize UV Installer."""
        self._uv_path = which("uv") or uv.find_uv_bin()

    def install(self, package: str) -> None:
        """Install package.

        Args:
            package: Package to install

        Raises:
            InstallError: If can't install package
        """
        retcode = subprocess.call([self._uv_path, "pip", "install", package])  # noqa: S603
        if retcode != 0:
            raise InstallError(package)

    def uninstall(self, package: str) -> None:
        """Uninstall package.

        Args:
            package: Package to uninstall
        """
        raise NotImplementedError
