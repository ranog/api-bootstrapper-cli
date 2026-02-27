"""Python version manager backed by uv.

https://github.com/astral-sh/uv
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


console = Console()


@dataclass(frozen=True)
class UvPythonManager:
    """PythonEnvironmentManager implementation using uv.

    uv can install and manage Python versions via `uv python`, making pyenv
    optional for projects that already adopt uv.
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

    def ensure_python(self, version: str) -> None:
        """Install the requested Python version with uv if not already present."""
        try:
            with console.status(
                f"[cyan][env] Installing Python {version} via uv...[/cyan]",
                spinner="dots",
            ):
                exec_cmd(
                    ["uv", "python", "install", version],
                    check=True,
                    env=self._get_clean_env(),
                )
        except ShellError as e:
            raise RuntimeError(
                f"[env] Falha ao instalar Python {version} via uv: {e}"
            ) from e

    def set_local(self, project_root: Path, version: str) -> None:
        """Pin the Python version for the project (creates .python-version)."""
        try:
            exec_cmd(
                ["uv", "python", "pin", version],
                cwd=str(project_root),
                check=True,
                env=self._get_clean_env(),
            )
        except ShellError as e:
            raise RuntimeError(
                f"[env] Falha ao definir Python {version} local via uv: {e}"
            ) from e

    def get_python_path(self, version: str) -> Path:
        """Return the path to the Python binary for the given version."""
        try:
            res = exec_cmd(
                ["uv", "python", "find", version],
                check=True,
                env=self._get_clean_env(),
            )
        except ShellError as e:
            raise RuntimeError(
                f"[env] Falha ao obter caminho do Python {version} via uv: {e}"
            ) from e
        return Path(res.stdout.strip())

    def install_pip_packages(self, version: str, packages: list[str]) -> None:
        """No-op: uv manages its own internals.

        When using uv as the dependency manager, pip/setuptools/wheel/poetry do
        not need to be pre-installed; uv handles everything natively.
        """
