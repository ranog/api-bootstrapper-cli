from __future__ import annotations

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
from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


console = Console()


def bootstrap_env(
    path: Path = typer.Option(
        Path("."), "--path", help="Target project folder (default: current)."
    ),
    python_version: str = typer.Option(
        "3.12.12", "--python", help="Python version to use via pyenv."
    ),
    install: bool = typer.Option(
        True, "--install/--no-install", help="Run 'poetry install'."
    ),
) -> None:
    """Setup Python environment with pyenv, Poetry, and VSCode configuration.

    Creates or configures:
    - Python version via pyenv (.python-version)
    - Poetry virtual environment (.venv)
    - VSCode Python settings (.vscode/settings.json)
    - Minimal pyproject.toml (if doesn't exist)
    """
    project_root = path.resolve()

    # Dependency Injection: create concrete instances
    service = _create_bootstrap_service()

    try:
        # Delegate all business logic to the service layer
        result = service.bootstrap(
            project_root=project_root,
            python_version=python_version,
            install_dependencies=install,
        )

        # Presentation layer: display result
        _display_success(result)

    except ValueError as e:
        # Handle validation errors
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


def _create_bootstrap_service() -> EnvironmentBootstrapService:
    """Factory to create the service with its injected dependencies.

    Factory Pattern + Dependency Injection.
    Single point of creation - facilitates testing and implementation substitution.
    """
    return EnvironmentBootstrapService(
        python_env_manager=PyenvManager(),
        dependency_manager=PoetryManager(),
        editor_writer=VSCodeWriter(),
        logger=RichLogger(),
    )


def _display_success(result: EnvironmentSetupResult) -> None:
    """Display success message to the user.

    Presentation responsibility separated from logic.
    """
    console.print()
    console.print("[bold green]✓[/bold green] [green]Environment ready![/green]")

    if result.has_poetry_project and result.venv_path:
        console.print(
            "[dim]To activate the virtual environment, run:[/dim]\n"
            f"  [cyan]source {result.venv_path}/bin/activate[/cyan]"
        )

    console.print()
