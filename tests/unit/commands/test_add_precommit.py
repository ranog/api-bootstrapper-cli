from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from tests.conftest import strip_ansi_codes


runner = CliRunner()


def test_should_show_add_pre_commit_help():
    result = runner.invoke(app, ["add-pre-commit", "--help"])
    output = strip_ansi_codes(text=result.stdout)

    assert result.exit_code == 0
    assert "Add pre-commit configuration" in output
    assert "--path" in output


def test_should_accept_default_path():
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        mock_instance.create_config.return_value = (
            Path(".pre-commit-config.yaml"),
            {"ruff": "0.15.1", "commitizen": "4.13.8"},
            False,
        )
        mock_manager.return_value = mock_instance

        runner.invoke(app, ["add-pre-commit"])

        mock_instance.create_config.assert_called_once()


def test_should_accept_custom_path():
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        test_path = Path("/tmp/test-project")
        mock_instance.create_config.return_value = (
            test_path / ".pre-commit-config.yaml",
            {"ruff": "0.15.1"},
            False,
        )
        mock_manager.return_value = mock_instance

        runner.invoke(app, ["add-pre-commit", "--path", str(test_path)])

        assert mock_instance.create_config.called


def test_should_display_success_message(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (
            config_path,
            {"ruff": "0.15.1", "commitizen": "4.13.8"},
            False,
        )
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Pre-commit configured!" in output
        assert ".pre-commit-config.yaml" in output


def test_should_display_installed_versions(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (
            config_path,
            {"ruff": "0.16.0", "commitizen": "4.14.0"},
            False,
        )
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Installed versions:" in output
        assert "ruff" in output
        assert "0.16.0" in output
        assert "commitizen" in output
        assert "4.14.0" in output


def test_should_display_existing_config_message(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (
            config_path,
            {"ruff": "0.16.0", "commitizen": "4.14.0"},
            True,  # Config already existed
        )
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Pre-commit config already exists" in output
        assert "Existing file preserved" in output
        assert "Dependencies and hooks have been updated" in output


def test_should_handle_empty_versions_dict(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (config_path, {}, False)
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Pre-commit configured!" in output


def test_should_show_hooks_installed_message_with_git(tmp_path: Path):
    git_hooks = tmp_path / ".git" / "hooks"
    git_hooks.mkdir(parents=True)

    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (
            config_path,
            {"ruff": "0.15.1"},
            False,
        )
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Hooks installed!" in output
        assert "will now run automatically" in output


def test_should_show_warning_without_git(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        config_path = tmp_path / ".pre-commit-config.yaml"
        config_path.touch()
        mock_instance.create_config.return_value = (
            config_path,
            {"ruff": "0.15.1"},
            False,
        )
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 0
        assert "Not a git repository" in output
        assert "poetry run pre-commit install" in output


def test_should_handle_value_error(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        mock_instance.create_config.side_effect = ValueError("Project root invalid")
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 1
        assert "Error:" in output
        assert "Project root invalid" in output


def test_should_handle_unexpected_error(tmp_path: Path):
    with patch(
        "api_bootstrapper_cli.commands.add_pre_commit.PreCommitManager"
    ) as mock_manager:
        mock_instance = MagicMock()
        mock_instance.create_config.side_effect = RuntimeError("Unexpected error")
        mock_manager.return_value = mock_instance

        result = runner.invoke(app, ["add-pre-commit", "--path", str(tmp_path)])
        output = strip_ansi_codes(text=result.stdout)

        assert result.exit_code == 1
        assert "Unexpected error:" in output
        assert "Unexpected error" in output


def test_should_show_command_in_help():
    result = runner.invoke(app, ["--help"])
    output = strip_ansi_codes(text=result.stdout)

    assert result.exit_code == 0
    assert "add-pre-commit" in output


def test_should_show_command_description_in_help():
    result = runner.invoke(app, ["add-pre-commit", "--help"])
    output = strip_ansi_codes(text=result.stdout)

    assert result.exit_code == 0
    assert "Ruff" in output
    assert "Commitizen" in output
