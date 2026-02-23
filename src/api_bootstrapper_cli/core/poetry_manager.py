from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


console = Console()


@dataclass(frozen=True)
class PoetryManager:
    def _get_poetry_cmd(self, project_root: Path | None = None) -> str:
        try:
            result = exec_cmd(
                ["pyenv", "which", "poetry"],
                check=True,
                env=self._get_clean_env(),
                cwd=str(project_root) if project_root else None,
            )
            poetry_path = result.stdout.strip()
            if poetry_path and Path(poetry_path).exists():
                return poetry_path
        except (ShellError, FileNotFoundError):
            pass

        env = self._get_clean_env()
        clean_path = env.get("PATH", "")
        for path_dir in clean_path.split(os.pathsep):
            if not path_dir:
                continue
            posix_path = Path(path_dir) / "poetry"
            if posix_path.exists() and os.access(posix_path, os.X_OK):
                return str(posix_path)

        return "poetry"

    def _get_clean_env(self) -> dict[str, str]:
        """Return clean environment without active venv variables and pyenv shims.

        This ensures Poetry doesn't use the CLI's venv when executing commands
        in the target project, and prevents pyenv from redirecting poetry
        commands to different Python versions.

        CRITICAL: This allows the CLI to work from anywhere, even when run
        from inside an active venv.
        """
        env = os.environ.copy()

        env.pop("VIRTUAL_ENV", None)
        env.pop("POETRY_ACTIVE", None)
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONSTARTUP", None)
        env.pop("PYTHONUSERBASE", None)

        path = env.get("PATH", "")
        path_dirs = path.split(os.pathsep)
        clean_path_dirs = [d for d in path_dirs if ".pyenv/shims" not in d]
        env["PATH"] = os.pathsep.join(clean_path_dirs)

        return env

    def is_installed(self) -> bool:
        try:
            exec_cmd(
                [self._get_poetry_cmd(), "--version"],
                check=True,
                env=self._get_clean_env(),
            )
            return True
        except ShellError:
            return False

    def configure_venv(self, project_root: Path) -> None:
        exec_cmd(
            [
                self._get_poetry_cmd(project_root),
                "config",
                "virtualenvs.in-project",
                "true",
                "--local",
            ],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def use_python(self, project_root: Path, python_path: Path) -> None:
        """Set which Python interpreter Poetry should use.

        NOTE: Creates the virtual environment if it doesn't exist yet.
        """
        exec_cmd(
            [self._get_poetry_cmd(project_root), "env", "use", str(python_path)],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def get_venv_path(self, project_root: Path) -> Path:
        """Return path to the project's virtual environment.

        NOTE: We don't use `poetry env info -p` as it may return wrong venv
        when executed from within another Poetry project.
        """
        return (project_root / ".venv").resolve()

    def get_venv_python(self, project_root: Path) -> Path:
        venv_path = self.get_venv_path(project_root)
        return self._resolve_venv_python(venv_path)

    def install_dependencies(self, project_root: Path) -> None:
        """Install project dependencies with Poetry.

        NOTE: Uses --no-root to support app projects without package-mode config.
        """
        self._ensure_venv_exists(project_root)

        with console.status(
            "[cyan]Installing dependencies with Poetry...[/cyan]",
            spinner="dots",
        ):
            exec_cmd(
                [self._get_poetry_cmd(project_root), "install", "--no-root"],
                cwd=str(project_root),
                check=True,
                env=self._get_clean_env(),
            )

    def _resolve_venv_python(self, venv_path: Path) -> Path:
        if platform.system() == "Windows":
            return venv_path / "Scripts" / "python.exe"
        return venv_path / "bin" / "python"

    def _ensure_venv_exists(self, project_root: Path) -> None:
        """Ensure venv exists (Poetry may skip creation for projects without dependencies)."""
        venv_dir = project_root / ".venv"
        if venv_dir.exists() and venv_dir.is_dir():
            return

        exec_cmd(
            [self._get_poetry_cmd(project_root), "install", "--no-root"],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )
