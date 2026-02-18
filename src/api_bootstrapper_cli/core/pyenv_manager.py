from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


console = Console()


@dataclass(frozen=True)
class PyenvManager:
    """Python version manager using pyenv.

    Implements PythonEnvironmentManager protocol.
    Encapsulates all details of pyenv interaction.
    """

    def _get_clean_env(self) -> dict[str, str]:
        """Return clean environment without Python/venv interference.

        Removes variables that could cause pyenv to use wrong Python version
        or interfere with target project setup.
        """
        env = os.environ.copy()

        env.pop("VIRTUAL_ENV", None)
        env.pop("POETRY_ACTIVE", None)
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONSTARTUP", None)

        return env

    def is_installed(self) -> bool:
        try:
            exec_cmd(["pyenv", "--version"], check=True, env=self._get_clean_env())
            return True
        except ShellError:
            return False

    def ensure_python(self, version: str) -> None:
        if version in self._get_installed_versions():
            return

        with console.status(
            f"[cyan]Installing Python {version} via pyenv...[/cyan]",
            spinner="dots",
        ):
            exec_cmd(
                ["pyenv", "install", "-s", version],
                check=True,
                env=self._get_clean_env(),
            )

    def set_local(self, project_root: Path, version: str) -> None:
        exec_cmd(
            ["pyenv", "local", version],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def get_python_path(self, version: str) -> Path:
        """Return path to Python executable (uses pyenv prefix, independent of cwd)."""
        res = exec_cmd(
            ["pyenv", "prefix", version],
            check=True,
            env=self._get_clean_env(),
        )
        python_prefix = Path(res.stdout.strip())
        return python_prefix / "bin" / "python"

    def install_pip_packages(self, version: str, packages: list[str]) -> None:
        python_path = self.get_python_path(version)
        packages_str = ", ".join(packages)
        with console.status(
            f"[cyan]Installing {packages_str}...[/cyan]",
            spinner="dots",
        ):
            exec_cmd(
                [str(python_path), "-m", "pip", "install", "--upgrade", *packages],
                check=True,
                env=self._get_clean_env(),
            )

    def _get_installed_versions(self) -> set[str]:
        res = exec_cmd(
            ["pyenv", "versions", "--bare"],
            check=True,
            env=self._get_clean_env(),
        )
        return {line.strip() for line in res.stdout.splitlines() if line.strip()}
