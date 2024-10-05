"""Module to find paths to binaries."""

import shutil

from typer import Exit

from pspm.utils.printing import print_error


def get_uv_path() -> str:
    """Finds uv binary path.

    Returns:
        Path to uv binary

    Raises:
        Exit: If UV path was not found
    """
    path = shutil.which("uv")
    if not path:
        print_error(
            r"UV command not found, can be installed by running "
            r"`[bold]pip install pspm\[uv][/]`"
        )
        raise Exit
    return path
