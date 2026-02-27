from __future__ import annotations

import enum
import platform
from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.environment_service import (
    EnvironmentBootstrapService,
    EnvironmentSetupResult,
)
from api_bootstrapper_cli.core.logger import RichLogger
from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.shell import ShellError
from api_bootstrapper_cli.core.uv_dependency_manager import UvDependencyManager
from api_bootstrapper_cli.core.uv_python_manager import UvPythonManager
from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


class ManagerChoice(str, enum.Enum):
    """Supported environment / dependency manager backends."""

    pyenv = "pyenv"
    uv = "uv"


console = Console()


def bootstrap_env(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target project folder (default: current).",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    python_version: str = typer.Option(
        "3.12.12", "--python", help="Python version to configure."
    ),
    install: bool = typer.Option(
        True, "--install/--no-install", help="Run dependency installation."
    ),
    manager: ManagerChoice = typer.Option(
        ManagerChoice.pyenv,
        "--manager",
        help="Python environment / dependency manager backend.",
        case_sensitive=False,
    ),
) -> None:
    """Setup Python environment with a chosen manager and VSCode configuration.

    Creates or configures:
    - Python version (.python-version)
    - Virtual environment (.venv)
    - VSCode Python settings (.vscode/settings.json)
    - Minimal pyproject.toml (if doesn't exist)

    Supported managers: pyenv (default, uses Poetry) | uv
    """
    project_root = path.resolve()

    service = _create_bootstrap_service(manager)

    try:
        result = service.bootstrap(
            project_root=project_root,
            python_version=python_version,
            install_dependencies=install,
        )

        # Presentation layer: display result
        _display_success(result, manager)

    except (ValueError, RuntimeError, OSError, ShellError) as e:
        # Handle validation and operational errors without stacktrace
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


def _create_bootstrap_service(
    manager: ManagerChoice = ManagerChoice.pyenv,
) -> EnvironmentBootstrapService:
    """Factory: build the service with the chosen manager backend.

    Factory Pattern + Dependency Injection.
    Single point of creation – facilitates testing and implementation substitution.
    """
    if manager == ManagerChoice.uv:
        return EnvironmentBootstrapService(
            python_env_manager=UvPythonManager(),
            dependency_manager=UvDependencyManager(),
            editor_writer=VSCodeWriter(),
            logger=RichLogger(),
        )
    # Default: pyenv + Poetry
    return EnvironmentBootstrapService(
        python_env_manager=PyenvManager(),
        dependency_manager=PoetryManager(),
        editor_writer=VSCodeWriter(),
        logger=RichLogger(),
    )


def _display_success(
    result: EnvironmentSetupResult,
    manager: ManagerChoice = ManagerChoice.pyenv,
) -> None:
    console.print()
    console.print("[bold green]✓[/bold green] [green]Environment ready![/green]")

    if result.has_poetry_project and result.venv_path:
        venv_path_str = str(result.venv_path)

        console.print("[dim]To activate the virtual environment, run:[/dim]")

        if platform.system() == "Windows":
            console.print(
                f"  [cyan].\\{result.venv_path.name}\\Scripts\\activate[/cyan]\n"
                f"  [dim]# Or use: $(poetry env info --path)\\Scripts\\activate[/dim]"
                if manager == ManagerChoice.pyenv
                else f"  [cyan].\\{result.venv_path.name}\\Scripts\\activate[/cyan]"
            )
        else:
            has_special_chars = " " in venv_path_str or any(
                ord(c) > 127 for c in venv_path_str
            )

            if manager == ManagerChoice.uv:
                # uv always creates an in-project .venv; direct path is reliable
                console.print(f"  [cyan]source {venv_path_str}/bin/activate[/cyan]")
            elif has_special_chars:
                console.print(
                    f"  [cyan]source $(poetry env info --path)/bin/activate[/cyan]\n"
                    f"  [dim]# Alternative (if path has spaces/accents):[/dim]\n"
                    f"  [dim]source '{venv_path_str}/bin/activate'[/dim]"
                )
            else:
                console.print(
                    f"  [cyan]source {venv_path_str}/bin/activate[/cyan]\n"
                    f"  [dim]# Or use: source $(poetry env info --path)/bin/activate[/dim]"
                )

    console.print()
