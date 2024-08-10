import pytest

from pspm.entities.package_manager import PackageManager
from pspm.entities.pyproject import BasePyproject
from pspm.entities.toml import BaseToml
from pspm.entities.installer import BaseInstaller
from pspm.entities.resolver import BaseResolver
from typing import Any


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

    def add_dependency(self, package: str) -> None:
        data = self._parser.load()
        data["project"]["dependencies"] += [package]
        self._parser.dump(data)
        self.added_dependencies.append(package)

    def add_group_dependency(self, package: str, group: str) -> None:
        data = self._parser.load()
        data["project"]["optional-dependencies"][group] += [package]
        self._parser.dump(data)
        self.added_group_dependencies[group] = (
            self.added_group_dependencies.get("group", []) + [package]
        )

    def get_extra_groups(self) -> list[str]:
        data = self._parser.load()
        return list(data["project"].get("optional-dependencies", {}).keys())


class DummyInstaller(BaseInstaller):
    def __init__(self, toml: BaseToml) -> None:
        self.installed_packages: list[str] = []
        self._toml = toml

    def install(self, package: str, *, editable=True) -> None:
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

    def compile(self, output_file: str, group: str | None = None) -> None:
        output_file = f"requirements{'-' + group if group else ''}.lock"
        self.output_files.append(output_file)


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
def resolver() -> BaseResolver:
    return DummyResolver()


@pytest.fixture
def package_manager(
    pyproject: BasePyproject, installer: BaseInstaller, resolver: BaseResolver
) -> PackageManager:
    return PackageManager(pyproject, installer, resolver)


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
    package_manager.add_dependency(package)

    assert package in pyproject.added_dependencies
    assert package in installer.installed_packages
    assert "requirements.lock" in resolver.output_files


def test_add_dependency_compiles_all_files(
    package: str,
    package_manager: PackageManager,
    resolver: DummyResolver,
) -> None:
    package_manager.add_dependency(package)

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
    package_manager.add_dependency(package, group)

    assert package in pyproject.added_group_dependencies.get(group, [])
    assert package in installer.installed_packages
    assert f"requirements-{group}.lock" in resolver.output_files
