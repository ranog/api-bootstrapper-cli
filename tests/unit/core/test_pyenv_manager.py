from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.shell import CommandResult, ShellError


def test_should_detect_pyenv_is_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="pyenv 2.3.0", stderr="", returncode=0
    )

    manager = PyenvManager()

    assert manager.is_installed() is True
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["pyenv", "--version"]
    assert call_args[1]["check"] is True


def test_should_detect_pyenv_is_not_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = ShellError("pyenv not found")

    manager = PyenvManager()

    assert manager.is_installed() is False


def test_should_list_installed_versions(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="3.11.0\n3.12.0\n3.12.3\n", stderr="", returncode=0
    )
    manager = PyenvManager()

    versions = manager._get_installed_versions()

    assert versions == {"3.11.0", "3.12.0", "3.12.3"}
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["pyenv", "versions", "--bare"]
    assert call_args[1]["check"] is True


def test_should_skip_install_if_version_exists(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="3.12.0\n", stderr="", returncode=0)
    manager = PyenvManager()

    manager.ensure_python("3.12.0")

    assert mock_exec.call_count == 1


def test_should_install_missing_version(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="", stderr="", returncode=0),  # versions()
        CommandResult(stdout="", stderr="", returncode=0),  # install
    ]
    manager = PyenvManager()

    manager.ensure_python("3.12.3")

    assert mock_exec.call_count == 2
    install_call = mock_exec.call_args_list[1]
    assert install_call[0][0] == ["pyenv", "install", "-s", "3.12.3"]


def test_should_set_local_version(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    manager = PyenvManager()

    manager.set_local(tmp_path, "3.12.3")

    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["pyenv", "local", "3.12.3"]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_get_python_path(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout="/home/user/.pyenv/versions/3.12.0\n",
        stderr="",
        returncode=0,
    )
    manager = PyenvManager()

    path = manager.get_python_path("3.12.0")

    assert path == Path("/home/user/.pyenv/versions/3.12.0/bin/python")
    assert mock_exec.call_count == 1
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["pyenv", "prefix", "3.12.0"]
    assert call_args[1]["check"] is True


# ── Error-handling tests ──────────────────────────────────────────────────────


def test_should_raise_runtime_error_when_ensure_python_fails(mocker):
    """ensure_python should raise RuntimeError (not ShellError) on failure."""
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="", stderr="", returncode=0),  # _get_installed_versions
        ShellError("build failed"),  # pyenv install
    ]
    manager = PyenvManager()

    with pytest.raises(RuntimeError, match=r"\[env\].*Falha ao instalar Python"):
        manager.ensure_python("3.12.99")


def test_should_raise_runtime_error_when_get_python_path_fails(mocker):
    """get_python_path should raise RuntimeError on ShellError."""
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = ShellError("version not found")
    manager = PyenvManager()

    with pytest.raises(
        RuntimeError, match=r"\[env\].*Falha ao obter caminho do Python"
    ):
        manager.get_python_path("3.12.99")


def test_should_raise_runtime_error_when_install_pip_packages_fails(mocker):
    """install_pip_packages should raise RuntimeError on ShellError."""
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    # First call is get_python_path → succeeds
    mock_exec.side_effect = [
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.0\n", stderr="", returncode=0
        ),
        ShellError("pip install failed"),
    ]
    manager = PyenvManager()

    with pytest.raises(RuntimeError, match=r"\[env\].*Falha ao instalar pacotes pip"):
        manager.install_pip_packages("3.12.0", ["pip", "wheel"])
