from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from api_bootstrapper_cli.core.mypy_manager import MypyManager
from api_bootstrapper_cli.core.protocols import ManagerChoice


def test_should_detect_poetry_manager(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.poetry]\nname = 'demo'\n")

    manager = MypyManager()

    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.pyenv


def test_should_detect_uv_manager(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'demo'\n")

    manager = MypyManager()

    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.uv


@patch("api_bootstrapper_cli.core.mypy_manager.exec_cmd")
def test_should_setup_mypy_for_poetry_project(
    mock_exec: MagicMock,
    tmp_path: Path,
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """\
[tool.poetry]
name = "demo"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )

    manager = MypyManager()

    result = manager.setup(tmp_path, manager=ManagerChoice.pyenv)
    content = pyproject.read_text(encoding="utf-8")

    assert result.manager == ManagerChoice.pyenv
    assert result.pyproject_path == pyproject
    assert result.config_already_existed is False
    assert result.version == "1.19.1"
    assert '[tool.poetry.group.dev.dependencies]\nmypy = "^1.19.1"\n' in content
    assert "[tool.mypy]" in content
    assert mock_exec.call_args_list == [
        call(["poetry", "lock"], cwd=str(tmp_path), check=True),
        call(["poetry", "install", "--no-root"], cwd=str(tmp_path), check=True),
    ]


@patch("api_bootstrapper_cli.core.mypy_manager.exec_cmd")
def test_should_setup_mypy_for_uv_project(
    mock_exec: MagicMock,
    tmp_path: Path,
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """\
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
"""
    )

    manager = MypyManager()

    result = manager.setup(tmp_path, manager=ManagerChoice.uv)
    content = pyproject.read_text(encoding="utf-8")

    assert result.manager == ManagerChoice.uv
    assert result.config_already_existed is False
    assert result.version == "1.19.1"
    assert "[project.optional-dependencies]" in content
    assert '"mypy>=1.19.1,<2",' in content
    assert "[tool.mypy]" in content
    mock_exec.assert_called_once_with(
        ["uv", "sync", "--all-groups"],
        cwd=str(tmp_path),
        check=True,
    )


@patch("api_bootstrapper_cli.core.mypy_manager.exec_cmd")
def test_should_create_uv_dev_group_when_optional_dependencies_exists_without_dev(
    mock_exec: MagicMock,
    tmp_path: Path,
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """\
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
docs = ["mkdocs>=1.6.0"]
"""
    )

    manager = MypyManager()

    manager.setup(tmp_path, manager=ManagerChoice.uv)
    content = pyproject.read_text(encoding="utf-8")

    assert "dev = [" in content
    assert '"mypy>=1.19.1,<2",' in content
    mock_exec.assert_called_once()


@patch("api_bootstrapper_cli.core.mypy_manager.exec_cmd")
def test_should_preserve_existing_tool_mypy_section(
    mock_exec: MagicMock,
    tmp_path: Path,
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """\
[tool.poetry]
name = "demo"

[tool.mypy]
python_version = "3.12"
"""
    )

    manager = MypyManager()

    result = manager.setup(tmp_path, manager=ManagerChoice.pyenv)
    content = pyproject.read_text(encoding="utf-8")

    assert result.config_already_existed is True
    assert content.count("[tool.mypy]") == 1
    assert 'mypy = "^1.19.1"' in content
    assert mock_exec.call_count == 2


@patch("api_bootstrapper_cli.core.mypy_manager.exec_cmd")
def test_should_not_duplicate_mypy_dependency_for_poetry(
    mock_exec: MagicMock,
    tmp_path: Path,
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """\
[tool.poetry]
name = "demo"

[tool.poetry.group.dev.dependencies]
mypy = "^1.19.1"
"""
    )

    manager = MypyManager()

    manager.setup(tmp_path, manager=ManagerChoice.pyenv)
    content = pyproject.read_text(encoding="utf-8")

    assert content.count('mypy = "^1.19.1"') == 1
    assert mock_exec.call_count == 2


def test_should_raise_value_error_when_project_root_not_exists() -> None:
    manager = MypyManager()

    with pytest.raises(ValueError, match="Project root does not exist"):
        manager.setup(Path("/non/existent/path"), manager=ManagerChoice.pyenv)


def test_should_raise_file_not_found_when_pyproject_is_missing(
    tmp_path: Path,
) -> None:
    manager = MypyManager()

    with pytest.raises(FileNotFoundError, match="pyproject.toml not found"):
        manager.setup(tmp_path, manager=ManagerChoice.pyenv)
