from __future__ import annotations

import subprocess
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

        result = self._setup_dependency_environment(
            project_root,
            python_path,
            python_version,
            install_dependencies,
        )

        return result

    def _validate_requirements(self) -> None:
        python_mgr = getattr(self._python_env, "name", "python environment manager")
        if not self._python_env.is_installed():
            raise ValueError(
                f"{python_mgr} not found in PATH. Install {python_mgr} first."
            )
        dep_mgr = getattr(self._deps, "name", "dependency manager")
        if not self._deps.is_installed():
            raise ValueError(f"{dep_mgr} not found in PATH. Install {dep_mgr} first.")

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

        try:
            version_parts = python_version.split(".")
            expected_major_minor = f"{version_parts[0]}.{version_parts[1]}"
            result = subprocess.run(
                [str(venv_python), "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            # Output format: "Python X.Y.Z"
            venv_version_str = result.stdout.strip() or result.stderr.strip()
            if not venv_version_str.startswith("Python "):
                return False
            venv_major_minor = ".".join(venv_version_str.split()[1].split(".")[:2])
            if venv_major_minor != expected_major_minor:
                return False
        except Exception:
            return False

        return True

    def _get_existing_environment_result(
        self,
        project_root: Path,
        python_version: str,
    ) -> EnvironmentSetupResult:
        venv_path = self._deps.get_venv_path(project_root)
        venv_python = self._deps.get_venv_python(project_root)
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
        self._logger.info(f"[bold][env] Setting up Python {python_version}[/bold]")
        self._python_env.ensure_python(python_version)

        self._logger.info("[env] Configuring pyenv local version")
        self._python_env.set_local(project_root, python_version)

        python_path = self._python_env.get_python_path(python_version)
        self._logger.success(f"[env] Python configured: {python_path}")

        return python_path

    def _install_python_dependencies(self, python_version: str) -> None:
        self._logger.info("[bold][env] Installing Python tooling[/bold]")
        self._python_env.install_pip_packages(
            python_version,
            ["pip", "setuptools", "wheel", "poetry"],
        )
        self._logger.success("[env] Python tooling installed")

    def _ensure_pyproject_exists(self, project_root: Path, python_version: str) -> None:
        dep_mgr = getattr(self._deps, "name", "deps")
        use_pep621 = dep_mgr == "uv"
        pyproject_path = project_root / "pyproject.toml"

        if not pyproject_path.exists():
            self._logger.info(f"[{dep_mgr}] Creating minimal pyproject.toml")
            files.create_minimal_pyproject(
                project_root,
                python_version=python_version,
                use_pep621=use_pep621,
            )
            self._logger.success(f"[{dep_mgr}] Created {pyproject_path}")
        else:
            updated = files.update_python_constraint(pyproject_path, python_version)
            if updated:
                version_parts = python_version.split(".")
                major_minor = f"{version_parts[0]}.{version_parts[1]}"
                constraint = f">={major_minor}" if use_pep621 else f"^{major_minor}"
                self._logger.info(
                    f"[{dep_mgr}] Updated Python constraint to {constraint}"
                )

                lock_file_name = "uv.lock" if use_pep621 else "poetry.lock"
                lock_file = project_root / lock_file_name
                if lock_file.exists():
                    self._logger.info(f"[{dep_mgr}] Removing old {lock_file_name}")
                    try:
                        lock_file.unlink()
                    except OSError as e:
                        self._logger.warning(
                            f"[{dep_mgr}] Could not remove {lock_file_name}: {e}. "
                            "Remove it manually before proceeding."
                        )

    def _setup_dependency_environment(
        self,
        project_root: Path,
        python_path: Path,
        python_version: str,
        install_dependencies: bool,
    ) -> EnvironmentSetupResult:
        dep_mgr = getattr(self._deps, "name", "deps")
        self._logger.info(f"[bold][{dep_mgr}] Configuring {dep_mgr} environment[/bold]")
        self._deps.configure_venv(project_root)

        self._logger.info(f"[{dep_mgr}] Linking to Python version")
        self._deps.use_python(project_root, python_path)

        venv_path_dir = self._deps.get_venv_path(project_root)
        if not venv_path_dir.exists():
            self._logger.info(f"[{dep_mgr}] Creating virtual environment")
            self._deps.ensure_venv(project_root)

        if install_dependencies:
            self._logger.info(
                f"[bold][{dep_mgr}] Installing project dependencies[/bold]"
            )
            self._deps.install_dependencies(project_root)

        venv_path = self._deps.get_venv_path(project_root)
        venv_python = self._deps.get_venv_python(project_root)

        self._logger.success(f"[{dep_mgr}] Virtual environment ready: {venv_path}")

        self._logger.info("[vscode] Writing VSCode configuration")
        editor_config = self._editor.write_config(project_root, venv_python)
        self._logger.success(f"[vscode] VSCode configured: {editor_config}")

        return EnvironmentSetupResult(
            python_version=python_version,
            python_path=python_path,
            venv_path=venv_path,
            venv_python=venv_python,
            editor_config_path=editor_config,
            has_poetry_project=True,
        )
