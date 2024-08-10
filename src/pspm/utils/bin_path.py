"""Module to find paths to binaries."""

import uv


def get_uv_path() -> str:
    """Finds uv binary path.

    Returns:
        Path to uv binary
    """
    return uv.find_uv_bin()
