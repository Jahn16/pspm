"""Module to find paths to binaries."""

from shutil import which


def get_uv_path() -> str:
    """Finds uv binary path.

    Returns:
        Path to uv binary
    """
    return which("uv") or "uv"
