"""Module for defining errors related to command execution."""


class CommandError(Exception):
    """Base error for command."""

    def __init__(self, command: str) -> None:
        """Initialize CommandError.

        Args:
            command: Command that failed to be executed.
        """
        self.command = command
        self.message = f"Command {command} failed"
        super().__init__(self.message)


class CommandNotFoundError(CommandError):
    """Comand bin was not found."""

    def __init__(self, command: str) -> None:
        """Initialize CommandNotFound.

        Args:
            command: Command that was not found
        """
        self.message = f"Command {command} was not found"
        super().__init__(self.message)


class CommandRunError(CommandError):
    """Command failed to run."""
