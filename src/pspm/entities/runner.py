"""Module to define command runner class."""

import subprocess

from pspm.entities.virtual_env import VirtualEnv
from pspm.errors.command import CommandNotFoundError, CommandRunError


class Runner:
    """Class to run commands."""

    def __init__(self, virtual_env: VirtualEnv) -> None:
        """Initialize Runner.

        Args:
            virtual_env: Virtual env
        """
        self._virtual_env = virtual_env

    def run(self, command: str, arguments: list[str]) -> None:
        """Run a command.

        Args:
            command: Command to execute
            arguments: Arguments to be passed to command.

        Raises:
            CommandRunError: If command fails
        """
        try:
            self._virtual_env.get_path_to_command_bin(command)
        except CommandNotFoundError as e:
            raise CommandRunError(command, str(e)) from e

        retcode = subprocess.call([command, *arguments], shell=False)
        if retcode != 0:
            raise CommandRunError(command)
