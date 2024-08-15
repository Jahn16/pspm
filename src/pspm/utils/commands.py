"""Module to define utils functions that execute commands."""

from __future__ import annotations

import subprocess
from shutil import which


def get_git_user() -> dict[str, str] | None:
    """Retrieve git user.

    Returns:
        Git user with name and email
    """
    user: dict[str, str] = {}
    git_path = which("git")
    if not git_path:
        return None
    for field in ["name", "email"]:
        try:
            output = subprocess.check_output([
                git_path,
                "config",
                f"user.{field}",
            ])
        except subprocess.CalledProcessError:
            return None
        user[field] = output.strip().decode()
    return user
