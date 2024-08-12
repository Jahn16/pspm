"""Module to define virtualenv classes."""

import abc
import subprocess
from pathlib import Path

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
    def activate(self) -> None:
        """Activate virtualenv."""
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, command: str) -> None:
        """Run command inside virtualenv.

        Args:
            command: Command to run
        """
        raise NotImplementedError


class VirtualEnv(BaseVirtualEnv):
    """Interacts with virtualenv."""

    def __init__(self) -> None:
        """Initialize BaseVirtualEnv."""
        self._path = ".venv"

    def already_created(self) -> bool:
        """Check if env is already created.

        Returns:
            Whether the env is created
        """
        p = Path(self._path)
        return p.exists()

    def create(self) -> None:
        """Create virtualenv."""
        uv_path = get_uv_path()
        subprocess.run([uv_path, "venv", self._path], check=False)

    def activate(self) -> None:
        """Activate virtualenv."""
        raise NotImplementedError

    def run(self, command: str) -> None:
        """Run command inside virtualenv.

        Args:
            command: Command to run
        """
        raise NotImplementedError
