"""Utils functions to use rich print."""

from rich import print as rprint
from rich.panel import Panel


def print_error(error_message: str) -> None:
    """Print error message.

    Args:
        error_message: Error message to print
    """
    rprint(
        Panel(
            error_message,
            title="Error",
            title_align="left",
            border_style="red",
        )
    )
