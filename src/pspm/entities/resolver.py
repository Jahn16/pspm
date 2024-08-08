"""Module with classes to deal with dependecy versions."""

from __future__ import annotations

import abc
import subprocess
from shutil import which

import uv


class BaseResolver(abc.ABC):
    """Base class for resolving dependencies.

    Attributes:
        pyproject_path: Path to pyproject.
    """

    def __init__(self, pyproject_path: str) -> None:
        """Initialize BaseResolver."""
        self.pyproject_path = pyproject_path

    @abc.abstractmethod
    def compile(self, output_file: str, group: str | None = None) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
        """
        raise NotImplementedError


class UVResolver(BaseResolver):
    """Class for resolving dependencies with UV."""

    def __init__(self, pyproject_path: str) -> None:
        """Initialize UV Compiler."""
        self.pyproject_path = pyproject_path
        self._uv_path = which("uv") or uv.find_uv_bin()

    def compile(self, output_file: str, group: str | None = None) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
        """
        extra_arguments = ["--extra", group] if group else []
        subprocess.call([  # noqa: S603
            self._uv_path,
            "pip",
            "compile",
            "-q",
            *extra_arguments,
            "-o",
            output_file,
            self.pyproject_path,
        ])
