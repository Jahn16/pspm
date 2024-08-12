"""Module to interact with pyproject.toml file."""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

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
    def add_dependency(self, package: str, group: str | None = None) -> None:
        """Add dependency to project.

        Args:
            package: Package to download
            group: Group that package will be inserted
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_extra_groups(self) -> list[str]:
        """Retrieve list of extra groups."""
        raise NotImplementedError


class Pyproject(BasePyproject):
    """Class for manipulating pyproject.toml file."""

    def add_dependency(self, package: str, group: str | None = None) -> None:
        """Add dependency to project.

        Args:
            package: Package to download
            group: Group that package will be inserted
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
        if package in packages:
            return
        packages.append(package)
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
