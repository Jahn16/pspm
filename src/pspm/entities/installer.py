"""Module with classes to deal with packages."""

import abc
import subprocess
from shutil import which

import uv

from pspm.errors.dependencies import InstallError


class BaseInstaller(abc.ABC):
    """Base class for handling packages."""

    @abc.abstractmethod
    def install(self, package: str) -> None:
        """Install package.

        :param package: Package to install
        """
        raise NotImplementedError

    @abc.abstractmethod
    def uninstall(self, package: str) -> None:
        """Uninstall package.

        :param package: Package to uninstall
        """
        raise NotImplementedError


class UVInstaller(BaseInstaller):
    """Class for installing packages with UV."""

    def __init__(self) -> None:
        """Initialize UV Installer."""
        self._uv_path = which("uv") or uv.find_uv_bin()

    def install(self, package: str) -> None:
        """Install package.

        :param package: Package to install
        """
        retcode = subprocess.call([self._uv_path, "pip", "install", package])  # noqa: S603
        if retcode != 0:
            raise InstallError(package)

    def uninstall(self, package: str) -> None:
        """Uninstall package.

        :param package: Package to uninstall
        """
        raise NotImplementedError
