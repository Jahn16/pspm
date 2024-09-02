"""Module with classes to deal with dependecy versions."""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from pspm.errors.dependencies import ResolveError
from pspm.utils.bin_path import get_uv_path

if TYPE_CHECKING:
    from pspm.entities.command_runner import BaseCommandRunner


class BaseResolver(abc.ABC):
    """Base class for resolving dependencies."""

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

    def __init__(self, command_runner: BaseCommandRunner) -> None:
        """Initialize UV Compiler."""
        self._uv_path = get_uv_path()
        self._command_runner = command_runner

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
        args = [
            "pip",
            "compile",
            "-q",
            *(["--extra", group] if group else []),
            *(["--constraint", constraint_file] if constraint_file else []),
            *(["--upgrade"] if upgrade else []),
            "-o",
            output_file,
            "pyproject.toml",
        ]
        retcode = self._command_runner.run(self._uv_path, args)
        if retcode != 0:
            raise ResolveError
