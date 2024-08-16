from pspm.entities.virtual_env import BaseVirtualEnv
import pytest

from pspm.entities.package_manager import PackageManager
from pspm.entities.pyproject import BasePyproject
from pspm.entities.toml import BaseToml
from pspm.entities.installer import BaseInstaller
from pspm.entities.resolver import BaseResolver
from typing import Any, Literal


class DummyToml(BaseToml):
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def load(self) -> dict[str, Any]:
        return self.data

    def dump(self, data: dict[str, Any]) -> None:
        self.data = data


class DummyPyproject(BasePyproject):
    def __init__(self, toml_parser: BaseToml) -> None:
        self._parser = toml_parser
        self.added_dependencies: list[str] = []
        self.added_group_dependencies: dict[str, list[str]] = {}
        self.uninstalled_dependencies: list[str] = []
        self.uninstalled_group_dependencies: dict[str, list[str]] = {}

    def manage_dependency(
        self, action: str, package: str, group: str | None = None
    ) -> None:
        data = self._parser.load()
        if not group:
            if action == "add":
                data["project"]["dependencies"] += [package]
                self.added_dependencies.append(package)
            else:
                data["project"]["dependencies"].remove(package)
                self.uninstalled_dependencies.append(package)
        else:
            if action == "add":
                data["project"]["optional-dependencies"][group] += [package]
                self.added_group_dependencies[group] = (
                    self.added_group_dependencies.get("group", []) + [package]
                )
            else:
                data["project"]["optional-dependencies"][group].remove(package)
                self.uninstalled_group_dependencies[group] = (
                    self.uninstalled_group_dependencies.get("group", [])
                    + [package]
                )
        self._parser.dump(data)

    def get_extra_groups(self) -> list[str]:
        data = self._parser.load()
        return list(data["project"].get("optional-dependencies", {}).keys())

    def is_installable(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "0.0.0"

    def change_version(self, new_version: str) -> str:
        return "0.0.0"

    def bump_version(self, rule: str) -> str:
        return "0.0.0"


class DummyInstaller(BaseInstaller):
    def __init__(self, toml: BaseToml) -> None:
        self.installed_packages: list[str] = []
        self._toml = toml

    def install(self, package: str, *, editable: bool = True) -> None:
        self.installed_packages.append(package)

    def uninstall(self, package: str) -> None:
        raise NotImplementedError

    def sync(self, requirements_files: list[str]) -> None:
        data = self._toml.load()
        requirements_per_file = {
            "requirements.lock": data["project"]["dependencies"],
            "requirements-dev.lock": data["project"]["optional-dependencies"][
                "dev"
            ],
            "requirements-test.lock": data["project"]["optional-dependencies"][
                "test"
            ],
        }
        packages: list[str] = []
        for f in requirements_files:
            packages.extend(requirements_per_file[f])
        self.installed_packages = packages


class DummyResolver(BaseResolver):
    def __init__(self) -> None:
        self.output_files: list[str] = []
        self.constraints_used: dict[str, str | None] = {}
        self.upgraded = False

    def compile(
        self,
        output_file: str,
        group: str | None = None,
        constraint_file: str | None = None,
        *,
        upgrade: bool = False,
    ) -> None:
        output_file = f"requirements{'-' + group if group else ''}.lock"
        self.output_files.append(output_file)
        self.constraints_used[output_file] = constraint_file
        self.upgraded = upgrade


class DummyVenv(BaseVirtualEnv):
    def __init__(self) -> None:
        self.created = False

    def already_created(self) -> bool:
        return self.created

    def create(self) -> None:
        self.created = True

    def get_path_to_command_bin(self, command: str) -> None:
        raise NotImplementedError


@pytest.fixture()
def requirements() -> dict[str, list[str]]:
    return {"main": ["foo", "bar"], "dev": ["developing"], "test": ["testing"]}


@pytest.fixture
def data(requirements: dict[str, list[str]]) -> dict[str, Any]:
    return {
        "project": {
            "name": "test",
            "dependencies": requirements["main"],
            "optional-dependencies": {
                "dev": requirements["dev"],
                "test": requirements["test"],
            },
        },
    }


@pytest.fixture
def toml(data: dict[str, Any]) -> BaseToml:
    return DummyToml(data)


@pytest.fixture
def pyproject(toml: BaseToml) -> BasePyproject:
    return DummyPyproject(toml)


@pytest.fixture
def installer(toml: BaseToml) -> BaseInstaller:
    return DummyInstaller(toml)


@pytest.fixture
def virtual_env() -> BaseVirtualEnv:
    return DummyVenv()


@pytest.fixture
def resolver() -> BaseResolver:
    return DummyResolver()


@pytest.fixture
def package_manager(
    pyproject: BasePyproject,
    installer: BaseInstaller,
    resolver: BaseResolver,
    virtual_env: BaseVirtualEnv,
) -> PackageManager:
    return PackageManager(pyproject, installer, resolver, virtual_env)


@pytest.fixture
def package() -> str:
    return "test-package"


def test_add_dependency(
    package: str,
    package_manager: PackageManager,
    pyproject: DummyPyproject,
    installer: DummyInstaller,
    resolver: DummyResolver,
) -> None:
    package_manager.manage_dependency("add", package)
    assert package in pyproject.added_dependencies
    assert package in installer.installed_packages
    assert "requirements.lock" in resolver.output_files


def test_remove_dependency(
    package_manager: PackageManager,
    pyproject: DummyPyproject,
    installer: DummyInstaller,
    resolver: DummyResolver,
) -> None:
    package = "foo"
    package_manager.manage_dependency("remove", package)
    assert package in pyproject.uninstalled_dependencies
    assert package not in installer.installed_packages
    assert "requirements.lock" in resolver.output_files


@pytest.mark.parametrize("action", ["add", "remove"])
def test_manage_dependency_compiles_all_files(
    action: Literal["add", "remove"],
    package_manager: PackageManager,
    resolver: DummyResolver,
) -> None:
    package = "bla" if action == "add" else "foo"
    package_manager.manage_dependency(action, package)

    groups = ["dev", "test"]
    files = ["requirements.lock"] + [
        f"requirements-{group}" for group in groups
    ]

    assert resolver.output_files.sort() == files.sort()


def test_add_dependency_with_group(
    package: str,
    package_manager: PackageManager,
    pyproject: DummyPyproject,
    installer: DummyInstaller,
    resolver: DummyResolver,
) -> None:
    group = "test"
    package_manager.manage_dependency("add", package, group)
    output_file = f"requirements-{group}.lock"

    assert package in pyproject.added_group_dependencies.get(group, [])
    assert package in installer.installed_packages
    assert output_file in resolver.output_files
    assert resolver.constraints_used[output_file] == "requirements.lock"


def test_remove_dependency_with_group(
    package_manager: PackageManager,
    pyproject: DummyPyproject,
    installer: DummyInstaller,
    resolver: DummyResolver,
) -> None:
    package = "testing"
    group = "test"
    package_manager.manage_dependency("remove", package, group)

    assert package in pyproject.uninstalled_group_dependencies.get(group, [])
    assert package not in installer.installed_packages
    assert f"requirements-{group}.lock" in resolver.output_files


def test_compile_requirements_upgrade(
    package_manager: PackageManager, resolver: DummyResolver
) -> None:
    package_manager.compile_requirements(upgrade=True)
    assert resolver.upgraded == True
