"""Tests for bootstrap_env command – error handling and OS-specific display."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.commands.bootstrap_env import _display_success
from api_bootstrapper_cli.core.environment_service import EnvironmentSetupResult
from api_bootstrapper_cli.core.shell import ShellError
from tests.conftest import strip_ansi_codes


runner = CliRunner()

# ── Helper ──────────────────────────────────────────────────────────────────


def _make_result(
    venv_path: Path | None = None, has_poetry: bool = True
) -> EnvironmentSetupResult:
    return EnvironmentSetupResult(
        python_version="3.12.3",
        python_path=Path("/home/user/.pyenv/versions/3.12.3/bin/python"),
        venv_path=venv_path,
        venv_python=venv_path / "bin" / "python" if venv_path else None,
        editor_config_path=Path("/project/.vscode/settings.json"),
        has_poetry_project=has_poetry,
    )


# ── bootstrap_env command error-handling tests ───────────────────────────────


@patch("api_bootstrapper_cli.commands.bootstrap_env._create_bootstrap_service")
def test_should_exit_1_and_show_message_on_value_error(
    mock_factory: MagicMock, tmp_path: Path
):
    """bootstrap-env must catch ValueError and exit with code 1."""
    mock_service = MagicMock()
    mock_service.bootstrap.side_effect = ValueError("pyenv not found in PATH")
    mock_factory.return_value = mock_service

    result = runner.invoke(app, ["bootstrap-env", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output
    assert "pyenv not found" in output


@patch("api_bootstrapper_cli.commands.bootstrap_env._create_bootstrap_service")
def test_should_exit_1_and_show_message_on_runtime_error(
    mock_factory: MagicMock, tmp_path: Path
):
    """bootstrap-env must catch RuntimeError (domain errors) and exit code 1."""
    mock_service = MagicMock()
    mock_service.bootstrap.side_effect = RuntimeError(
        "[poetry] Falha ao instalar dependências: …"
    )
    mock_factory.return_value = mock_service

    result = runner.invoke(app, ["bootstrap-env", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output
    assert "Falha ao instalar" in output


@patch("api_bootstrapper_cli.commands.bootstrap_env._create_bootstrap_service")
def test_should_exit_1_and_show_message_on_shell_error(
    mock_factory: MagicMock, tmp_path: Path
):
    """bootstrap-env must catch ShellError and exit with code 1."""
    mock_service = MagicMock()
    mock_service.bootstrap.side_effect = ShellError("Command failed: poetry install")
    mock_factory.return_value = mock_service

    result = runner.invoke(app, ["bootstrap-env", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output


# ── _display_success OS-specific output tests ────────────────────────────────


def test_display_success_unix_plain_path(tmp_path: Path, capsys):
    """On Linux/macOS, shows source <venv>/bin/activate."""
    venv = tmp_path / ".venv"
    result = _make_result(venv_path=venv)

    with patch(
        "api_bootstrapper_cli.commands.bootstrap_env.platform.system",
        return_value="Linux",
    ):
        _display_success(result)

    captured = capsys.readouterr().out
    assert "source" in captured
    assert "/bin/activate" in captured


def test_display_success_unix_special_chars_path(tmp_path: Path, capsys):
    """On Linux/macOS with spaces in path, shows poetry env info alternative."""
    venv = tmp_path / "Área de Trabalho" / ".venv"
    result = _make_result(venv_path=venv)

    with patch(
        "api_bootstrapper_cli.commands.bootstrap_env.platform.system",
        return_value="Linux",
    ):
        _display_success(result)

    captured = capsys.readouterr().out
    assert "poetry env info --path" in captured


def test_display_success_windows(tmp_path: Path, capsys):
    """On Windows, shows Scripts\\activate path."""
    venv = tmp_path / ".venv"
    result = _make_result(venv_path=venv)

    with patch(
        "api_bootstrapper_cli.commands.bootstrap_env.platform.system",
        return_value="Windows",
    ):
        _display_success(result)

    captured = capsys.readouterr().out
    assert "Scripts" in captured or "activate" in captured


def test_display_success_without_venv(capsys):
    """When venv_path is None and has_poetry_project=False, no activation shown."""
    result = _make_result(venv_path=None, has_poetry=False)

    with patch(
        "api_bootstrapper_cli.commands.bootstrap_env.platform.system",
        return_value="Linux",
    ):
        _display_success(result)

    captured = capsys.readouterr().out
    assert "Environment ready" in captured
