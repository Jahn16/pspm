"""Module to define command runner class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pspm.errors.command import CommandNotFoundError, CommandRunError

if TYPE_CHECKING:
    from pspm.entities.command_runner import BaseCommandRunner
    from pspm.entities.virtual_env import VirtualEnv


class VenvRunner:
    """Class to run commands inside virtualenv."""

    def __init__(
        self, virtual_env: VirtualEnv, command_runner: BaseCommandRunner
    ) -> None:
        """Initialize Runner.

        Args:
            virtual_env: Virtual env
            command_runner: Command Runner
        """
        self._virtual_env = virtual_env
        self._command_runner = command_runner

    def run(self, command: str, arguments: list[str] | None = None) -> None:
        """Run a command inside virtualenv.

        Args:
            command: Command to execute
            arguments: Arguments to be passed to command.

        Raises:
            CommandRunError: If command fails
        """
        try:
            command_path = self._virtual_env.get_path_to_command_bin(command)
        except CommandNotFoundError as e:
            raise CommandRunError(command, str(e)) from e

        self._command_runner.run(command_path, arguments)
