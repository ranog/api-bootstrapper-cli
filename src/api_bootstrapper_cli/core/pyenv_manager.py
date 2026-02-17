from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


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

        # Remove active venv variables
        env.pop("VIRTUAL_ENV", None)
        env.pop("POETRY_ACTIVE", None)

        # Remove Python path variables that could interfere
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONSTARTUP", None)

        return env

    def is_installed(self) -> bool:
        """Check if pyenv is available on the system."""
        try:
            exec_cmd(["pyenv", "--version"], check=True, env=self._get_clean_env())
            return True
        except ShellError:
            return False

    def ensure_python(self, version: str) -> None:
        """Ensure the Python version is installed via pyenv.

        Args:
            version: Python version in X.Y.Z format
        """
        if version in self._get_installed_versions():
            return

        exec_cmd(
            ["pyenv", "install", "-s", version], check=True, env=self._get_clean_env()
        )

    def set_local(self, project_root: Path, version: str) -> None:
        """Set the project's local Python version.

        Args:
            project_root: Project root directory
            version: Python version in X.Y.Z format
        """
        exec_cmd(
            ["pyenv", "local", version],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def get_python_path(self, version: str) -> Path:
        """Return the path to the Python executable for the version.

        Uses pyenv prefix to get the installation path for the specific version,
        independent of the current directory context.

        Args:
            version: Python version in X.Y.Z format

        Returns:
            Path to the Python executable
        """
        res = exec_cmd(
            ["pyenv", "prefix", version],
            check=True,
            env=self._get_clean_env(),
        )
        python_prefix = Path(res.stdout.strip())
        return python_prefix / "bin" / "python"

    def install_pip_packages(self, version: str, packages: list[str]) -> None:
        """Install pip packages in the Python version.

        Args:
            version: Python version in X.Y.Z format
            packages: List of package names to install
        """
        python_path = self.get_python_path(version)
        exec_cmd(
            [str(python_path), "-m", "pip", "install", "--upgrade", *packages],
            check=True,
            env=self._get_clean_env(),
        )

    def _get_installed_versions(self) -> set[str]:
        """Return set of Python versions installed via pyenv.

        Private method - implementation detail.
        """
        res = exec_cmd(
            ["pyenv", "versions", "--bare"],
            check=True,
            env=self._get_clean_env(),
        )
        return {line.strip() for line in res.stdout.splitlines() if line.strip()}
