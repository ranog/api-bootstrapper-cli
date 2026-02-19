from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

import pytest


BOX_BORDER_RE = re.compile(r"^[╭╰│].*[╮╯│]$")


def normalize_help_lines(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # remove purely box lines (borders and lines with │ ... │)
    return [ln for ln in lines if not BOX_BORDER_RE.match(ln)]


@pytest.fixture
def expected_bootstrap_help() -> list[str]:
    return [
        "Usage: root bootstrap-env [OPTIONS]",
        "Setup Python environment with pyenv, Poetry, and VSCode configuration.",
        "Creates or configures:",
        "- Python version via pyenv (.python-version)",
        "- Poetry virtual environment (.venv)",
        "- VSCode Python settings (.vscode/settings.json)",
        "- Minimal pyproject.toml (if doesn't exist)",
    ]


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
