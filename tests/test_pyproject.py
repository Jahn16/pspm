from __future__ import annotations

from typing import Any

import pytest
from pspm.entities.toml import BaseToml
from pspm.entities.pyproject import Pyproject


class DummyToml(BaseToml):
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def load(self) -> dict[str, Any]:
        return self.data

    def dump(self, data: dict[str, Any]) -> None:
        self.data = data


@pytest.fixture()
def requirements() -> dict[str, list[str]]:
    return {"main": ["foo", "bar"], "dev": ["developing"], "test": ["testing"]}


@pytest.fixture()
def version() -> str:
    return "1.1.1"


@pytest.fixture
def data(version: str, requirements: dict[str, list[str]]) -> dict[str, Any]:
    return {
        "project": {
            "name": "test",
            "version": version,
            "dependencies": requirements["main"],
            "optional-dependencies": {
                "dev": requirements["dev"],
                "test": requirements["test"],
            },
        },
    }


@pytest.fixture
def toml_parser(data: dict[str, Any]) -> BaseToml:
    return DummyToml(data)


@pytest.fixture()
def pyproject(toml_parser: BaseToml) -> Pyproject:
    return Pyproject(toml_parser)


def test_add_dependency(pyproject: Pyproject, toml_parser: BaseToml) -> None:
    package = "bla"
    data = toml_parser.load()
    expected_dependencies = data["project"]["dependencies"] + [package]
    pyproject.manage_dependency("add", package)
    result = toml_parser.load()
    assert result["project"]["dependencies"] == expected_dependencies


def test_remove_dependency(
    pyproject: Pyproject, toml_parser: BaseToml
) -> None:
    package = "foo"
    pyproject.manage_dependency("remove", package)
    result = toml_parser.load()
    assert result["project"]["dependencies"] == ["bar"]


def test_add_dependency_with_group(
    pyproject: Pyproject,
    toml_parser: BaseToml,
) -> None:
    package = "bla"
    group = "dev"
    data = toml_parser.load()
    expected_dependencies = data["project"].get(
        "optional-dependencies",
        {},
    ).get(group, []) + [
        package,
    ]
    pyproject.manage_dependency("add", package, group)
    result = toml_parser.load()
    assert (
        result["project"].get("optional-dependencies").get(group, [])
        == expected_dependencies
    )


def test_remove_dependency_with_group(
    pyproject: Pyproject, toml_parser: BaseToml
) -> None:
    group = "dev"
    pyproject.manage_dependency("remove", "developing", group)
    result = toml_parser.load()
    assert result["project"]["optional-dependencies"][group] == []


def test_dont_add_duplicate_dependency(
    pyproject: Pyproject, toml_parser: BaseToml
) -> None:
    data = toml_parser.load()
    dependencies = data["project"]["dependencies"].copy()
    package = dependencies[1]
    pyproject.manage_dependency("add", package)
    result = toml_parser.load()
    assert result["project"]["dependencies"] == dependencies


def test_get_extra_groups(pyproject: Pyproject, toml_parser: BaseToml) -> None:
    data = toml_parser.load()
    result = pyproject.get_extra_groups()
    assert result == ["dev", "test"]


def test_version_property(pyproject: Pyproject, version: str) -> None:
    assert pyproject.version == version


def test_version_change(pyproject: Pyproject) -> None:
    new_version = "2.3.4"
    pyproject.change_version(new_version)
    assert pyproject.version == new_version


@pytest.mark.parametrize(
    "rule,expected",
    [("major", "2.0.0"), ("minor", "1.2.0"), ("patch", "1.1.2")],
)
def test_version_bump(pyproject: Pyproject, rule: str, expected: str) -> None:
    pyproject.bump_version(rule)  # type: ignore
    assert pyproject.version == expected
