from __future__ import annotations

import subprocess
from unittest.mock import Mock

import pytest

from api_bootstrapper_cli.core.shell import CommandResult, ShellError, exec_cmd


def test_should_execute_simple_command_successfully(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = Mock(stdout="output", stderr="", returncode=0)

    result = exec_cmd(["echo", "test"])

    assert result.stdout == "output"
    assert result.stderr == ""
    assert result.returncode == 0
    mock_run.assert_called_once()


def test_should_pass_cwd_to_subprocess(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = Mock(stdout="", stderr="", returncode=0)

    exec_cmd(["ls"], cwd="/tmp")

    call_args = mock_run.call_args
    assert call_args.kwargs["cwd"] == "/tmp"


def test_should_raise_shell_error_on_failure(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.side_effect = subprocess.CalledProcessError(1, ["false"], stderr="error")

    with pytest.raises(ShellError, match="Command failed"):
        exec_cmd(["false"], check=True)


def test_should_not_raise_when_check_is_false(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = Mock(stdout="", stderr="error", returncode=1)

    result = exec_cmd(["false"], check=False)

    assert result.returncode == 1


def test_should_return_command_result_object(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = Mock(stdout="out", stderr="err", returncode=0)

    result = exec_cmd(["test"])

    assert isinstance(result, CommandResult)
    assert result.stdout == "out"
    assert result.stderr == "err"
    assert result.returncode == 0
