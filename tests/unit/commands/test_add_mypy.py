from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.core.mypy_manager import MypySetupResult
from api_bootstrapper_cli.core.protocols import ManagerChoice


runner = CliRunner()


def strip_ansi_codes(text: str) -> str:
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def test_should_show_add_mypy_help() -> None:
    result = runner.invoke(app, ["add-mypy", "--help"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Add mypy type-checking configuration" in output
    assert "--path" in output
    assert "--manager" in output


@patch("api_bootstrapper_cli.commands.add_mypy.MypyManager")
def test_should_configure_mypy_with_poetry_prefix(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = MypySetupResult(
        manager=ManagerChoice.pyenv,
        pyproject_path=tmp_path / "pyproject.toml",
        config_already_existed=False,
        version="1.19.1",
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(app, ["add-mypy", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Mypy configured!" in output
    assert "pyproject.toml" in output
    assert "1.19.1" in output
    assert "poetry run mypy src" in output
    mock_instance.setup.assert_called_once_with(tmp_path.resolve(), manager=None)


@patch("api_bootstrapper_cli.commands.add_mypy.MypyManager")
def test_should_show_existing_config_message(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = MypySetupResult(
        manager=ManagerChoice.pyenv,
        pyproject_path=tmp_path / "pyproject.toml",
        config_already_existed=True,
        version="1.19.1",
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(app, ["add-mypy", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Mypy config already exists" in output
    assert "Dependencies have been updated if needed" in output


@patch("api_bootstrapper_cli.commands.add_mypy.MypyManager")
def test_should_use_uv_prefix_when_manager_is_uv(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = MypySetupResult(
        manager=ManagerChoice.uv,
        pyproject_path=tmp_path / "pyproject.toml",
        config_already_existed=False,
        version="1.19.1",
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(
        app,
        ["add-mypy", "--path", str(tmp_path), "--manager", "uv"],
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "uv run mypy src" in output
    assert "poetry run mypy src" not in output
    mock_instance.setup.assert_called_once_with(
        tmp_path.resolve(),
        manager=ManagerChoice.uv,
    )


@patch("api_bootstrapper_cli.commands.add_mypy.MypyManager")
def test_should_handle_expected_errors(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.side_effect = RuntimeError("setup failed")
    mock_manager.return_value = mock_instance

    result = runner.invoke(app, ["add-mypy", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output
    assert "setup failed" in output
