"""Module to interact with pyproject.toml file."""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pspm.entities.toml import BaseToml


class BasePyproject:
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
    def add_dependency(self, package: str) -> None:
        """Add dependency to project.

        Args:
            package: Package to download
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_group_dependency(self, package: str, group: str) -> None:
        """Add optional-dependency with group to project.

        Args:
            package: Package to install
            group: Group that package will be inserted
        """
        raise NotImplementedError


class Pyproject(BasePyproject):
    """Class for manipulating pyproject.toml file."""

    def add_dependency(self, package: str) -> None:
        """Add dependency to project.

        Args:
            package: Package to download
        """
        data = self._parser.load()
        dependencies: list[str] = data["project"].get("dependencies", [])
        dependencies.append(package)
        data["project"]["dependencies"] = dependencies
        self._parser.dump(data)

    def add_group_dependency(self, package: str, group: str) -> None:
        """Add optional-dependency with group to project.

        Args:
            package: Package to install
            group: Group that package will be inserted
        """
        data = self._parser.load()
        optional_dependencies = data["project"].get(
            "optional-dependencies",
            {},
        )
        dependencies = optional_dependencies.get(group, [])
        dependencies.append(package)
        optional_dependencies[group] = dependencies
        data["project"]["optional-dependencies"] = optional_dependencies
        self._parser.dump(data)
