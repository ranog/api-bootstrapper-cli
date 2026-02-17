from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


@dataclass(frozen=True)
class PoetryManager:
    """Dependency manager using Poetry.

    Implements DependencyManager protocol.
    Encapsulates all details of Poetry interaction and venv structure.
    """

    def _get_poetry_cmd(self) -> str:
        """Get absolute path to poetry executable.

        If using pyenv, gets the real poetry path from pyenv to bypass shims.
        Otherwise falls back to searching PATH or using "poetry" command.

        Returns:
            Absolute path to poetry executable, or "poetry" as fallback
        """
        # First try: Ask pyenv for the real poetry path (bypasses shims)
        try:
            result = exec_cmd(
                ["pyenv", "which", "poetry"],
                check=True,
                env=self._get_clean_env(),
            )
            poetry_path = result.stdout.strip()
            if poetry_path and Path(poetry_path).exists():
                return poetry_path
        except (ShellError, FileNotFoundError):
            # pyenv not available or poetry not found via pyenv
            pass

        # Second try: Search clean PATH (without pyenv shims)
        env = self._get_clean_env()
        clean_path = env.get("PATH", "")
        for path_dir in clean_path.split(os.pathsep):
            if not path_dir:
                continue
            poetry_path = Path(path_dir) / "poetry"
            if poetry_path.exists() and os.access(poetry_path, os.X_OK):
                return str(poetry_path)

        # Fallback to "poetry" command - will work with clean env
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

        # Remove active venv variables
        env.pop("VIRTUAL_ENV", None)
        env.pop("POETRY_ACTIVE", None)

        # Remove Python path variables that could interfere
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONSTARTUP", None)
        env.pop("PYTHONUSERBASE", None)

        # Remove pyenv shims from PATH to prevent version switching
        # This ensures poetry runs from its actual installation location
        path = env.get("PATH", "")
        path_dirs = path.split(os.pathsep)
        clean_path_dirs = [d for d in path_dirs if ".pyenv/shims" not in d]
        env["PATH"] = os.pathsep.join(clean_path_dirs)

        return env

    def is_installed(self) -> bool:
        """Check if Poetry is available on the system."""
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
        """Configure Poetry to use in-project venv (.venv).

        Args:
            project_root: Project root directory
        """
        exec_cmd(
            [
                self._get_poetry_cmd(),
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

        This command creates the virtual environment if it doesn't exist yet.

        Args:
            project_root: Project root directory
            python_path: Path to the Python executable
        """
        exec_cmd(
            [self._get_poetry_cmd(), "env", "use", str(python_path)],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def get_venv_path(self, project_root: Path) -> Path:
        """Return the path to the project's virtual environment.

        Since we configure virtualenvs.in-project=true, the venv is always
        at <project_root>/.venv. We don't trust `poetry env info -p` as it
        may return the wrong venv when executed from within another Poetry project.

        Args:
            project_root: Project root directory

        Returns:
            Path to the virtual environment (always absolute)
        """
        # With virtualenvs.in-project=true, venv is always in .venv
        return (project_root / ".venv").resolve()

    def get_venv_python(self, project_root: Path) -> Path:
        """Return the path to the Python executable in the virtual environment.

        Encapsulates the logic for Windows/Unix differences.

        Args:
            project_root: Project root directory

        Returns:
            Path to the Python executable in the venv
        """
        venv_path = self.get_venv_path(project_root)
        return self._resolve_venv_python(venv_path)

    def install_dependencies(self, project_root: Path) -> None:
        """Install the project's dependencies using Poetry.

        Uses --no-root to not install the project as a package,
        allowing use in projects that are applications (not libraries)
        without needing to configure package-mode = false.

        Args:
            project_root: Project root directory
        """
        # Ensure venv exists before installing
        self._ensure_venv_exists(project_root)

        exec_cmd(
            [self._get_poetry_cmd(), "install", "--no-root"],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )

    def _resolve_venv_python(self, venv_path: Path) -> Path:
        """Resolve the Python path in venv considering the operating system.

        Private method - implementation detail.

        Args:
            venv_path: Path to the virtual environment

        Returns:
            Path to the Python executable
        """
        if platform.system() == "Windows":
            return venv_path / "Scripts" / "python.exe"
        return venv_path / "bin" / "python"

    def _ensure_venv_exists(self, project_root: Path) -> None:
        """Ensure the virtual environment has been created.

        In some cases (projects without dependencies), Poetry may not create
        the venv automatically. This method forces creation.

        Args:
            project_root: Project root directory
        """
        # Check if .venv already exists in the project (in-project venv)
        venv_dir = project_root / ".venv"
        if venv_dir.exists() and venv_dir.is_dir():
            return

        # If it doesn't exist, force creation by running install
        # This ensures the venv is created even without dependencies
        exec_cmd(
            [self._get_poetry_cmd(), "install", "--no-root"],
            cwd=str(project_root),
            check=True,
            env=self._get_clean_env(),
        )
