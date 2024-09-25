"""Module to find paths to binaries."""

import shutil

import uv


def get_uv_path() -> str:
    """Finds uv binary path.

    Returns:
        Path to uv binary
    """
    return shutil.which("uv") or uv.find_uv_bin()
