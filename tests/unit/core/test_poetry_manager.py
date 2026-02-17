from __future__ import annotations

from pathlib import Path

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.shell import CommandResult


def test_should_verify_poetry_is_installed(mocker):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="Poetry version 1.7.0", stderr="", returncode=0
    )
    manager = PoetryManager()

    result = manager.is_installed()

    assert result is True
    # Check that exec_cmd was called with poetry command (absolute path)
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["poetry", "--version"]
    assert call_args[1]["check"] is True


def test_should_configure_in_project_venv(mocker, tmp_path: Path):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    manager = PoetryManager()

    manager.configure_venv(tmp_path)

    # Checks only the main arguments, ignoring the env parameter
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == [
        "poetry",
        "config",
        "virtualenvs.in-project",
        "true",
        "--local",
    ]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_use_specific_python_version(mocker, tmp_path: Path):
    # Create a .venv file to simulate that it has already been created.
    (tmp_path / ".venv").mkdir()

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    python_path = Path("/usr/bin/python3.12")
    manager = PoetryManager()

    manager.use_python(tmp_path, python_path)

    # Checks only the main arguments, ignoring the env parameter
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["poetry", "env", "use", str(python_path)]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_get_virtualenv_path(mocker, tmp_path: Path):
    manager = PoetryManager()

    venv_path = manager.get_venv_path(tmp_path)

    assert venv_path == tmp_path / ".venv"


def test_should_install_dependencies(mocker, tmp_path: Path):
    # Create .venv to prevent _ensure_venv_exists from making extra call
    (tmp_path / ".venv").mkdir()

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="Installing dependencies...", stderr="", returncode=0
    )
    manager = PoetryManager()

    manager.install_dependencies(tmp_path)

    # Checks only the main arguments, ignoring the env parameter
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["poetry", "install", "--no-root"]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True
