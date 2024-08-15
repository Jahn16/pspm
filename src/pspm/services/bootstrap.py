"""Module to handle bootstrap of project."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, PackageLoader
from rich import print as rprint


def _create_package_structure(name: str) -> None:
    safe_name = name.lower().replace("-", "_")
    package_init = Path(f"src/{safe_name}/__init__.py")
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
    for template_name in template_names:
        template = env.get_template(template_name)
        result = template.render(
            name=name, description=description, installable=installable
        )
        file_name = template_name.replace(".j2", "")
        file_path = path / file_name
        file_path.write_text(result, encoding="utf-8")
    _create_package_structure(name)
    rprint(
        f"Initialized project [blue]{name}[/blue] "
        + (f"in [blue]{path.name}[/blue]" if path.name else "")
    )
