from __future__ import annotations

import json
from pathlib import Path

from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.shell import CommandResult
from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


class TestBootstrapFlow:
    def test_should_coordinate_pyenv_and_poetry_setup(
        self, mocker, tmp_path: Path, mock_pyproject_toml: Path
    ):
        # Mock all shell commands
        mock_exec = mocker.patch("api_bootstrapper_cli.core.pyenv_manager.exec_cmd")
        mock_exec.side_effect = [
            CommandResult(
                stdout="pyenv 2.3.0", stderr="", returncode=0
            ),  # is_installed
            CommandResult(stdout="3.12.0\n", stderr="", returncode=0),  # versions
            CommandResult(stdout="", stderr="", returncode=0),  # install
            CommandResult(stdout="", stderr="", returncode=0),  # set_local
            CommandResult(
                stdout="/home/user/.pyenv/versions/3.12.3\n", stderr="", returncode=0
            ),  # get_python_path (pyenv prefix)
        ]

        # Mock _get_poetry_cmd to bypass pyenv which poetry call
        mocker.patch(
            "api_bootstrapper_cli.core.poetry_manager.PoetryManager._get_poetry_cmd",
            return_value="poetry",
        )

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
                stdout=f"{tmp_path}/.venv\n", stderr="", returncode=0
            ),  # env_path
        ]

        # Execute the flow
        pyenv = PyenvManager()
        poetry = PoetryManager()
        vscode = VSCodeWriter()

        # Create a .venv file to simulate that it has already been created.
        (tmp_path / ".venv").mkdir()

        # Step 1: Ensure Python version
        assert pyenv.is_installed()
        pyenv.ensure_python("3.12.3")
        pyenv.set_local(tmp_path, "3.12.3")

        # Step 2: Configure Poetry
        assert poetry.is_installed()
        poetry.configure_venv(tmp_path)

        python_path = pyenv.get_python_path("3.12.3")
        poetry.use_python(tmp_path, python_path)
        poetry.install_dependencies(tmp_path)

        # Step 3: Configure VSCode
        venv_path = poetry.get_venv_path(tmp_path)
        venv_python = venv_path / "bin" / "python"
        settings_path = vscode.write_config(tmp_path, venv_python)

        # Assertions
        assert settings_path.exists()
        assert (tmp_path / ".vscode" / "settings.json").exists()

    def test_should_handle_environment_recreation(self, mocker, tmp_path: Path):
        # Setup existing .venv
        venv_dir = tmp_path / ".venv"
        venv_dir.mkdir()

        # Mock _get_poetry_cmd to bypass pyenv which poetry call
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

    def test_should_preserve_existing_vscode_settings(self, tmp_path: Path):
        # Create existing settings
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        settings_file = vscode_dir / "settings.json"

        existing_settings = {
            "editor.fontSize": 16,
            "files.autoSave": "onFocusChange",
        }
        settings_file.write_text(json.dumps(existing_settings, indent=2))

        # Write Python interpreter
        vscode = VSCodeWriter()
        python_path = Path("/usr/bin/python3.12")
        vscode.write_config(tmp_path, python_path)

        # Verify settings were merged
        updated_settings = json.loads(settings_file.read_text())
        assert updated_settings["editor.fontSize"] == 16
        assert updated_settings["files.autoSave"] == "onFocusChange"
        assert (
            updated_settings["python.defaultInterpreterPath"] == "/usr/bin/python3.12"
        )
