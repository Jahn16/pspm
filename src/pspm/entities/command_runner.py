"""Module to define CommandRunner class."""

from __future__ import annotations

import abc
import subprocess


class BaseCommandRunner(abc.ABC):
    """Runs commands."""

    @staticmethod
    @abc.abstractmethod
    def run(command: str, args: list[str] | None = None) -> int:
        """Run a command.

        Args:
            command: Command to be executed
            args: Arguments to be passed to command
        """
        raise NotImplementedError


class CommandRunner(BaseCommandRunner):
    """Runs commands."""

    @staticmethod
    def run(command: str, args: list[str] | None = None) -> int:
        """Run a command.

        Args:
            command: Command to be executed
            args: Arguments to be pased to command

        Returns:
            Return code from command
        """
        return subprocess.call([command, *(args or [])], shell=False)
