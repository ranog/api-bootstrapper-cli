from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.core.alembic_manager import AlembicSetupResult
from api_bootstrapper_cli.core.protocols import ManagerChoice


runner = CliRunner()


def strip_ansi_codes(text: str) -> str:
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def test_should_show_add_alembic_help() -> None:
    result = runner.invoke(app, ["add-alembic", "--help"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Add Alembic database migrations support" in output
    assert "--path" in output
    assert "--manager" in output
    assert "--with-db" in output
    assert "--create-initial-items" in output
    assert "--upgrade-head" in output


@patch("api_bootstrapper_cli.commands.add_alembic.AlembicManager")
def test_should_initialize_alembic_and_show_next_steps(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = AlembicSetupResult(
        manager=ManagerChoice.pyenv,
        config_path=tmp_path / "alembic.ini",
        env_path=tmp_path / "alembic" / "env.py",
        versions_path=tmp_path / "alembic" / "versions",
        initialized_now=True,
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(app, ["add-alembic", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Alembic initialized!" in output
    assert "poetry run alembic revision --autogenerate" in output
    mock_instance.setup.assert_called_once_with(tmp_path.resolve(), manager=None)


@patch("api_bootstrapper_cli.commands.add_alembic.AlembicManager")
def test_should_use_uv_prefix_when_manager_is_uv(
    mock_manager: MagicMock, tmp_path: Path
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = AlembicSetupResult(
        manager=ManagerChoice.uv,
        config_path=tmp_path / "alembic.ini",
        env_path=tmp_path / "alembic" / "env.py",
        versions_path=tmp_path / "alembic" / "versions",
        initialized_now=False,
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(
        app,
        ["add-alembic", "--path", str(tmp_path), "--manager", "uv"],
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Configuration refreshed" in output
    assert "uv run alembic revision --autogenerate" in output
    mock_instance.setup.assert_called_once_with(
        tmp_path.resolve(),
        manager=ManagerChoice.uv,
    )


@patch("api_bootstrapper_cli.commands.add_alembic.AlembicManager")
def test_should_handle_expected_errors(mock_manager: MagicMock, tmp_path: Path) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.side_effect = RuntimeError("init failed")
    mock_manager.return_value = mock_instance

    result = runner.invoke(app, ["add-alembic", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output
    assert "init failed" in output


@patch("api_bootstrapper_cli.commands.add_alembic.AlembicManager")
def test_should_start_db_and_run_revision_and_upgrade_when_requested(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = AlembicSetupResult(
        manager=ManagerChoice.pyenv,
        config_path=tmp_path / "alembic.ini",
        env_path=tmp_path / "alembic" / "env.py",
        versions_path=tmp_path / "alembic" / "versions",
        initialized_now=True,
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(
        app,
        [
            "add-alembic",
            "--path",
            str(tmp_path),
            "--with-db",
            "--create-initial-items",
            "--upgrade-head",
        ],
    )
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "db service is up" in output
    assert "create items table" in output
    assert "upgrade head applied" in output
    mock_instance.ensure_database_running.assert_called_once_with(tmp_path.resolve())
    mock_instance.create_initial_items_revision.assert_called_once_with(
        tmp_path.resolve(),
        ManagerChoice.pyenv,
    )
    mock_instance.upgrade_head.assert_called_once_with(
        tmp_path.resolve(),
        ManagerChoice.pyenv,
    )


@patch("api_bootstrapper_cli.commands.add_alembic.AlembicManager")
def test_should_auto_start_db_when_running_migrations_without_with_db_flag(
    mock_manager: MagicMock,
    tmp_path: Path,
) -> None:
    mock_instance = MagicMock()
    mock_instance.setup.return_value = AlembicSetupResult(
        manager=ManagerChoice.uv,
        config_path=tmp_path / "alembic.ini",
        env_path=tmp_path / "alembic" / "env.py",
        versions_path=tmp_path / "alembic" / "versions",
        initialized_now=False,
    )
    mock_manager.return_value = mock_instance

    result = runner.invoke(
        app,
        ["add-alembic", "--path", str(tmp_path), "--upgrade-head"],
    )

    assert result.exit_code == 0
    mock_instance.ensure_database_running.assert_called_once_with(tmp_path.resolve())
    mock_instance.create_initial_items_revision.assert_not_called()
    mock_instance.upgrade_head.assert_called_once_with(
        tmp_path.resolve(),
        ManagerChoice.uv,
    )
