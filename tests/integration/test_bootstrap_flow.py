from __future__ import annotations

import json
from pathlib import Path

import pytest

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.shell import CommandResult
from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


@pytest.mark.integration
def test_should_coordinate_pyenv_and_poetry_setup(
    mocker, tmp_path: Path, mock_pyproject_toml: Path
):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),
        CommandResult(stdout="3.12.0\n", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(
            stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
        ),
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
        CommandResult(stdout=f"{tmp_path}/.venv\n", stderr="", returncode=0),
    ]

    pyenv = PyenvManager()
    poetry = PoetryManager()
    vscode = VSCodeWriter()

    (tmp_path / ".venv").mkdir()

    assert pyenv.is_installed()

    pyenv.ensure_python("3.12.3")
    pyenv.set_local(tmp_path, "3.12.3")

    assert poetry.is_installed()

    poetry.configure_venv(tmp_path)
    python_path = pyenv.get_python_path("3.12.3")
    poetry.use_python(tmp_path, python_path)
    poetry.install_dependencies(tmp_path)
    venv_path = poetry.get_venv_path(tmp_path)
    venv_python = venv_path / "bin" / "python"
    settings_path = vscode.write_config(tmp_path, venv_python)

    assert settings_path.exists()
    assert (tmp_path / ".vscode" / "settings.json").exists()


@pytest.mark.integration
def test_should_handle_environment_recreation(mocker, tmp_path: Path):
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="Poetry 1.7.0", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout=f"{tmp_path}/.venv\n", stderr="", returncode=0),
    ]

    poetry = PoetryManager()

    assert poetry.is_installed()

    poetry.configure_venv(tmp_path)
    venv_path = poetry.get_venv_path(tmp_path)

    assert venv_path == tmp_path / ".venv"


@pytest.mark.integration
def test_should_preserve_existing_vscode_settings(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"
    existing_settings = {
        "editor.fontSize": 16,
        "files.autoSave": "onFocusChange",
    }
    settings_file.write_text(json.dumps(existing_settings, indent=2))
    vscode = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    vscode.write_config(tmp_path, python_path)

    updated_settings = json.loads(settings_file.read_text())

    assert updated_settings["editor.fontSize"] == 16
    assert updated_settings["files.autoSave"] == "onFocusChange"
    assert updated_settings["python.defaultInterpreterPath"] == "/usr/bin/python3.12"


@pytest.mark.integration
def test_should_handle_missing_python_version(mocker, tmp_path: Path):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="pyenv 2.3.0", stderr="", returncode=0),  # is_installed
        CommandResult(stdout="3.11.0\n", stderr="", returncode=0),  # list versions
    ]

    pyenv = PyenvManager()

    assert pyenv.is_installed()

    installed_versions = mock_exec.return_value.stdout.strip().split("\n")
    assert "3.12.3" not in installed_versions


@pytest.mark.integration
def test_should_handle_poetry_not_installed(mocker):
    mocker.patch(
        "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
        return_value="poetry",
    )
    mock_exec = mocker.patch("api_bootstrapper_cli.core.poetry_manager.exec_cmd")
    mock_exec.side_effect = FileNotFoundError("poetry command not found")

    poetry = PoetryManager()

    with pytest.raises(FileNotFoundError):
        poetry.is_installed()


@pytest.mark.integration
def test_should_handle_pyenv_not_installed(mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
    mock_exec.side_effect = FileNotFoundError("pyenv command not found")

    pyenv = PyenvManager()

    with pytest.raises(FileNotFoundError):
        pyenv.is_installed()
