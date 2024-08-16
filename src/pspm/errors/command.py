"""Module for defining errors related to command execution."""


class CommandError(Exception):
    """Base error for command."""

    def __init__(self, command: str, message: str = "") -> None:
        """Initialize CommandError.

        Args:
            command: Command that failed to be executed.
            message: Error message
        """
        self.command = command
        self.message = message or f"Command {command} failed"
        super().__init__(self.message)


class CommandNotFoundError(CommandError):
    """Comand bin was not found."""


class CommandRunError(CommandError):
    """Command failed to run."""
