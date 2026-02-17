from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.core.shell import CommandResult, ShellError


runner = CliRunner()


@pytest.mark.e2e
def test_should_show_error_when_pyenv_not_installed(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = ShellError("pyenv not found")
    
    result = runner.invoke(
        app,
        [
            "bootstrap-env",
            "--path",
            str(tmp_path),
            "--python",
            "3.12.3",
            "--no-install",
        ],
    )

    assert result.exit_code != 0
    output = result.stdout + (result.stderr if hasattr(result, "stderr") else "")
    assert "pyenv" in output.lower() or result.exception is not None


@pytest.mark.e2e    
def test_should_execute_full_bootstrap_workflow(
    mocker, tmp_path: Path, mock_pyproject_toml: Path
):
    mock_pyenv_exec = mocker.patch(
        "api_bootstrapper_cli.core.pyenv_manager.exec_cmd"
    )
    project_path = mock_pyproject_toml.parent
    mock_pyenv_exec.side_effect = [
        CommandResult(
            stdout="pyenv 2.3.0", stderr="", returncode=0
        ),  # is_installed
        CommandResult(stdout="3.12.3\n", stderr="", returncode=0),  # versions
        CommandResult(stdout="", stderr="", returncode=0),  # set_local
        CommandResult(
            stdout=f"{project_path}/.venv/bin/python\n", stderr="", returncode=0
        ),  # python_path
    ]
    mock_poetry_exec = mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.exec_cmd"
    )
    mock_poetry_exec.side_effect = [
        CommandResult(
            stdout="Poetry 1.7.0", stderr="", returncode=0
        ),  # ensure_installed
        CommandResult(stdout="", stderr="", returncode=0),  # set_in_project_venv
        CommandResult(stdout="", stderr="", returncode=0),  # env_use
        CommandResult(stdout="", stderr="", returncode=0),  # install
        CommandResult(
            stdout=f"{project_path}/.venv\n", stderr="", returncode=0
        ),  # env_path
    ]

    result = runner.invoke(
        app,
        ["bootstrap-env", "--path", str(project_path), "--python", "3.12.3"],
    )

    assert result.exit_code == 0
    assert "pyenv" in result.stdout
    assert "poetry" in result.stdout
    assert "vscode" in result.stdout
    vscode_settings = project_path / ".vscode" / "settings.json"
    assert vscode_settings.exists()


@pytest.mark.e2e
def test_should_skip_install_when_flag_is_set(
    mocker, tmp_path: Path, mock_pyproject_toml: Path
):
    project_path = mock_pyproject_toml.parent
    mock_pyenv_exec = mocker.patch(
        "api_bootstrapper_cli.core.pyenv_manager.exec_cmd"
    )
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),
        CommandResult(stdout="3.12.3\n", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(
            stdout=f"{project_path}/.venv/bin/python\n", stderr="", returncode=0
        ),
    ]
    # Mock poetry commands
    mock_poetry_exec = mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.exec_cmd"
    )
    mock_poetry_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout=f"{project_path}/.venv\n", stderr="", returncode=0),
    ]

    result = runner.invoke(
        app,
        [
            "bootstrap-env",
            "--path",
            str(project_path),
            "--python",
            "3.12.3",
            "--no-install",
        ],
    )

    assert result.exit_code == 0
    # Verify poetry install was not called
    install_calls = [
        call
        for call in mock_poetry_exec.call_args_list
        if call[0][0] == ["poetry", "install"]
    ]
    assert len(install_calls) == 0


@pytest.mark.e2e
def test_should_skip_poetry_when_no_pyproject_toml(
    mocker, tmp_path: Path
):
    # No pyproject.toml file created
    pyproject_file = tmp_path / "pyproject.toml"
    assert not pyproject_file.exists()
    # Mock pyenv commands
    mock_pyenv_exec = mocker.patch(
        "api_bootstrapper_cli.core.pyenv_manager.exec_cmd"
    )
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),  # is_installed
        CommandResult(stdout="3.12.12\n", stderr="", returncode=0),  # versions
        CommandResult(stdout="", stderr="", returncode=0),  # set_local
        CommandResult(
            stdout=f"{tmp_path}/.pyenv/versions/3.12.12/bin/python\n",
            stderr="",
            returncode=0,
        ),  # python_path
    ]
    # Mock poetry commands - should NOT be called
    mock_poetry_exec = mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.exec_cmd"
    )

    result = runner.invoke(app, ["bootstrap-env", "--path", str(tmp_path)])
    
    assert result.exit_code == 0
    assert "warning" in result.stdout.lower()
    assert "no pyproject.toml found" in result.stdout
    assert "skipping poetry setup" in result.stdout
    
    # Verify Poetry commands were NOT called
    assert mock_poetry_exec.call_count == 0
    
    # Verify VSCode settings were still created
    vscode_settings = tmp_path / ".vscode" / "settings.json"
    assert vscode_settings.exists()


@pytest.mark.e2e
def test_should_show_todo_message():
    result = runner.invoke(app, ["add-alembic"])
    
    assert result.exit_code == 0
    assert "TODO" in result.stdout


@pytest.mark.e2e
def test_should_list_all_commands():
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "bootstrap-env" in result.stdout
    assert "add-alembic" in result.stdout


@pytest.mark.e2e
def test_should_show_bootstrap_env_options():
    result = runner.invoke(app, ["bootstrap-env", "--help"])

    assert result.exit_code == 0
    assert "--path" in result.stdout
    assert "--python" in result.stdout
    assert "--install" in result.stdout
