from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.mypy_manager import MypyManager
from api_bootstrapper_cli.core.protocols import ManagerChoice


console = Console()


def add_mypy(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target project folder (default: current).",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    manager: ManagerChoice | None = typer.Option(
        None,
        "--manager",
        help="Dependency manager backend for mypy setup (auto-detect by default).",
        case_sensitive=False,
    ),
) -> None:
    """Add mypy type-checking configuration to the project."""
    project_root = path.resolve()

    try:
        manager_instance = MypyManager()
        setup_result = manager_instance.setup(project_root, manager=manager)

        console.print()
        if setup_result.config_already_existed:
            console.print(
                "[bold yellow]ℹ[/bold yellow] [yellow]Mypy config already exists[/yellow]"
            )
            console.print("[dim]Dependencies have been updated if needed[/dim]")
        else:
            console.print("[bold green]✓[/bold green] [green]Mypy configured![/green]")

        console.print(
            f"[dim]Config:[/dim] {setup_result.pyproject_path.relative_to(project_root)}"
        )

        if setup_result.version:
            console.print(f"[dim]Installed mypy version:[/dim] {setup_result.version}")

        mypy_cmd = (
            "uv run mypy src"
            if setup_result.manager == ManagerChoice.uv
            else "poetry run mypy src"
        )

        console.print()
        console.print("[bold]Next step:[/bold]")
        console.print(f"  [cyan]{mypy_cmd}[/cyan]")
        console.print()

    except (FileNotFoundError, ValueError, RuntimeError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1) from error
