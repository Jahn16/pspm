"""Module to define virtualenv classes."""

import abc
import subprocess
from pathlib import Path

from pspm.errors.command import CommandNotFoundError
from pspm.utils.bin_path import get_uv_path


class BaseVirtualEnv(abc.ABC):
    """Interacts with virtualenv."""

    @abc.abstractmethod
    def already_created(self) -> bool:
        """Check if env is already created."""
        raise NotImplementedError

    @abc.abstractmethod
    def create(self) -> None:
        """Create virtualenv."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_path_to_command_bin(self, command: str) -> str:
        """Retrieve path to command bin.

        Args:
            command: Command to find bin
        """
        raise NotImplementedError


class VirtualEnv(BaseVirtualEnv):
    """Interacts with virtualenv."""

    def __init__(self) -> None:
        """Initialize BaseVirtualEnv."""
        self._path = Path(".venv")

    def already_created(self) -> bool:
        """Check if env is already created.

        Returns:
            Whether the env is created
        """
        return self._path.exists()

    def create(self) -> None:
        """Create virtualenv."""
        uv_path = get_uv_path()
        subprocess.run([uv_path, "venv", self._path.absolute()], check=False)

    def get_path_to_command_bin(self, command: str) -> str:
        """Retrieve path to command bin.

        Args:
            command: Command to find bin path

        Raises:
            CommandNotFoundError: If command bin was not found

        Returns:
            Absolute path to command bin
        """
        command_path = self._path / "bin" / command
        if not command_path.exists():
            error_message = (
                f"Command {command} was not found "
                f"in {command_path.parent.relative_to(self._path.parent)}"
            )
            raise CommandNotFoundError(command, error_message)
        return str(command_path.absolute())
