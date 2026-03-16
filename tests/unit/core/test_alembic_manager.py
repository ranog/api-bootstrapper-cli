from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.alembic_manager import AlembicManager
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.shell import CommandResult, ShellError


def _create_pyproject(project_root: Path, *, manager: ManagerChoice) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    pyproject = project_root / "pyproject.toml"

    if manager == ManagerChoice.uv:
        pyproject.write_text('[project]\nname = "demo"\nversion = "0.1.0"\n')
        return

    pyproject.write_text('[tool.poetry]\nname = "demo"\nversion = "0.1.0"\n')


def test_should_detect_poetry_manager_from_pyproject(tmp_path: Path) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)

    manager = AlembicManager()
    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.pyenv


def test_should_detect_uv_manager_from_pyproject(tmp_path: Path) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.uv)

    manager = AlembicManager()
    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.uv


def test_should_raise_when_pyproject_is_missing(tmp_path: Path) -> None:
    manager = AlembicManager()

    with pytest.raises(FileNotFoundError, match="pyproject.toml not found"):
        manager._detect_manager(tmp_path)


def test_should_raise_when_project_root_does_not_exist(tmp_path: Path) -> None:
    manager = AlembicManager()

    with pytest.raises(ValueError, match="Project root does not exist"):
        manager.setup(tmp_path / "missing")


def test_should_initialize_alembic_with_poetry_when_not_configured(
    tmp_path: Path,
    mocker,
) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)

    def _fake_exec(command, cwd=None, **kwargs):
        root = Path(cwd)
        (root / "alembic").mkdir(exist_ok=True)
        (root / "alembic" / "versions").mkdir(exist_ok=True)
        (root / "alembic" / "env.py").write_text("placeholder")
        (root / "alembic.ini").write_text("[alembic]\n")
        return CommandResult(stdout="", stderr="", returncode=0)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = _fake_exec

    result = AlembicManager().setup(tmp_path)

    assert result.manager == ManagerChoice.pyenv
    assert result.initialized_now is True
    assert result.config_path.exists()
    assert result.env_path.exists()
    assert result.versions_path.exists()
    assert "target_metadata = Base.metadata" in result.env_path.read_text()

    expected_command = ["poetry", "run", "alembic", "init", "alembic"]
    assert mock_exec.call_args[0][0] == expected_command


def test_should_initialize_alembic_with_uv_when_manager_is_uv(
    tmp_path: Path, mocker
) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.uv)

    def _fake_exec(command, cwd=None, **kwargs):
        root = Path(cwd)
        (root / "alembic").mkdir(exist_ok=True)
        (root / "alembic" / "versions").mkdir(exist_ok=True)
        (root / "alembic" / "env.py").write_text("placeholder")
        (root / "alembic.ini").write_text("[alembic]\n")
        return CommandResult(stdout="", stderr="", returncode=0)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = _fake_exec

    result = AlembicManager().setup(tmp_path, manager=ManagerChoice.uv)

    assert result.manager == ManagerChoice.uv
    assert result.initialized_now is True

    expected_command = ["uv", "run", "alembic", "init", "alembic"]
    assert mock_exec.call_args[0][0] == expected_command


def test_should_refresh_env_without_reinitializing_when_alembic_exists(
    tmp_path: Path,
    mocker,
) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)
    (tmp_path / "alembic.ini").write_text("[alembic]\n")
    (tmp_path / "alembic" / "versions").mkdir(parents=True)
    env_path = tmp_path / "alembic" / "env.py"
    env_path.write_text("old env")

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")

    result = AlembicManager().setup(tmp_path)

    assert result.initialized_now is False
    assert mock_exec.call_count == 0
    assert "target_metadata = Base.metadata" in env_path.read_text()


def test_should_raise_for_partial_alembic_setup(tmp_path: Path) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)
    (tmp_path / "alembic.ini").write_text("[alembic]\n")

    with pytest.raises(RuntimeError, match="partial Alembic setup"):
        AlembicManager().setup(tmp_path)


def test_should_raise_when_alembic_env_file_is_missing_after_init(
    tmp_path: Path,
    mocker,
) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)

    def _fake_exec(command, cwd=None, **kwargs):
        root = Path(cwd)
        (root / "alembic").mkdir(exist_ok=True)
        (root / "alembic" / "versions").mkdir(exist_ok=True)
        (root / "alembic.ini").write_text("[alembic]\n")
        return CommandResult(stdout="", stderr="", returncode=0)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = _fake_exec

    with pytest.raises(RuntimeError, match="Alembic env.py not found"):
        AlembicManager().setup(tmp_path)


def test_should_raise_when_init_command_fails(tmp_path: Path, mocker) -> None:
    _create_pyproject(tmp_path, manager=ManagerChoice.pyenv)

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = ShellError("command failed")

    with pytest.raises(RuntimeError, match="Failed to initialize Alembic"):
        AlembicManager().setup(tmp_path)


def test_should_start_database_service_and_wait_until_ready(
    tmp_path: Path, mocker
) -> None:
    manager = AlembicManager()

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="Docker Compose version v2", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=1),
        CommandResult(stdout="", stderr="", returncode=0),
    ]
    mock_sleep = mocker.patch("api_bootstrapper_cli.core.alembic_manager.time.sleep")

    manager.ensure_database_running(tmp_path, retries=2, delay_seconds=0.01)

    assert mock_exec.call_args_list[1].args[0] == [
        "docker",
        "compose",
        "up",
        "-d",
        "db",
    ]
    assert mock_exec.call_args_list[2].args[0] == [
        "docker",
        "compose",
        "exec",
        "-T",
        "db",
        "pg_isready",
        "-U",
        "postgres",
        "-d",
        "app_db",
    ]
    assert mock_sleep.call_count == 1


def test_should_fallback_to_docker_compose_binary_when_needed(tmp_path: Path, mocker):
    manager = AlembicManager()

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = [
        ShellError("docker compose unavailable"),
        CommandResult(stdout="docker-compose 1.29.2", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
    ]

    manager.ensure_database_running(tmp_path, retries=1, delay_seconds=0.0)

    assert mock_exec.call_args_list[2].args[0] == ["docker-compose", "up", "-d", "db"]


def test_should_raise_when_docker_compose_is_not_available(tmp_path: Path, mocker):
    manager = AlembicManager()

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = [
        ShellError("docker compose unavailable"),
        FileNotFoundError("docker-compose"),
    ]

    with pytest.raises(RuntimeError, match="Docker Compose not found"):
        manager.ensure_database_running(tmp_path)


def test_should_raise_when_database_does_not_become_ready(tmp_path: Path, mocker):
    manager = AlembicManager()

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="Docker Compose version v2", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=0),
        CommandResult(stdout="", stderr="", returncode=1),
        CommandResult(stdout="", stderr="", returncode=1),
    ]
    mocker.patch("api_bootstrapper_cli.core.alembic_manager.time.sleep")

    with pytest.raises(RuntimeError, match="did not become ready"):
        manager.ensure_database_running(tmp_path, retries=2, delay_seconds=0.0)


def test_should_raise_when_database_service_start_fails(tmp_path: Path, mocker):
    manager = AlembicManager()

    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = [
        CommandResult(stdout="Docker Compose version v2", stderr="", returncode=0),
        ShellError("compose up failed"),
    ]

    with pytest.raises(RuntimeError, match="Failed to start database service"):
        manager.ensure_database_running(tmp_path)


def test_should_create_initial_items_revision_with_selected_manager(
    tmp_path: Path, mocker
):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    AlembicManager().create_initial_items_revision(tmp_path, ManagerChoice.pyenv)

    assert mock_exec.call_args.args[0] == [
        "poetry",
        "run",
        "alembic",
        "revision",
        "--autogenerate",
        "-m",
        "create items table",
    ]


def test_should_raise_when_create_revision_fails(tmp_path: Path, mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = ShellError("revision failed")

    with pytest.raises(RuntimeError, match="Failed to create Alembic revision"):
        AlembicManager().create_initial_items_revision(tmp_path, ManagerChoice.uv)


def test_should_upgrade_head_with_selected_manager(tmp_path: Path, mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.return_value = CommandResult(stdout="", stderr="", returncode=0)

    AlembicManager().upgrade_head(tmp_path, ManagerChoice.uv)

    assert mock_exec.call_args.args[0] == ["uv", "run", "alembic", "upgrade", "head"]


def test_should_raise_when_upgrade_head_fails(tmp_path: Path, mocker):
    mock_exec = mocker.patch("api_bootstrapper_cli.core.alembic_manager.exec_cmd")
    mock_exec.side_effect = ShellError("upgrade failed")

    with pytest.raises(RuntimeError, match="Failed to upgrade Alembic head"):
        AlembicManager().upgrade_head(tmp_path, ManagerChoice.pyenv)
