"""Module to handle bootstrap of project."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


import copier

from pspm.utils.commands import get_git_user


def bootstrap_project(
    path: Path,
    template_src: str,
    name: str | None,
    description: str | None,
    *,
    is_installable: bool,
) -> None:
    """Create initial project structure.

    Args:
        path: Path to project
        template_src: Template source path
        name: Project name
        description: Project description
        is_installable: Whether the project is installable
    """
    name = name or path.absolute().name
    description = description or "Describe your project here"

    author = get_git_user() or {}
    copier.run_copy(
        template_src,
        path,
        data={
            "project_name": name,
            "project_description": description,
            "is_installable": is_installable,
            "author_name": author.get("name", ""),
            "author_email": author.get("email", ""),
        },
        defaults=True,
        quiet=True,
        overwrite=False,
    )
