from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.core.shell import CommandResult, ShellError
from tests.conftest import strip_ansi_codes


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
    project_path = mock_pyproject_toml.parent
    # Create a .venv file to simulate that it has already been created.
    (project_path / ".venv").mkdir()

    mock_pyenv_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),
        CommandResult(stdout="3.12.3\n", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(stdout="", stderr="", returncode=0),
    ]

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    mock_poetry_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_poetry_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),  # is_installed
        CommandResult(stdout="", stderr="", returncode=0),  # configure_venv
        CommandResult(stdout="", stderr="", returncode=0),  # use_python
        CommandResult(stdout="", stderr="", returncode=0),  # install_dependencies
        CommandResult(
            stdout=f"{project_path}/.venv\n", stderr="", returncode=0
        ),  # get_venv_path (first call)
        CommandResult(
            stdout=f"{project_path}/.venv\n", stderr="", returncode=0
        ),  # get_venv_path (second call in get_venv_python)
    ]

    result = runner.invoke(
        app,
        ["bootstrap-env", "--path", str(project_path), "--python", "3.12.3"],
    )

    assert result.exit_code == 0
    assert "Python" in result.stdout
    assert "Poetry" in result.stdout
    assert "VSCode" in result.stdout
    vscode_settings = project_path / ".vscode" / "settings.json"
    assert vscode_settings.exists()


@pytest.mark.e2e
def test_should_skip_install_when_flag_is_set(
    mocker, tmp_path: Path, mock_pyproject_toml: Path
):
    project_path = mock_pyproject_toml.parent
    # Create a .venv file to simulate that it has already been created.
    (project_path / ".venv").mkdir()

    mock_pyenv_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),  # is_installed
        CommandResult(
            stdout="3.12.3\n", stderr="", returncode=0
        ),  # _get_installed_versions
        CommandResult(stdout="", stderr="", returncode=0),  # set_local
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),  # get_python_path (pyenv prefix)
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),  # get_python_path (in install_pip_packages)
        CommandResult(
            stdout="", stderr="", returncode=0
        ),  # install_pip_packages (pip install)
    ]

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    mock_poetry_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_poetry_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),  # is_installed
        CommandResult(stdout="", stderr="", returncode=0),  # configure_venv
        CommandResult(stdout="", stderr="", returncode=0),  # use_python
        CommandResult(
            stdout=f"{project_path}/.venv\n", stderr="", returncode=0
        ),  # get_venv_path (first)
        CommandResult(
            stdout=f"{project_path}/.venv\n", stderr="", returncode=0
        ),  # get_venv_path (second)
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
    install_calls = [
        call
        for call in mock_poetry_exec.call_args_list
        if call[0][0] == ["poetry", "install", "--no-root"]
    ]
    assert len(install_calls) == 0


@pytest.mark.e2e
def test_should_create_minimal_pyproject_when_missing(mocker, tmp_path: Path):
    pyproject_file = tmp_path / "pyproject.toml"
    assert not pyproject_file.exists()

    mock_pyenv_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),  # is_installed
        CommandResult(stdout="3.12.12\n", stderr="", returncode=0),  # versions
        CommandResult(stdout="", stderr="", returncode=0),  # set_local
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.12\n",
            stderr="",
            returncode=0,
        ),  # get_python_path (pyenv prefix)
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.12\n",
            stderr="",
            returncode=0,
        ),  # get_python_path (in install_pip_packages)
        CommandResult(
            stdout="", stderr="", returncode=0
        ),  # install_pip_packages (pip install)
    ]

    # Mock _get_poetry_cmd to bypass pyenv which poetry call
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    mock_poetry_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_poetry_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    result = runner.invoke(app, ["bootstrap-env", "--path", str(tmp_path)])

    assert result.exit_code == 0

    assert pyproject_file.exists()
    assert "Creating minimal pyproject.toml" in result.stdout
    assert "Created" in result.stdout

    assert mock_poetry_exec.call_count > 0

    vscode_settings = tmp_path / ".vscode" / "settings.json"
    assert vscode_settings.exists()


@pytest.mark.e2e
def test_should_show_poetry_command_for_normal_path(mocker, tmp_path: Path):
    project_path = tmp_path / "test_project"
    project_path.mkdir()
    (project_path / ".venv").mkdir()
    (project_path / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "test"\nversion = "1.0.0"'
    )

    mock_pyenv_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),
        CommandResult(stdout="3.12.3\n", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(stdout="", stderr="", returncode=0),
    ]

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    mock_poetry_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_poetry_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout=f"{project_path}/.venv\n", stderr="", returncode=0),
        CommandResult(stdout=f"{project_path}/.venv\n", stderr="", returncode=0),
    ]

    result = runner.invoke(
        app,
        ["bootstrap-env", "--path", str(project_path), "--python", "3.12.3"],
    )

    assert result.exit_code == 0

    output = strip_ansi_codes(result.stdout)
    output_normalized = " ".join(output.split())

    assert "source" in output_normalized
    assert "bin/activate" in output_normalized
    assert "source $(poetry env info --path)/bin/activate" in output_normalized
    assert "# Or use:" in output_normalized


@pytest.mark.e2e
def test_should_prioritize_poetry_command_for_special_chars_path(
    mocker, tmp_path: Path
):
    project_path = tmp_path / "Área de trabalho" / "my project"
    project_path.mkdir(parents=True)
    (project_path / ".venv").mkdir()
    (project_path / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "test"\nversion = "1.0.0"'
    )

    mock_pyenv_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_pyenv_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),
        CommandResult(stdout="3.12.3\n", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
        CommandResult(stdout="", stderr="", returncode=0),
    ]

    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )

    mock_poetry_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_poetry_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout=f"{project_path}/.venv\n", stderr="", returncode=0),
        CommandResult(stdout=f"{project_path}/.venv\n", stderr="", returncode=0),
    ]

    result = runner.invoke(
        app,
        ["bootstrap-env", "--path", str(project_path), "--python", "3.12.3"],
    )

    assert result.exit_code == 0

    output_lines = result.stdout.split("\n")
    activate_section_start = None

    for i, line in enumerate(output_lines):
        if "To activate" in line:
            activate_section_start = i
            break

    assert activate_section_start is not None, "Activation message not found"
    assert (
        "source $(poetry env info --path)/bin/activate"
        in output_lines[activate_section_start + 1]
    )
    assert "if path has spaces/accents" in result.stdout
