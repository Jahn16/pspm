import pytest

from pspm.entities.package_manager import PackageManager
from pspm.entities.pyproject import BasePyproject
from pspm.entities.toml import BaseToml
from pspm.entities.installer import BaseInstaller
from pspm.entities.resolver import BaseResolver
from typing import Any


class DummyToml(BaseToml):
    def __init__(self, path: str) -> None:
        self.data = {
            "project": {
                "name": "test",
                "dependencies": [
                    "foo",
                    "bar",
                ],
                "optional-dependencies": {
                    "dev": ["developing"],
                    "test": ["testing"],
                },
            },
        }

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
        self.added_dependencies.append(package)

    def add_group_dependency(self, package: str, group: str) -> None:
        self.added_group_dependencies[group] = (
            self.added_group_dependencies.get("group", []) + [package]
        )

    def get_extra_groups(self) -> list[str]:
        data = self._parser.load()
        return list(data["project"].get("optional-dependencies", {}).keys())


class DummyInstaller(BaseInstaller):
    def __init__(self) -> None:
        self.installed_packages: list[str] = []

    def install(self, package: str) -> None:
        self.installed_packages.append(package)

    def uninstall(self, package: str) -> None:
        raise NotImplementedError


class DummyResolver(BaseResolver):
    def __init__(self) -> None:
        self.output_files: list[str] = []

    def compile(self, output_file: str, group: str | None = None) -> None:
        output_file = f"requirements{'-' + group if group else ''}.lock"
        self.output_files.append(output_file)


@pytest.fixture
def toml() -> BaseToml:
    return DummyToml("bla")


@pytest.fixture
def pyproject(toml: BaseToml) -> BasePyproject:
    return DummyPyproject(toml)


@pytest.fixture
def installer() -> BaseInstaller:
    return DummyInstaller()


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
