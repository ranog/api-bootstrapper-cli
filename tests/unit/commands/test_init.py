from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from tests.conftest import strip_ansi_codes


runner = CliRunner()


def test_should_show_init_help():
    result = runner.invoke(app, ["init", "--help"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Initialize a complete Python project" in output
    assert "--python" in output
    assert "--path" in output


def test_should_show_command_in_help():
    result = runner.invoke(app, ["--help"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "init" in output


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_call_bootstrap_and_precommit(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )

    assert result.exit_code == 0
    mock_bootstrap.assert_called_once()
    mock_precommit.assert_called_once()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_pass_python_version_to_bootstrap(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(app, ["init", "--python", "3.13.9", "--path", str(tmp_path)])

    call_kwargs = mock_bootstrap.call_args.kwargs
    assert call_kwargs["python_version"] == "3.13.9"


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_pass_path_to_both_commands(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(app, ["init", "--python", "3.12.12", "--path", str(tmp_path)])

    bootstrap_kwargs = mock_bootstrap.call_args.kwargs
    precommit_kwargs = mock_precommit.call_args.kwargs

    assert bootstrap_kwargs["path"] == tmp_path
    assert precommit_kwargs["path"] == tmp_path


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_pass_install_flag_to_bootstrap(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path), "--no-install"]
    )

    call_kwargs = mock_bootstrap.call_args.kwargs
    assert call_kwargs["install"] is False


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_show_success_message(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Project initialized successfully" in output
    assert "Next steps:" in output


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_show_progress_steps(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert "Step 1/2" in output
    assert "Setting up Python environment" in output
    assert "Step 2/2" in output
    assert "Configuring pre-commit hooks" in output


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_handle_bootstrap_failure(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    mock_bootstrap.side_effect = Exception("Bootstrap failed")

    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Initialization failed" in output
    mock_precommit.assert_not_called()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_handle_precommit_failure(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    mock_precommit.side_effect = Exception("Precommit failed")

    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Initialization failed" in output


def test_should_require_python_argument():
    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_precommit")
def test_should_use_current_directory_by_default(
    mock_precommit: MagicMock, mock_bootstrap: MagicMock
):
    runner.invoke(app, ["init", "--python", "3.12.12"])

    bootstrap_kwargs = mock_bootstrap.call_args.kwargs
    precommit_kwargs = mock_precommit.call_args.kwargs

    assert bootstrap_kwargs["path"].is_absolute()
    assert precommit_kwargs["path"].is_absolute()
