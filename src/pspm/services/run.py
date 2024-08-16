"""Module to interact with command runner."""

from os import environ
from pathlib import Path

from rich import print as rprint

from pspm.entities.runner import Runner
from pspm.entities.virtual_env import VirtualEnv
from pspm.errors.command import CommandRunError


def _get_runner() -> Runner:
    virtual_env = VirtualEnv()
    return Runner(virtual_env)


def load_dotenv() -> None:
    """Load env vars from dotenv file."""
    path = Path(".env")
    if not path.exists():
        return
    text = path.read_text()
    lines = text.rsplit()
    for line in lines:
        key, value = line.split("=")
        environ[key] = value


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
