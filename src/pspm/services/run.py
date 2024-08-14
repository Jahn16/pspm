"""Module to interact with command runner."""

from dotenv import load_dotenv
from rich import print as rprint

from pspm.entities.runner import Runner
from pspm.entities.virtual_env import VirtualEnv
from pspm.errors.command import CommandRunError


def _get_runner() -> Runner:
    virtual_env = VirtualEnv()
    return Runner(virtual_env)


def run_command(command: str, arguments: list[str]) -> None:
    """Load dotenv and run a command.

    Args:
        command: Command to run
        arguments: Arguments to pass to command
    """
    load_dotenv()
    runner = _get_runner()
    try:
        runner.run(command, arguments)
    except CommandRunError as e:
        rprint(f"[red]{e}[/red]")
