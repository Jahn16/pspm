import pytest

from pspm.entities.command_runner import BaseCommandRunner
from pspm.entities.installer import UVInstaller
from pspm.errors.dependencies import InstallError, SyncError


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
def installer(command_runner: BaseCommandRunner) -> UVInstaller:
    return UVInstaller(command_runner)


def test_install(
    installer: UVInstaller, command_runner: DummyCommandRunner
) -> None:
    package = "banana"
    args = ["pip", "install", package]
    installer.install(package)
    assert command_runner.command.endswith("uv")
    assert command_runner.arguments == args


def test_install_editable(
    installer: UVInstaller, command_runner: DummyCommandRunner
) -> None:
    package = "banana"
    args = ["pip", "install", "--editable", package]
    installer.install(package, editable=True)
    assert command_runner.arguments == args


def test_raises_install_error(installer: UVInstaller) -> None:
    package = "invalid"
    with pytest.raises(InstallError):
        installer.install(package)


def test_sync(
    installer: UVInstaller, command_runner: DummyCommandRunner
) -> None:
    requirements_files = [
        "requirements.lock",
        "requirements-dev.lock",
        "requirements-docs.lock",
    ]
    args = ["pip", "sync"] + requirements_files
    installer.sync(requirements_files)
    assert command_runner.command.endswith("uv")
    assert command_runner.arguments == args


def test_sync_raises_error(installer: UVInstaller) -> None:
    requirements_files = [
        "requirements.lock",
        "requirements-dev.lock",
        "invalid",
    ]
    with pytest.raises(SyncError):
        installer.sync(requirements_files)
