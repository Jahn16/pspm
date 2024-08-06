from __future__ import annotations

from typing import Any

import pytest
from pspm.entities.toml import BaseToml
from pspm.services.pyproject import Pyproject


class TestToml(BaseToml):
    def __init__(self, path: str) -> None:
        self.data = {
            "project": {
                "name": "test",
                "dependencies": [
                    "foo",
                    "bar",
                ],
            },
        }

    def load(self) -> dict[str, Any]:
        return self.data

    def dump(self, data: dict[str, Any]) -> None:
        return


@pytest.fixture()
def pyproject() -> Pyproject:
    toml_parser = TestToml("foobar")
    return Pyproject(toml_parser)


def test_add_dependency(pyproject: Pyproject) -> None:
    package = "bla"
    data = pyproject._parser.load()
    expected_dependencies = data["project"]["dependencies"] + [package]
    pyproject.add_dependency(package)
    result = pyproject._parser.load()
    assert result["project"]["dependencies"] == expected_dependencies


def test_add_dependency_with_group(pyproject: Pyproject) -> None:
    package = "bla"
    group = "dev"
    data = pyproject._parser.load()
    expected_dependencies = data["project"].get(
        "optional-dependencies",
        {},
    ).get(group, []) + [
        package,
    ]
    pyproject.add_dependency(package, group)
    result = pyproject._parser.load()
    assert (
        result["project"].get("optional-dependencies", {}).get(group, [])
        == expected_dependencies
    )
