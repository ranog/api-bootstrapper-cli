"""Dependency manager backed by uv.

https://github.com/astral-sh/uv
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


console = Console()


@dataclass(frozen=True)
class UvDependencyManager:
    """DependencyManager implementation using uv.

    uv replaces Poetry for virtual-environment creation and dependency
    installation.  It is compatible with both PEP 621 (``[project]``) and
    Poetry-style (``[tool.poetry]``) pyproject.toml files.
    """

    name: str = field(default="uv")

    def _get_clean_env(self) -> dict[str, str]:
        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONSTARTUP", None)
        return env

    def is_installed(self) -> bool:
        try:
            exec_cmd(["uv", "--version"], check=True, env=self._get_clean_env())
            return True
        except (ShellError, FileNotFoundError):
            return False

    def configure_venv(self, project_root: Path) -> None:
        """No-op: uv always creates an in-project .venv by default."""

    def use_python(self, project_root: Path, python_path: Path) -> None:
        """Create (or recreate) .venv with the specified Python interpreter."""
        try:
            exec_cmd(
                ["uv", "venv", "--python", str(python_path)],
                cwd=str(project_root),
                check=True,
                env=self._get_clean_env(),
            )
        except ShellError as e:
            raise RuntimeError(
                f"[uv] Falha ao criar virtualenv com Python {python_path}: {e}"
            ) from e

    def get_venv_path(self, project_root: Path) -> Path:
        return (project_root / ".venv").resolve()

    def get_venv_python(self, project_root: Path) -> Path:
        venv_path = self.get_venv_path(project_root)
        return self._resolve_venv_python(venv_path)

    def ensure_venv(self, project_root: Path) -> None:
        """Create .venv if it does not already exist."""
        venv_dir = project_root / ".venv"
        if venv_dir.exists() and venv_dir.is_dir():
            return
        try:
            exec_cmd(
                ["uv", "venv"],
                cwd=str(project_root),
                check=True,
                env=self._get_clean_env(),
            )
        except ShellError as e:
            raise RuntimeError(f"[uv] Falha ao criar virtualenv: {e}") from e

    def install_dependencies(self, project_root: Path) -> None:
        """Sync project dependencies with ``uv sync --all-groups``.

        Works with both PEP 621 (``[project]``) and Poetry-style
        (``[tool.poetry]``) pyproject.toml files.
        Installs all dependency groups including optional ones (e.g., dev).
        """
        self.ensure_venv(project_root)
        try:
            with console.status(
                "[cyan][uv] Syncing dependencies...[/cyan]",
                spinner="dots",
            ):
                exec_cmd(
                    ["uv", "sync", "--all-groups"],
                    cwd=str(project_root),
                    check=True,
                    env=self._get_clean_env(),
                )
        except ShellError as e:
            raise RuntimeError(f"[uv] Falha ao sincronizar dependências: {e}") from e

    def _resolve_venv_python(self, venv_path: Path) -> Path:
        if platform.system() == "Windows":
            return venv_path / "Scripts" / "python.exe"
        return venv_path / "bin" / "python"
