"""Module to interact with pyproject.toml file."""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from pspm.entities.toml import BaseToml


class BasePyproject(abc.ABC):
    """Manipulate pyproject.

    Attributes:
        toml_parser: Parser to be used for parsing TOML
    """

    def __init__(self, toml_parser: BaseToml) -> None:
        """Iniatilize BasePyproject.

        Args:
            toml_parser: Parser to be used for parsing TOML
        """
        self._parser = toml_parser

    @abc.abstractmethod
    def manage_dependency(
        self,
        action: Literal["add", "remove"],
        package: str,
        group: str | None = None,
    ) -> None:
        """Add or removes dependency from project.

        Args:
            action: Action to take can be either add or remove
            package: Package to manage
            group: Group that package belongs
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_extra_groups(self) -> list[str]:
        """Retrieve list of extra groups."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_installable(self) -> bool:
        """Determine if project is installable.

        Returns:
            Whether the project is installable
        """
        raise NotImplementedError


class Pyproject(BasePyproject):
    """Class for manipulating pyproject.toml file."""

    def manage_dependency(
        self,
        action: Literal["add", "remove"],
        package: str,
        group: str | None = None,
    ) -> None:
        """Add or removes dependency from project.

        Args:
            action: Action to take can be either add or remove
            package: Package to manage
            group: Group that package belongs
        """
        data = self._parser.load()
        project: dict[str, Any] = data.get("project", {})
        optional_dependencies: dict[str, list[str]] = project.get(
            "optional-dependencies", {}
        )
        packages: list[str] = (
            project.get("dependencies", [])
            if not group
            else optional_dependencies.get(group, [])
        )
        if (action == "add" and package in packages) or (
            action == "remove" and package not in packages
        ):
            return
        (
            packages.append(package)
            if action == "add"
            else packages.remove(package)
        )
        if not group:
            project["dependencies"] = packages
        else:
            optional_dependencies[group] = packages
            project["optional-dependencies"] = optional_dependencies
        data["project"] = project
        self._parser.dump(data)

    def get_extra_groups(self) -> list[str]:
        """Retrieve list of extra groups.

        Returns:
            List of extra groups
        """
        data = self._parser.load()
        optional_dependencies = data["project"].get(
            "optional-dependencies",
            {},
        )
        return list(optional_dependencies.keys())

    def is_installable(self) -> bool:
        """Determine if project is installable.

        Returns:
            Whether the project is installable
        """
        data = self._parser.load()
        return data.get("build-system") is not None
