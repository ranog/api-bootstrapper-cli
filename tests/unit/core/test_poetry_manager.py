from __future__ import annotations

from pathlib import Path

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.shell import CommandResult


def test_should_verify_poetry_is_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="Poetry version 1.7.0", stderr="", returncode=0
    )
    manager = PoetryManager()

    manager.ensure_installed()
    
    mock_exec.assert_called_once_with(["poetry", "--version"], check=True)


def test_should_configure_in_project_venv(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    manager = PoetryManager()
    
    manager.set_in_project_venv(tmp_path, enabled=True)
    
    mock_exec.assert_called_once_with(
        ["poetry", "config", "virtualenvs.in-project", "true", "--local"],
        cwd=str(tmp_path),
        check=True,
    )


def test_should_disable_in_project_venv(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    manager = PoetryManager()

    manager.set_in_project_venv(tmp_path, enabled=False)
    
    call_args = mock_exec.call_args[0][0]
    assert "false" in call_args

    
def test_should_use_specific_python_version(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    python_path = Path("/usr/bin/python3.12")
    manager = PoetryManager()

    manager.env_use(tmp_path, python_path)
    
    mock_exec.assert_called_once_with(
        ["poetry", "env", "use", str(python_path)],
        cwd=str(tmp_path),
        check=True,
    )


def test_should_get_virtualenv_path(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout=f"{tmp_path}/.venv\n",
        stderr="",
        returncode=0,
    )
    manager = PoetryManager()
    
    venv_path = manager.env_path(tmp_path)
    
    assert venv_path == tmp_path / ".venv"


def test_should_install_dependencies(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="Installing dependencies...", stderr="", returncode=0
    )
    manager = PoetryManager()
    
    manager.install(tmp_path)
    
    mock_exec.assert_called_once_with(
        ["poetry", "install"],
        cwd=str(tmp_path),
        check=True,
    )
