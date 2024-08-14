"""Module to handle bootstrap of project."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, PackageLoader


def _create_package_structure(name: str) -> None:
    safe_name = name.lower().replace("-", "_")
    package_init = Path(f"src/{safe_name}/__init__.py")
    package_init.parent.mkdir(parents=True, exist_ok=True)
    package_init.write_text("")


def bootstrap_project(
    name: str, description: str | None, *, installable: bool
) -> None:
    """Create initial project structure.

    Args:
        name: Project name
        description: Project description
        installable: Whether the project is installable
    """
    if description is None:
        description = "Describe your project here"

    env = Environment(loader=PackageLoader("pspm"), autoescape=True)
    template_names = env.list_templates()
    for template_name in template_names:
        template = env.get_template(template_name)
        result = template.render(
            name=name, description=description, installable=installable
        )
        file_name = template_name.replace(".j2", "")
        Path(file_name).write_text(result, encoding="utf-8")
    _create_package_structure(name)
