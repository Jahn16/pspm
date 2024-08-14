"""Module with classes to deal with dependecy versions."""

from __future__ import annotations

import abc
import subprocess

from pspm.errors.dependencies import ResolveError
from pspm.utils.bin_path import get_uv_path


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
        *,
        upgrade: bool = False,
    ) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
            constraint_file: Requirements file to contrain versions
            upgrade: Whether to upgrade package versions
        """
        raise NotImplementedError


class UVResolver(BaseResolver):
    """Class for resolving dependencies with UV."""

    def __init__(self, pyproject_path: str) -> None:
        """Initialize UV Compiler."""
        self.pyproject_path = pyproject_path
        self._uv_path = get_uv_path()

    def compile(
        self,
        output_file: str,
        group: str | None = None,
        constraint_file: str | None = None,
        *,
        upgrade: bool = False,
    ) -> None:
        """Compiles requirements into a lock file.

        Args:
            output_file: File to write output
            group: Group to include dependencies from
            constraint_file: Requirements file to contrain versions
            upgrade: Whether to upgrade package versions

        Raises:
            ResolveError: If cant resolve dependencies
        """
        retcode = subprocess.call([
            self._uv_path,
            "pip",
            "compile",
            "-q",
            *(["--extra", group] if group else []),
            *(["--constraint", constraint_file] if constraint_file else []),
            *(["--upgrade"] if upgrade else []),
            "-o",
            output_file,
            self.pyproject_path,
        ])
        if retcode != 0:
            raise ResolveError
