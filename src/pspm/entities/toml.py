"""Module for interacting with toml files."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any

import tomli
import tomli_w


class BaseToml(abc.ABC):
    """TOML Parser and writer.

    Attributes:
        path: TOML file path
    """

    def __init__(self, path: str) -> None:
        """Initialize TOML.

        Args:
            path: File path to TOML file
        """
        self.path = path

    @abc.abstractmethod
    def load(self) -> dict[str, Any]:
        """Load TOML file."""
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self, data: dict[str, Any]) -> None:
        """Write a dictionary to a file containing TOML-formatted data.

        Args:
            data: TOML data
        """
        raise NotImplementedError


class Toml(BaseToml):
    """TOML Parser and writer."""

    def load(self) -> dict[str, Any]:
        """Load TOML file.

        Returns:
            A dictionary containing parsed TOML
        """
        with Path(self.path).open("rb") as f:
            return tomli.load(f)

    def dump(self, data: dict[str, Any]) -> None:
        """Write a dictionary to a file containing TOML-formatted data.

        Args:
            data: TOML data
        """
        with Path(self.path).open("wb") as f:
            tomli_w.dump(data, f)
