import pytest

from pspm.entities.command_runner import BaseCommandRunner
from pspm.entities.resolver import UVResolver


class DummyCommandRunner:
    def run(self, command: str, arguments: list[str] | None = None) -> int:
        self.command = command
        self.arguments = arguments or []
        if arguments and arguments[-1] == "invalid":
            return -1
        return 0


@pytest.fixture
def command_runner() -> DummyCommandRunner:
    return DummyCommandRunner()


@pytest.fixture
def pyproject_path() -> str:
    return "pyproject.toml"


@pytest.fixture
def resolver(
    command_runner: BaseCommandRunner, pyproject_path: str
) -> UVResolver:
    return UVResolver(command_runner)


@pytest.fixture
def output_file() -> str:
    return "requirements.lock"


def test_compile(
    resolver: UVResolver,
    command_runner: DummyCommandRunner,
    pyproject_path: str,
    output_file: str,
) -> None:
    args = [
        "pip",
        "compile",
        "-q",
        "-o",
        output_file,
        pyproject_path,
    ]
    resolver.compile(output_file)
    assert command_runner.command.endswith("uv")
    assert command_runner.arguments == args


def test_compile_with_group(
    resolver: UVResolver,
    command_runner: DummyCommandRunner,
    output_file: str,
) -> None:
    group = "docs"
    resolver.compile(output_file, group=group)
    assert command_runner.command.endswith("uv")
    assert f"--extra {group}" in " ".join(command_runner.arguments)


def test_compile_with_constraint(
    resolver: UVResolver,
    command_runner: DummyCommandRunner,
    output_file: str,
) -> None:
    constraint_file = "constraint.lock"
    resolver.compile(output_file, constraint_file=constraint_file)
    assert command_runner.command.endswith("uv")
    assert f"--constraint {constraint_file}" in " ".join(
        command_runner.arguments
    )


def test_compile_with_upgrade(
    resolver: UVResolver,
    command_runner: DummyCommandRunner,
    output_file: str,
) -> None:
    resolver.compile(output_file, upgrade=True)
    assert command_runner.command.endswith("uv")
    assert "--upgrade" in command_runner.arguments
