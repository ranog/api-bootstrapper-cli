from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core import files
from api_bootstrapper_cli.core.protocols import (
    DependencyManager,
    EditorConfigWriter,
    Logger,
    PythonEnvironmentManager,
)


@dataclass
class EnvironmentSetupResult:
    """Environment setup result.

    Encapsulates information about the configured environment.
    """

    python_version: str
    python_path: Path
    venv_path: Path | None
    venv_python: Path | None
    editor_config_path: Path
    has_poetry_project: bool


class EnvironmentBootstrapService:
    """Orchestration service for Python environment bootstrap.

    Separates business logic from presentation and concrete implementations.
    Uses dependency injection to decouple from specific implementations.
    """

    def __init__(
        self,
        python_env_manager: PythonEnvironmentManager,
        dependency_manager: DependencyManager,
        editor_writer: EditorConfigWriter,
        logger: Logger,
    ):
        """Initialize the service with its dependencies.

        Args:
            python_env_manager: Python version manager (pyenv, etc)
            dependency_manager: Dependency manager (poetry, etc)
            editor_writer: Editor configuration writer
            logger: Logging interface
        """
        self._python_env = python_env_manager
        self._deps = dependency_manager
        self._editor = editor_writer
        self._logger = logger

    def bootstrap(
        self,
        project_root: Path,
        python_version: str,
        install_dependencies: bool = True,
    ) -> EnvironmentSetupResult:
        """Execute complete project environment bootstrap.

        Args:
            project_root: Project root directory
            python_version: Desired Python version
            install_dependencies: Whether to install dependencies

        Returns:
            EnvironmentSetupResult with configured environment information

        Raises:
            ValueError: If pyenv is not installed
        """
        # Ensure project directory exists
        files.ensure_dir(project_root)

        self._validate_requirements()

        # Check if environment already exists
        if self._is_environment_ready(project_root, python_version):
            self._logger.info("environment already configured")
            return self._get_existing_environment_result(project_root, python_version)

        # Setup Python via pyenv
        python_path = self._setup_python_environment(project_root, python_version)

        # Install Poetry and pip tools in project Python
        self._install_python_dependencies(python_version)

        # Ensure pyproject.toml exists (create minimal if needed)
        self._ensure_pyproject_exists(project_root, python_version)

        # Setup with Poetry (now always has pyproject.toml)
        result = self._setup_with_poetry(
            project_root,
            python_path,
            python_version,
            install_dependencies,
        )

        return result

    def _validate_requirements(self) -> None:
        """Validate that required tools are installed."""
        if not self._python_env.is_installed():
            raise ValueError("pyenv not found in PATH. Install pyenv first.")

    def _is_environment_ready(self, project_root: Path, python_version: str) -> bool:
        """Check if environment is already configured.

        Args:
            project_root: Project root directory
            python_version: Expected Python version

        Returns:
            True if environment exists and is properly configured
        """
        venv_path = project_root / ".venv"
        pyproject_path = project_root / "pyproject.toml"
        python_version_file = project_root / ".python-version"

        # Check if all required files/directories exist
        if not (
            venv_path.exists()
            and pyproject_path.exists()
            and python_version_file.exists()
        ):
            return False

        # Check if .python-version matches requested version
        try:
            existing_version = python_version_file.read_text().strip()
            if existing_version != python_version:
                return False
        except Exception:
            return False

        # Check if venv has Python executable
        venv_python = venv_path / "bin" / "python"
        if not venv_python.exists():
            return False

        return True

    def _get_existing_environment_result(
        self,
        project_root: Path,
        python_version: str,
    ) -> EnvironmentSetupResult:
        """Get result for existing environment.

        Args:
            project_root: Project root directory
            python_version: Python version

        Returns:
            EnvironmentSetupResult with existing environment information
        """
        venv_path = project_root / ".venv"
        venv_python = venv_path / "bin" / "python"
        python_path = self._python_env.get_python_path(python_version)
        vscode_settings = project_root / ".vscode" / "settings.json"

        self._logger.success("environment ready")

        return EnvironmentSetupResult(
            python_version=python_version,
            python_path=python_path,
            venv_path=venv_path,
            venv_python=venv_python,
            editor_config_path=vscode_settings,
            has_poetry_project=True,
        )

    def _setup_python_environment(
        self,
        project_root: Path,
        python_version: str,
    ) -> Path:
        """Configure Python via pyenv.

        Returns:
            Path to the Python executable
        """
        self._logger.info(f"pyenv ensure python {python_version}")
        self._python_env.ensure_python(python_version)

        self._logger.info(f"pyenv set local {python_version} in {project_root}")
        self._python_env.set_local(project_root, python_version)

        python_path = self._python_env.get_python_path(python_version)
        self._logger.success(f"python {python_path}")

        return python_path

    def _install_python_dependencies(self, python_version: str) -> None:
        """Install pip, setuptools, wheel and poetry in project Python.

        Args:
            python_version: Python version in X.Y.Z format
        """
        self._logger.info("installing pip, setuptools, wheel, poetry")
        self._python_env.install_pip_packages(
            python_version,
            ["pip", "setuptools", "wheel", "poetry"],
        )
        self._logger.success("python dependencies installed")

    def _ensure_pyproject_exists(self, project_root: Path, python_version: str) -> None:
        """Ensure pyproject.toml exists, creating minimal if needed.

        Args:
            project_root: Project root directory
            python_version: Python version for dependency constraint
        """
        pyproject_path = project_root / "pyproject.toml"

        if not pyproject_path.exists():
            self._logger.info("creating minimal pyproject.toml")
            files.create_minimal_pyproject(project_root, python_version=python_version)
            self._logger.success(f"created {pyproject_path}")

    def _setup_with_poetry(
        self,
        project_root: Path,
        python_path: Path,
        python_version: str,
        install_dependencies: bool,
    ) -> EnvironmentSetupResult:
        """Complete setup with Poetry."""
        self._logger.info("poetry configure in-project venv (.venv)")
        self._deps.configure_venv(project_root)

        self._logger.info("poetry use python")
        self._deps.use_python(project_root, python_path)

        # Always ensure venv exists (important for projects without dependencies)
        venv_path_dir = project_root / ".venv"
        if not venv_path_dir.exists():
            self._logger.info("poetry create venv")
            self._deps.install_dependencies(project_root)

        if install_dependencies:
            self._logger.info("poetry install dependencies")
            self._deps.install_dependencies(project_root)

        # Get venv information
        venv_path = self._deps.get_venv_path(project_root)
        venv_python = self._deps.get_venv_python(project_root)

        self._logger.success(f"venv {venv_path}")

        # Configure editor with venv Python
        editor_config = self._editor.write_config(project_root, venv_python)
        self._logger.success(f"vscode wrote {editor_config}")

        return EnvironmentSetupResult(
            python_version=python_version,
            python_path=python_path,
            venv_path=venv_path,
            venv_python=venv_python,
            editor_config_path=editor_config,
            has_poetry_project=True,
        )
