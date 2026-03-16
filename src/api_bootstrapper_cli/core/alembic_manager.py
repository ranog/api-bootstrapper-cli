from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.files import read_text, write_text
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


ALEMBIC_ENV_TEMPLATE = """from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/app_db",
    )


config.set_main_option("sqlalchemy.url", get_database_url())

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""


@dataclass(frozen=True)
class AlembicSetupResult:
    manager: ManagerChoice
    config_path: Path
    env_path: Path
    versions_path: Path
    initialized_now: bool


@dataclass(frozen=True)
class AlembicManager:
    def _detect_manager(self, project_root: Path) -> ManagerChoice:
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found in {project_root}")

        content = read_text(pyproject_path)

        if "[tool.poetry]" in content:
            return ManagerChoice.pyenv

        if "[project]" in content:
            return ManagerChoice.uv

        return ManagerChoice.pyenv

    def setup(
        self,
        project_root: Path,
        manager: ManagerChoice | None = None,
    ) -> AlembicSetupResult:
        if not project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")

        selected_manager = manager or self._detect_manager(project_root)

        alembic_ini = project_root / "alembic.ini"
        alembic_dir = project_root / "alembic"
        env_path = alembic_dir / "env.py"
        versions_path = alembic_dir / "versions"

        has_ini = alembic_ini.exists()
        has_dir = alembic_dir.exists()

        if has_ini != has_dir:
            raise RuntimeError(
                "Detected partial Alembic setup (alembic.ini and alembic/ must coexist)."
            )

        initialized_now = False
        if not has_ini and not has_dir:
            self._run_init(project_root, selected_manager)
            initialized_now = True

        if not env_path.exists():
            raise RuntimeError(f"Alembic env.py not found: {env_path}")

        write_text(env_path, ALEMBIC_ENV_TEMPLATE, overwrite=True)
        versions_path.mkdir(parents=True, exist_ok=True)

        return AlembicSetupResult(
            manager=selected_manager,
            config_path=alembic_ini,
            env_path=env_path,
            versions_path=versions_path,
            initialized_now=initialized_now,
        )

    def _run_init(self, project_root: Path, manager: ManagerChoice) -> None:
        command = (
            ["uv", "run", "alembic", "init", "alembic"]
            if manager == ManagerChoice.uv
            else ["poetry", "run", "alembic", "init", "alembic"]
        )

        try:
            exec_cmd(command, cwd=str(project_root), check=True)
        except (ShellError, FileNotFoundError) as error:
            raise RuntimeError(
                f"Failed to initialize Alembic using {manager.value}: {error}"
            ) from error

    def ensure_database_running(
        self,
        project_root: Path,
        retries: int = 30,
        delay_seconds: float = 1.0,
    ) -> None:
        compose_cmd = self._get_compose_command()
        up_command = compose_cmd + ["up", "-d", "db"]
        ready_command = compose_cmd + [
            "exec",
            "-T",
            "db",
            "pg_isready",
            "-U",
            "postgres",
            "-d",
            "app_db",
        ]

        try:
            exec_cmd(up_command, cwd=str(project_root), check=True)
        except (ShellError, FileNotFoundError) as error:
            raise RuntimeError(f"Failed to start database service: {error}") from error

        for attempt in range(retries):
            result = exec_cmd(ready_command, cwd=str(project_root), check=False)
            if result.returncode == 0:
                return

            if attempt < retries - 1:
                time.sleep(delay_seconds)

        raise RuntimeError("Database service did not become ready in time.")

    def create_initial_items_revision(
        self,
        project_root: Path,
        manager: ManagerChoice,
        message: str = "create items table",
    ) -> None:
        command = self._build_alembic_command(
            manager,
            ["revision", "--autogenerate", "-m", message],
        )

        try:
            exec_cmd(command, cwd=str(project_root), check=True)
        except (ShellError, FileNotFoundError) as error:
            raise RuntimeError(f"Failed to create Alembic revision: {error}") from error

    def upgrade_head(self, project_root: Path, manager: ManagerChoice) -> None:
        command = self._build_alembic_command(manager, ["upgrade", "head"])

        try:
            exec_cmd(command, cwd=str(project_root), check=True)
        except (ShellError, FileNotFoundError) as error:
            raise RuntimeError(f"Failed to upgrade Alembic head: {error}") from error

    def _get_compose_command(self) -> list[str]:
        try:
            exec_cmd(["docker", "compose", "version"], check=True)
            return ["docker", "compose"]
        except (ShellError, FileNotFoundError):
            pass

        try:
            exec_cmd(["docker-compose", "version"], check=True)
            return ["docker-compose"]
        except (ShellError, FileNotFoundError):
            pass

        raise RuntimeError(
            "Docker Compose not found. Install Docker Compose to run migrations with --with-db."
        )

    def _build_alembic_command(
        self, manager: ManagerChoice, args: list[str]
    ) -> list[str]:
        prefix = (
            ["uv", "run", "alembic"]
            if manager == ManagerChoice.uv
            else [
                "poetry",
                "run",
                "alembic",
            ]
        )
        return prefix + args
