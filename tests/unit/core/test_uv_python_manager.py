"""Unit tests for UvPythonManager."""

from __future__ import annotations

import pytest

from api_bootstrapper_cli.core.shell import CommandResult, ShellError
from api_bootstrapper_cli.core.uv_python_manager import UvPythonManager


# ---------------------------------------------------------------------------
# is_installed
# ---------------------------------------------------------------------------


def test_should_detect_uv_is_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="uv 0.5.0", stderr="", returncode=0)

    manager = UvPythonManager()

    assert manager.is_installed() is True
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "--version"]
    assert call_args[1]["check"] is True


def test_should_detect_uv_is_not_installed_when_shell_error(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.side_effect = ShellError("uv not found")

    assert UvPythonManager().is_installed() is False


def test_should_detect_uv_is_not_installed_when_file_not_found(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.side_effect = FileNotFoundError()

    assert UvPythonManager().is_installed() is False


# ---------------------------------------------------------------------------
# ensure_python
# ---------------------------------------------------------------------------


def test_should_install_python_with_uv(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    UvPythonManager().ensure_python("3.12.0")

    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "python", "install", "3.12.0"]
    assert call_args[1]["check"] is True


def test_should_raise_runtime_error_when_python_install_fails(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.side_effect = ShellError("download failed")

    with pytest.raises(RuntimeError, match="3.12.0"):
        UvPythonManager().ensure_python("3.12.0")


# ---------------------------------------------------------------------------
# set_local
# ---------------------------------------------------------------------------


def test_should_pin_python_version_locally(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    UvPythonManager().set_local(tmp_path, "3.12.0")

    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "python", "pin", "3.12.0"]
    assert call_args[1]["cwd"] == str(tmp_path)
    assert call_args[1]["check"] is True


def test_should_raise_runtime_error_when_set_local_fails(mocker, tmp_path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.side_effect = ShellError("pinning failed")

    with pytest.raises(RuntimeError, match="3.12.0"):
        UvPythonManager().set_local(tmp_path, "3.12.0")


# ---------------------------------------------------------------------------
# get_python_path
# ---------------------------------------------------------------------------


def test_should_return_python_path_from_uv(mocker, tmp_path):
    python_bin = tmp_path / "python3"
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.return_value = CommandResult(
        stdout=str(python_bin) + "\n", stderr="", returncode=0
    )

    result = UvPythonManager().get_python_path("3.12.0")

    assert result == python_bin
    call_args = mock_exec.call_args
    assert call_args[0][0] == ["uv", "python", "find", "3.12.0"]


def test_should_raise_runtime_error_when_python_path_not_found(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")
    mock_exec.side_effect = ShellError("not found")

    with pytest.raises(RuntimeError, match="3.12.0"):
        UvPythonManager().get_python_path("3.12.0")


# ---------------------------------------------------------------------------
# install_pip_packages (no-op)
# ---------------------------------------------------------------------------


def test_install_pip_packages_is_noop(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.uv_python_manager.exec_cmd")

    UvPythonManager().install_pip_packages("3.12.0", ["pip", "setuptools"])

    mock_exec.assert_not_called()


# ---------------------------------------------------------------------------
# name attribute
# ---------------------------------------------------------------------------


def test_manager_name_is_uv():
    assert UvPythonManager().name == "uv"
