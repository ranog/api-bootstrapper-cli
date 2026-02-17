from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    yield project_dir


@pytest.fixture
def mock_pyproject_toml(temp_project_dir: Path) -> Path:
    pyproject = temp_project_dir / "pyproject.toml"
    pyproject.write_text(
        """
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test project"
authors = ["Test <test@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )
    return pyproject
