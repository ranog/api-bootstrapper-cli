from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.shell import CommandResult, ShellError


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

    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["poetry", "install", "--no-root"]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_use_pyenv_path_when_available(mocker, tmp_path: Path):
    poetry_path = tmp_path / "poetry-executable"
    poetry_path.touch()
    poetry_path.chmod(0o755)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout=f"{poetry_path}\n", stderr="", returncode=0),
        CommandResult(stdout="Poetry version 1.7.0", stderr="", returncode=0),
    ]
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.Path.exists", return_value=True
    )

    manager = PoetryManager()
    result = manager.is_installed()

    assert result is True
    assert mock_exec.call_count == 2
    assert mock_exec.call_args_list[0][0][0] == ["pyenv", "which", "poetry"]
    assert mock_exec.call_args_list[1][0][0] == [str(poetry_path), "--version"]


def test_should_search_path_when_pyenv_fails(mocker, tmp_path: Path):
    poetry_path = tmp_path / "bin" / "poetry"
    poetry_path.parent.mkdir(parents=True)
    poetry_path.touch()
    poetry_path.chmod(0o755)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = [
        FileNotFoundError("pyenv not found"),
        CommandResult(stdout="Poetry version 1.7.0", stderr="", returncode=0),
    ]

    mock_env = mocker.patch("api_bootstrapper_cli.core.poetry_manager.os.environ")
    mock_env.copy.return_value = {"PATH": str(poetry_path.parent)}
    mock_env.get.return_value = str(poetry_path.parent)

    manager = PoetryManager()
    result = manager.is_installed()

    assert result is True
    assert mock_exec.call_count == 2
    assert mock_exec.call_args_list[1][0][0] == [str(poetry_path), "--version"]


def test_should_fallback_to_poetry_string_command(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = [
        FileNotFoundError("pyenv not found"),
        CommandResult(stdout="Poetry version 1.7.0", stderr="", returncode=0),
    ]

    mock_env = mocker.patch("api_bootstrapper_cli.core.poetry_manager.os.environ")
    mock_env.copy.return_value = {"PATH": ""}
    mock_env.get.return_value = ""

    manager = PoetryManager()
    result = manager.is_installed()

    assert result is True
    assert mock_exec.call_count == 2
    assert mock_exec.call_args_list[1][0][0] == ["poetry", "--version"]


def test_should_raise_runtime_error_when_configure_venv_fails(mocker, tmp_path: Path):
    """configure_venv should raise RuntimeError (not raw ShellError) on failure."""

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = ShellError("poetry config failed")
    manager = PoetryManager()

    with pytest.raises(
        RuntimeError, match=r"\[poetry\].*Falha ao configurar virtualenv"
    ):
        manager.configure_venv(tmp_path)


def test_should_raise_runtime_error_when_use_python_fails(mocker, tmp_path: Path):
    """use_python should raise RuntimeError on ShellError."""

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = ShellError("env use failed")
    manager = PoetryManager()

    with pytest.raises(RuntimeError, match=r"\[poetry\].*Falha ao vincular Python"):
        manager.use_python(tmp_path, Path("/usr/bin/python3.12"))


def test_should_raise_runtime_error_when_install_dependencies_fails(
    mocker, tmp_path: Path
):
    """install_dependencies should raise RuntimeError on ShellError."""

    (tmp_path / ".venv").mkdir()
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = ShellError("install failed")
    manager = PoetryManager()

    with pytest.raises(RuntimeError, match=r"\[poetry\].*Falha ao instalar depend"):
        manager.install_dependencies(tmp_path)


def test_ensure_venv_is_noop_when_venv_exists(mocker, tmp_path: Path):
    """ensure_venv should not call poetry when .venv already exists."""
    (tmp_path / ".venv").mkdir()
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    manager = PoetryManager()

    manager.ensure_venv(tmp_path)

    mock_exec.assert_not_called()


def test_ensure_venv_raises_runtime_error_when_creation_fails(mocker, tmp_path: Path):
    """ensure_venv should raise RuntimeError when poetry fails to create venv."""

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = ShellError("creation failed")
    manager = PoetryManager()

    with pytest.raises(RuntimeError, match=r"\[poetry\].*Falha ao criar virtualenv"):
        manager.ensure_venv(tmp_path)
