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
    python_version: str
    python_path: Path
    venv_path: Path | None
    venv_python: Path | None
    editor_config_path: Path
    has_poetry_project: bool


class EnvironmentBootstrapService:
    def __init__(
        self,
        python_env_manager: PythonEnvironmentManager,
        dependency_manager: DependencyManager,
        editor_writer: EditorConfigWriter,
        logger: Logger,
    ):
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
        # Raises: ValueError if pyenv is not installed
        files.ensure_dir(project_root)

        self._validate_requirements()

        if self._is_environment_ready(project_root, python_version):
            self._logger.info("environment already configured")
            return self._get_existing_environment_result(project_root, python_version)

        python_path = self._setup_python_environment(project_root, python_version)
        self._install_python_dependencies(python_version)
        self._ensure_pyproject_exists(project_root, python_version)

        result = self._setup_with_poetry(
            project_root,
            python_path,
            python_version,
            install_dependencies,
        )

        return result

    def _validate_requirements(self) -> None:
        if not self._python_env.is_installed():
            raise ValueError("pyenv not found in PATH. Install pyenv first.")

    def _is_environment_ready(self, project_root: Path, python_version: str) -> bool:
        venv_path = project_root / ".venv"
        pyproject_path = project_root / "pyproject.toml"
        python_version_file = project_root / ".python-version"

        if not (
            venv_path.exists()
            and pyproject_path.exists()
            and python_version_file.exists()
        ):
            return False

        try:
            existing_version = python_version_file.read_text().strip()
            if existing_version != python_version:
                return False
        except Exception:
            return False

        venv_python = venv_path / "bin" / "python"
        if not venv_python.exists():
            return False

        return True

    def _get_existing_environment_result(
        self,
        project_root: Path,
        python_version: str,
    ) -> EnvironmentSetupResult:
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
        self._logger.info(f"[bold]Setting up Python {python_version}[/bold]")
        self._python_env.ensure_python(python_version)

        self._logger.info("Configuring pyenv local version")
        self._python_env.set_local(project_root, python_version)

        python_path = self._python_env.get_python_path(python_version)
        self._logger.success(f"Python configured: {python_path}")

        return python_path

    def _install_python_dependencies(self, python_version: str) -> None:
        self._logger.info("[bold]Installing Python tooling[/bold]")
        self._python_env.install_pip_packages(
            python_version,
            ["pip", "setuptools", "wheel", "poetry"],
        )
        self._logger.success("Python tooling installed")

    def _ensure_pyproject_exists(self, project_root: Path, python_version: str) -> None:
        pyproject_path = project_root / "pyproject.toml"

        if not pyproject_path.exists():
            self._logger.info("creating minimal pyproject.toml")
            files.create_minimal_pyproject(project_root, python_version=python_version)
            self._logger.success(f"created {pyproject_path}")
        else:
            updated = files.update_python_constraint(pyproject_path, python_version)
            if updated:
                version_parts = python_version.split(".")
                major_minor = f"{version_parts[0]}.{version_parts[1]}"
                self._logger.info(f"updated Python constraint to ^{major_minor}")

                poetry_lock = project_root / "poetry.lock"
                if poetry_lock.exists():
                    self._logger.info("removing old poetry.lock")
                    poetry_lock.unlink()

    def _setup_with_poetry(
        self,
        project_root: Path,
        python_path: Path,
        python_version: str,
        install_dependencies: bool,
    ) -> EnvironmentSetupResult:
        self._logger.info("[bold]Configuring Poetry environment[/bold]")
        self._deps.configure_venv(project_root)

        self._logger.info("Linking Poetry to Python version")
        self._deps.use_python(project_root, python_path)

        venv_path_dir = project_root / ".venv"
        if not venv_path_dir.exists():
            self._logger.info("Creating virtual environment")
            self._deps.install_dependencies(project_root)

        if install_dependencies:
            self._logger.info("[bold]Installing project dependencies[/bold]")
            self._deps.install_dependencies(project_root)

        venv_path = self._deps.get_venv_path(project_root)
        venv_python = self._deps.get_venv_python(project_root)

        self._logger.success(f"Virtual environment ready: {venv_path}")

        self._logger.info("Writing VSCode configuration")
        editor_config = self._editor.write_config(project_root, venv_python)
        self._logger.success(f"VSCode configured: {editor_config}")

        return EnvironmentSetupResult(
            python_version=python_version,
            python_path=python_path,
            venv_path=venv_path,
            venv_python=venv_python,
            editor_config_path=editor_config,
            has_poetry_project=True,
        )
