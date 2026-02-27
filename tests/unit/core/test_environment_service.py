from __future__ import annotations

import subprocess
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from api_bootstrapper_cli.core.environment_service import (
    EnvironmentBootstrapService,
    EnvironmentSetupResult,
)


class MockLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg: str) -> None:
        self.messages.append(("info", msg))

    def success(self, msg: str) -> None:
        self.messages.append(("success", msg))

    def error(self, msg: str) -> None:
        self.messages.append(("error", msg))

    def warning(self, msg: str) -> None:
        self.messages.append(("warning", msg))


class MockPythonEnvManager:
    def __init__(self):
        self.installed = True
        self.name = "pyenv"
        self.python_path = Path("/home/user/.pyenv/versions/3.12.3/bin/python")

    def is_installed(self) -> bool:
        return cast(bool, self.installed)

    def ensure_python(self, version: str):
        pass

    def set_local(self, path: Path, version: str):
        pass

    def get_python_path(self, version: str) -> Path:
        return cast(Path, self.python_path)

    def install_pip_packages(self, version: str, packages: list[str]):
        pass


class MockDependencyManager:
    name: str = "Poetry"

    def is_installed(self) -> bool:
        return True

    def configure_venv(self, path: Path) -> None:
        pass

    def use_python(self, path: Path, python_path: Path) -> None:
        pass

    def ensure_venv(self, path: Path) -> None:
        pass

    def install_dependencies(self, path: Path) -> None:
        pass

    def get_venv_path(self, path: Path) -> Path:
        return path / ".venv"

    def get_venv_python(self, path: Path) -> Path:
        return path / ".venv" / "bin" / "python"


class MockEditorWriter:
    def write_config(self, project_root: Path, python_path: Path) -> Path:
        return project_root / ".vscode" / "settings.json"


def test_should_return_existing_environment_when_already_configured(
    tmp_path: Path,
):
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[tool.poetry]\nname = "test"\nversion = "1.0.0"')

    python_version_file = tmp_path / ".python-version"
    python_version_file.write_text("3.12.3")

    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    (vscode_dir / "settings.json").touch()

    logger = MockLogger()
    service = EnvironmentBootstrapService(
        python_env_manager=MockPythonEnvManager(),
        dependency_manager=MockDependencyManager(),
        editor_writer=MockEditorWriter(),
        logger=logger,
    )

    mock_completed = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="Python 3.12.3\n", stderr=""
    )
    with patch(
        "api_bootstrapper_cli.core.environment_service.subprocess.run",
        return_value=mock_completed,
    ):
        result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)

    assert isinstance(result, EnvironmentSetupResult)
    assert result.python_version == "3.12.3"
    assert result.venv_path == venv_path
    assert result.venv_python == venv_path / "bin" / "python"
    assert result.has_poetry_project is True

    messages = [msg for level, msg in logger.messages]
    assert "environment already configured" in messages
    assert "environment ready" in messages


def test_should_recreate_environment_when_python_version_mismatches(
    tmp_path: Path, mocker
):
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[tool.poetry]\nname = "test"\nversion = "1.0.0"')

    python_version_file = tmp_path / ".python-version"
    python_version_file.write_text("3.11.0")

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    editor = MockEditorWriter()

    ensure_python_spy = mocker.spy(python_env, "ensure_python")
    install_deps_spy = mocker.spy(deps, "install_dependencies")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=editor,
        logger=logger,
    )

    result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)

    ensure_python_spy.assert_called_once_with("3.12.3")
    assert install_deps_spy.call_count >= 1

    assert result.python_version == "3.12.3"


def test_should_create_environment_when_venv_is_missing(tmp_path: Path, mocker):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[tool.poetry]\nname = "test"\nversion = "1.0.0"')

    python_version_file = tmp_path / ".python-version"
    python_version_file.write_text("3.12.3")

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    editor = MockEditorWriter()

    ensure_python_spy = mocker.spy(python_env, "ensure_python")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=editor,
        logger=logger,
    )

    result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)

    ensure_python_spy.assert_called_once_with("3.12.3")
    assert result.python_version == "3.12.3"


def test_should_create_environment_when_pyproject_is_missing(tmp_path: Path, mocker):
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()

    python_version_file = tmp_path / ".python-version"
    python_version_file.write_text("3.12.3")

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    editor = MockEditorWriter()

    ensure_python_spy = mocker.spy(python_env, "ensure_python")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=editor,
        logger=logger,
    )

    result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)

    ensure_python_spy.assert_called_once_with("3.12.3")
    assert result.python_version == "3.12.3"


def test_should_create_environment_when_python_version_file_is_missing(
    tmp_path: Path, mocker
):
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[tool.poetry]\nname = "test"\nversion = "1.0.0"')

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    editor = MockEditorWriter()

    ensure_python_spy = mocker.spy(python_env, "ensure_python")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=editor,
        logger=logger,
    )

    result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)

    ensure_python_spy.assert_called_once_with("3.12.3")
    assert result.python_version == "3.12.3"


def test_should_raise_error_when_pyenv_not_installed(tmp_path: Path):
    logger = MockLogger()
    python_env = MockPythonEnvManager()
    python_env.installed = False  # Simulate pyenv not installed

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=MockDependencyManager(),
        editor_writer=MockEditorWriter(),
        logger=logger,
    )

    with pytest.raises(ValueError, match="pyenv not found"):
        service.bootstrap(tmp_path, "3.12.3", install_dependencies=True)


# ── Additional error and edge-case tests (Item 8) ─────────────────────────────


def test_should_force_setup_when_venv_python_version_mismatches(tmp_path: Path, mocker):
    """_is_environment_ready returns False when venv Python doesn't match requested version."""
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()

    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "t"\nversion = "1"')
    (tmp_path / ".python-version").write_text("3.12.3")

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    ensure_python_spy = mocker.spy(python_env, "ensure_python")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=MockEditorWriter(),
        logger=logger,
    )

    # Simulate venv Python reporting 3.11 while requested is 3.12
    mock_completed = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="Python 3.11.9\n", stderr=""
    )
    with patch(
        "api_bootstrapper_cli.core.environment_service.subprocess.run",
        return_value=mock_completed,
    ):
        result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=False)

    # Full setup MUST have run (ensure_python called)
    ensure_python_spy.assert_called_once_with("3.12.3")
    assert result.python_version == "3.12.3"


def test_should_force_setup_when_venv_python_not_runnable(tmp_path: Path, mocker):
    """_is_environment_ready returns False when running venv Python raises an error."""
    venv_path = tmp_path / ".venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir(parents=True)
    (venv_path / "bin" / "python").touch()  # Not executable

    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "t"\nversion = "1"')
    (tmp_path / ".python-version").write_text("3.12.3")

    logger = MockLogger()
    python_env = MockPythonEnvManager()
    deps = MockDependencyManager()
    ensure_python_spy = mocker.spy(python_env, "ensure_python")

    service = EnvironmentBootstrapService(
        python_env_manager=python_env,
        dependency_manager=deps,
        editor_writer=MockEditorWriter(),
        logger=logger,
    )

    with patch(
        "api_bootstrapper_cli.core.environment_service.subprocess.run",
        side_effect=OSError("Cannot execute"),
    ):
        result = service.bootstrap(tmp_path, "3.12.3", install_dependencies=False)

    ensure_python_spy.assert_called_once_with("3.12.3")
    assert result.python_version == "3.12.3"
