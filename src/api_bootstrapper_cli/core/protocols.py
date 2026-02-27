from __future__ import annotations

import enum
from pathlib import Path
from typing import Protocol


class ManagerChoice(str, enum.Enum):
    """Manager backend for Python environment and dependencies."""

    pyenv = "pyenv"
    uv = "uv"


class PythonEnvironmentManager(Protocol):
    """Interface for Python version managers (pyenv, asdf, etc)."""

    def is_installed(self) -> bool:
        """Check if the manager is installed on the system."""
        ...

    def ensure_python(self, version: str) -> None:
        """Ensure a specific Python version is available."""
        ...

    def set_local(self, project_root: Path, version: str) -> None:
        """Set the local Python version for the project."""
        ...

    def get_python_path(self, version: str) -> Path:
        """Return the path to the Python executable for the version."""
        ...

    def install_pip_packages(self, version: str, packages: list[str]) -> None:
        """Install pip packages for a specific Python version."""
        ...


class DependencyManager(Protocol):
    """Interface for dependency managers (poetry, pipenv, etc)."""

    def is_installed(self) -> bool:
        """Check if the manager is installed on the system."""
        ...

    def configure_venv(self, project_root: Path) -> None:
        """Configure the project's virtual environment."""
        ...

    def use_python(self, project_root: Path, python_path: Path) -> None:
        """Set which Python interpreter to use."""
        ...

    def get_venv_path(self, project_root: Path) -> Path:
        """Return the path to the virtual environment."""
        ...

    def get_venv_python(self, project_root: Path) -> Path:
        """Return the path to the Python executable in the virtual environment."""
        ...

    def ensure_venv(self, project_root: Path) -> None:
        """Ensure virtual environment exists without a full dependency install."""
        ...

    def install_dependencies(self, project_root: Path) -> None:
        """Install the project's dependencies."""
        ...


class EditorConfigWriter(Protocol):
    """Interface for editor configuration writers."""

    def write_config(self, project_root: Path, python_path: Path) -> Path:
        """Write editor configuration and return the path of the created file."""
        ...


class Logger(Protocol):
    """Interface for logging/output."""

    def info(self, message: str) -> None:
        """Log information."""
        ...

    def success(self, message: str) -> None:
        """Log success."""
        ...

    def warning(self, message: str) -> None:
        """Log warning."""
        ...

    def error(self, message: str) -> None:
        """Log error."""
        ...
