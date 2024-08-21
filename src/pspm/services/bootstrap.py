"""Module to handle bootstrap of project."""

from __future__ import annotations

from typing import TYPE_CHECKING

from copier.errors import UserMessageError

if TYPE_CHECKING:
    from pathlib import Path


import copier
from jinja2 import Environment, PackageLoader
from rich import print as rprint

from pspm.utils.commands import get_git_user


def _create_package_structure(base_path: Path, safe_name: str) -> None:
    package_init = base_path / "src" / safe_name / "__init__.py"
    package_init.parent.mkdir(parents=True, exist_ok=True)
    package_init.write_text("")


def bootstrap_project(
    path: Path, name: str | None, description: str | None, *, installable: bool
) -> None:
    """Create initial project structure.

    Args:
        path: Path to project
        name: Project name
        description: Project description
        installable: Whether the project is installable
    """
    name = name or path.absolute().name
    description = description or "Describe your project here"

    path.mkdir(exist_ok=True)
    env = Environment(loader=PackageLoader("pspm"), autoescape=True)
    template_names = env.list_templates()
    author = get_git_user()
    safe_package_name = name.lower().replace("-", "_")
    for template_name in template_names:
        template = env.get_template(template_name)
        result = template.render(
            name=name,
            safe_name=safe_package_name,
            description=description,
            installable=installable,
            author=author,
        )
        file_name = template_name.replace(".j2", "")
        file_path = path / file_name
        file_path.write_text(result, encoding="utf-8")
    _create_package_structure(path, safe_package_name)
    rprint(
        f"Initialized project [blue]{name}[/blue] "
        + (f"in [blue]{path.name}[/blue]" if path.name else "")
    )


def bootstrap_project_with_copier(
    path: Path,
    template_src: str | None,
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
    template_src = template_src or "gh:Jahn16/pspm-templates"

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
    )


def update_project(path: Path) -> None:
    """Update to latest project template.

    Args:
        path: Path to project
    """
    try:
        copier.run_update(path, overwrite=True, defaults=True)
    except UserMessageError as e:
        rprint(f"[red]{e}.[/red]")
    except TypeError as e:
        rprint(f"[red]{e}. Perhaps missing an .copier-answer.yml file?[/red]")
