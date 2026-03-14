from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from tests.conftest import strip_ansi_codes


runner = CliRunner()


@pytest.fixture(autouse=True)
def cleanup_generated_dockerfile():
    project_root = Path.cwd()
    generated_paths = [
        project_root / "Dockerfile",
        project_root / "docker-compose.yml",
        project_root / "src" / "main.py",
        project_root / "src" / "database.py",
        project_root / "src" / "models.py",
        project_root / "src" / "schemas.py",
        project_root / "tests" / "__init__.py",
        project_root / "tests" / "unit" / "__init__.py",
        project_root / "tests" / "integration" / "__init__.py",
        project_root / "tests" / "integration" / "test_api_flow.py",
        project_root / "tests" / "e2e" / "__init__.py",
    ]
    existed_before = {path: path.exists() for path in generated_paths}

    yield

    for path in generated_paths:
        if not existed_before[path] and path.exists():
            path.unlink()


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
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_call_bootstrap_and_pre_commit(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )

    assert result.exit_code == 0
    mock_bootstrap.assert_called_once()
    mock_pre_commit.assert_called_once()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_pass_python_version_to_bootstrap(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(app, ["init", "--python", "3.13.9", "--path", str(tmp_path)])

    call_kwargs = mock_bootstrap.call_args.kwargs
    assert call_kwargs["python_version"] == "3.13.9"


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_pass_path_to_both_commands(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(app, ["init", "--python", "3.12.12", "--path", str(tmp_path)])

    bootstrap_kwargs = mock_bootstrap.call_args.kwargs
    pre_commit_kwargs = mock_pre_commit.call_args.kwargs

    assert bootstrap_kwargs["path"] == tmp_path
    assert pre_commit_kwargs["path"] == tmp_path


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_pass_install_flag_to_bootstrap(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path), "--no-install"]
    )

    call_kwargs = mock_bootstrap.call_args.kwargs
    assert call_kwargs["install"] is False


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_show_success_message(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Project initialized successfully" in output
    assert "Next steps:" in output


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_create_makefile_during_init(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )

    assert result.exit_code == 0
    assert (tmp_path / "Makefile").exists()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_create_docker_compose_during_init(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )

    assert result.exit_code == 0
    assert (tmp_path / "docker-compose.yml").exists()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_show_progress_steps(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert "Step 1/6" in output
    assert "Creating project structure" in output
    assert "Step 2/6" in output
    assert "Setting up Python environment" in output
    assert "Step 3/6" in output
    assert "Creating Dockerfile" in output
    assert "Step 4/6" in output
    assert "Setting up environment file" in output
    assert "Step 5/6" in output
    assert "Checking .gitignore" in output
    assert "Step 6/6" in output
    assert "Configuring pre-commit hooks" in output


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_handle_bootstrap_failure(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    mock_bootstrap.side_effect = Exception("Bootstrap failed")

    result = runner.invoke(
        app, ["init", "--python", "3.12.12", "--path", str(tmp_path)]
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Initialization failed" in output
    mock_pre_commit.assert_not_called()


@patch("api_bootstrapper_cli.commands.init.bootstrap_env")
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_handle_pre_commit_failure(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock, tmp_path: Path
):
    mock_pre_commit.side_effect = Exception("Pre-commit failed")

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
@patch("api_bootstrapper_cli.commands.init.add_pre_commit")
def test_should_use_current_directory_by_default(
    mock_pre_commit: MagicMock, mock_bootstrap: MagicMock
):
    runner.invoke(app, ["init", "--python", "3.12.12"])

    bootstrap_kwargs = mock_bootstrap.call_args.kwargs
    pre_commit_kwargs = mock_pre_commit.call_args.kwargs

    assert bootstrap_kwargs["path"].is_absolute()
    assert pre_commit_kwargs["path"].is_absolute()
