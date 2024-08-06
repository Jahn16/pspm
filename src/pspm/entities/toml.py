"""Module for interacting with toml files."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any

import toml


class BaseToml(abc.ABC):
    """Base abstract class for TOML."""

    def __init__(self, path: str) -> None:
        """Initialize TOML.

        :param path: File path to TOML file
        """
        self.path = path

    @abc.abstractmethod
    def load(self) -> dict[str, Any]:
        """Load TOML file.

        :return: A dictionary containing parsed TOML
        """
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self, data: dict[str, Any]) -> None:
        """Write a dictionary to a file containing TOML-formatted data.

        :param data: TOML data
        """
        raise NotImplementedError


class Toml(BaseToml):
    """Class for manipulating TOML files."""

    def load(self) -> dict[str, Any]:
        """Load TOML file.

        :return: A dictionary containing parsed TOML
        """
        return toml.load(self.path)

    def dump(self, data: dict[str, Any]) -> None:
        """Write a dictionary to a file containing TOML-formatted data.

        :param data: TOML data
        """
        with Path(self.path).open("w", encoding="utf-8") as f:
            toml.dump(data, f)
