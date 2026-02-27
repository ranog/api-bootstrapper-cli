"""Command to initialize a complete Python project with all features."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.commands.add_pre_commit import add_pre_commit
from api_bootstrapper_cli.commands.bootstrap_env import ManagerChoice, bootstrap_env
from api_bootstrapper_cli.core.shell import ShellError


console = Console()


def init(
    python: str = typer.Option(..., "--python", "-p", help="Python version to install"),
    path: Path = typer.Option(
        Path.cwd(),
        "--path",
        help="Project directory path",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    install: bool = typer.Option(
        True,
        "--install/--no-install",
        help="Install dependencies after environment setup",
    ),
    manager: ManagerChoice = typer.Option(
        ManagerChoice.pyenv,
        "--manager",
        help="Python environment / dependency manager backend.",
        case_sensitive=False,
    ),
) -> None:
    """
    Initialize a complete Python project with all features.

    This command combines bootstrap-env and add-pre-commit in a single workflow,
    setting up a fully configured Python development environment.

    What it does:

    \b
    1. Sets up Python environment (pyenv + Poetry + VSCode)
    2. Configures pre-commit hooks (Ruff + Commitizen)

    Example usage:

    \b
    # Initialize new project
    api-bootstrapper init --python 3.12.12 --path ./my-project

    \b
    # Initialize in current directory
    api-bootstrapper init --python 3.13.9

    \b
    # Skip dependency installation
    api-bootstrapper init --python 3.12.12 --no-install
    """
    console.print("\n[bold cyan]🚀 Initializing Python project...[/bold cyan]\n")

    try:
        # Step 1: Bootstrap environment
        console.print("[bold]Step 1/2:[/bold] Setting up Python environment")
        bootstrap_env(
            python_version=python, path=path, install=install, manager=manager
        )

        # Step 2: Add pre-commit
        console.print("\n[bold]Step 2/2:[/bold] Configuring pre-commit hooks")
        add_pre_commit(path=path)

        # Success summary
        console.print(
            "\n[bold green]✓ Project initialized successfully![/bold green]\n"
        )
        console.print("[bold]Next steps:[/bold]")
        console.print(f"  1. cd {path}")
        console.print("  2. source .venv/bin/activate")
        console.print("  3. Start coding!\n")

    except (ValueError, RuntimeError, OSError, ShellError) as e:
        console.print(f"\n[bold red]✗ Initialization failed:[/bold red] {e}\n")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(
            f"\n[bold red]✗ Initialization failed (unexpected):[/bold red] {e}\n"
        )
        raise typer.Exit(1) from e
