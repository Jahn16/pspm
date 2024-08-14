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
    def compile(
        self,
        output_file: str,
        group: str | None = None,
        constraint_file: str | None = None,
    ) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
            constraint_file: Requirements file to contrain versions
        """
        raise NotImplementedError


class UVResolver(BaseResolver):
    """Class for resolving dependencies with UV."""

    def __init__(self, pyproject_path: str) -> None:
        """Initialize UV Compiler."""
        self.pyproject_path = pyproject_path
        self._uv_path = which("uv") or uv.find_uv_bin()
        self._uv_path = (
            "/nix/store/2gv9l9nm38dhniynb3mm1s41yqxh4p2c-uv-0.2.27/bin/uv"
        )

    def compile(
        self,
        output_file: str,
        group: str | None = None,
        constraint_file: str | None = None,
    ) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
            constraint_file: Requirements file to contrain versions
        """
        subprocess.call([
            self._uv_path,
            "pip",
            "compile",
            "-q",
            *(["--extra", group] if group else []),
            *(["--constraint", constraint_file] if constraint_file else []),
            "-o",
            output_file,
            self.pyproject_path,
        ])
