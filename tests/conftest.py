from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

import pytest


def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


@pytest.fixture
def expected_bootstrap_help() -> str:
    return (
        "                                                                                \n"
        " Usage: root bootstrap-env [OPTIONS]                                            \n"
        "                                                                                \n"
        " Setup Python environment with pyenv, Poetry, and VSCode configuration.         \n"
        "                                                                                \n"
        " Creates or configures:                                                         \n"
        " - Python version via pyenv (.python-version)                                   \n"
        " - Poetry virtual environment (.venv)                                           \n"
        " - VSCode Python settings (.vscode/settings.json)                               \n"
        " - Minimal pyproject.toml (if doesn't exist)                                    \n"
        "                                                                                \n"
        "╭─ Options ────────────────────────────────────────────────────────────────────╮\n"
        "│ --path                       PATH  Target project folder (default: current). │\n"
        "│                                    [default: .]                              │\n"
        "│ --python                     TEXT  Python version to use via pyenv.          │\n"
        "│                                    [default: 3.12.12]                        │\n"
        "│ --install    --no-install          Run 'poetry install'. [default: install]  │\n"
        "│ --help                             Show this message and exit.               │\n"
        "╰──────────────────────────────────────────────────────────────────────────────╯\n"
        "\n"
    )


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
