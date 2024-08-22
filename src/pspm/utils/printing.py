"""Utils functions to use rich print."""

from pathlib import Path

from rich import print as rprint
from rich.markup import escape
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree


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


def print_file_tree(directory: Path, panel_title: str = "") -> None:
    """Print file tree.

    Args:
        directory: Directory to print tree
        panel_title: Panel title
    """
    tree = Tree(
        f":open_file_folder: {directory}",
        guide_style="bold bright_blue",
    )
    _walk_directory(Path(directory), tree)
    rprint(
        Panel(
            tree,
            title=panel_title,
            title_align="left",
        )
    )


def _walk_directory(directory: Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    paths = sorted(
        Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.is_dir():
            branch = tree.add(
                f":open_file_folder: {escape(path.name)}",
            )
            _walk_directory(path, branch)
        else:
            text_filename = Text(path.name)
            text_filename.stylize(str(path))
            tree.add(text_filename)
