"""Module to handle bootstrap of project."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


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
