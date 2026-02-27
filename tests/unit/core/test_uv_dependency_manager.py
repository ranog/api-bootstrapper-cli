"""Unit tests for UvDependencyManager."""

from __future__ import annotations

import pytest

from api_bootstrapper_cli.core.shell import CommandResult, ShellError
from api_bootstrapper_cli.core.uv_dependency_manager import UvDependencyManager


# ---------------------------------------------------------------------------
# is_installed
# ---------------------------------------------------------------------------


def test_should_detect_uv_is_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="uv 0.5.0", stderr="", returncode=0)

    assert UvDependencyManager().is_installed() is True
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "--version"]
    assert call_args[1]["check"] is True


def test_should_detect_uv_not_installed_when_shell_error(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.side_effect = ShellError("uv not found")

    assert UvDependencyManager().is_installed() is False


def test_should_detect_uv_not_installed_when_file_not_found(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.side_effect = FileNotFoundError()

    assert UvDependencyManager().is_installed() is False


# ---------------------------------------------------------------------------
# configure_venv (no-op)
# ---------------------------------------------------------------------------


def test_configure_venv_is_noop(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")

    UvDependencyManager().configure_venv(tmp_path)

    mock_exec.assert_not_called()


# ---------------------------------------------------------------------------
# use_python
# ---------------------------------------------------------------------------


def test_should_create_venv_with_specified_python(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    python_path = tmp_path / "python3"
    UvDependencyManager().use_python(tmp_path, python_path)

    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "venv", "--python", str(python_path)]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_raise_runtime_error_when_use_python_fails(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.side_effect = ShellError("venv failed")

    with pytest.raises(RuntimeError, match=r"\[uv\]"):
        UvDependencyManager().use_python(tmp_path, tmp_path / "python3")


# ---------------------------------------------------------------------------
# ensure_venv
# ---------------------------------------------------------------------------


def test_should_create_venv_when_not_present(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    UvDependencyManager().ensure_venv(tmp_path)

    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "venv"]
    assert call_args[1]["cwd"] == str(tmp_path)


def test_should_skip_venv_creation_when_already_present(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()

    UvDependencyManager().ensure_venv(tmp_path)

    mock_exec.assert_not_called()


def test_should_raise_runtime_error_when_ensure_venv_fails(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.side_effect = ShellError("venv failed")

    with pytest.raises(RuntimeError, match=r"\[uv\]"):
        UvDependencyManager().ensure_venv(tmp_path)


# ---------------------------------------------------------------------------
# install_dependencies
# ---------------------------------------------------------------------------


def test_should_run_uv_sync_to_install_dependencies(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)
    # pre-create .venv so ensure_venv is a no-op
    (tmp_path / ".venv").mkdir()

    UvDependencyManager().install_dependencies(tmp_path)

    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "sync"]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_raise_runtime_error_when_sync_fails(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_dependency_manager.exec_cmd")
    mock_exec.side_effect = ShellError("lock file missing")
    (tmp_path / ".venv").mkdir()

    with pytest.raises(RuntimeError, match=r"\[uv\]"):
        UvDependencyManager().install_dependencies(tmp_path)


# ---------------------------------------------------------------------------
# get_venv_path / get_venv_python
# ---------------------------------------------------------------------------


def test_should_return_venv_path(tmp_path):
    result = UvDependencyManager().get_venv_path(tmp_path)
    assert result == (tmp_path / ".venv").resolve()


def test_should_return_venv_python_on_unix(mocker, tmp_path):
    mocker.patch("platform.system", return_value="Linux")

    result = UvDependencyManager().get_venv_python(tmp_path)

    assert result == (tmp_path / ".venv").resolve() / "bin" / "python"


def test_should_return_venv_python_on_windows(mocker, tmp_path):
    mocker.patch("platform.system", return_value="Windows")

    result = UvDependencyManager().get_venv_python(tmp_path)

    assert result == (tmp_path / ".venv").resolve() / "Scripts" / "python.exe"


# ---------------------------------------------------------------------------
# name attribute
# ---------------------------------------------------------------------------


def test_manager_name_is_uv():
    assert UvDependencyManager().name == "uv"
