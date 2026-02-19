from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.shell import CommandResult


@pytest.mark.integration
def test_should_detect_pyenv_installation(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="pyenv 2.3.0", stderr="", returncode=0
    )

    pyenv = PyenvManager()

    assert pyenv.is_installed()
    assert mock_exec.call_count == 1
    assert mock_exec.call_args[0][0] == ["pyenv", "--version"]


@pytest.mark.integration
def test_should_detect_poetry_installation(mocker):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="Poetry 1.7.0", stderr="", returncode=0
    )

    poetry = PoetryManager()

    assert poetry.is_installed()
    assert mock_exec.call_count == 1
    assert mock_exec.call_args[0][0] == ["poetry", "--version"]


@pytest.mark.integration
def test_should_set_local_python_version_in_directory(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    pyenv = PyenvManager()
    pyenv.set_local(tmp_path, "3.12.3")

    assert mock_exec.called
    call_args = mock_exec.call_args[0][0]
    assert call_args == ["pyenv", "local", "3.12.3"]


@pytest.mark.integration
def test_should_configure_poetry_venv_location(mocker, tmp_path: Path):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    poetry = PoetryManager()
    poetry.configure_venv(tmp_path)

    assert mock_exec.called
    call_args = mock_exec.call_args[0][0]
    assert call_args == [
        "poetry",
        "config",
        "virtualenvs.in-project",
        "true",
        "--local",
    ]


@pytest.mark.integration
def test_should_get_venv_path_from_poetry(mocker, tmp_path: Path):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    poetry = PoetryManager()
    venv_path = poetry.get_venv_path(tmp_path)

    # get_venv_path returns (project_root / ".venv").resolve()
    assert venv_path == (tmp_path / ".venv").resolve()


@pytest.mark.integration
def test_should_get_python_path_from_pyenv(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
    )

    pyenv = PyenvManager()
    python_path = pyenv.get_python_path("3.12.3")

    assert python_path == Path("/home/user/.pyenv/versions/3.12.3/bin/python")
    assert mock_exec.called
    assert mock_exec.call_args[0][0] == ["pyenv", "prefix", "3.12.3"]


@pytest.mark.integration
def test_should_install_poetry_dependencies(mocker, tmp_path: Path):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    poetry = PoetryManager()
    poetry.install_dependencies(tmp_path)

    assert mock_exec.called
    call_args = mock_exec.call_args[0][0]
    assert call_args == ["poetry", "install", "--no-root"]
