from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.alembic_manager import AlembicManager
from api_bootstrapper_cli.core.protocols import ManagerChoice


console = Console()


def add_alembic(
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
        help="Dependency manager backend for Alembic commands (auto-detect by default).",
        case_sensitive=False,
    ),
    with_db: bool = typer.Option(
        False,
        "--with-db",
        help="Start local PostgreSQL service (`db`) via docker compose before migrations.",
    ),
    create_initial_items: bool = typer.Option(
        False,
        "--create-initial-items",
        help="Generate an initial migration for the sample Item model.",
    ),
    upgrade_head: bool = typer.Option(
        False,
        "--upgrade-head",
        help="Run `alembic upgrade head` after setup (and revision generation, if selected).",
    ),
) -> None:
    """Add Alembic database migrations support to the project."""
    project_root = path.resolve()

    try:
        manager_instance = AlembicManager()
        setup_result = manager_instance.setup(project_root, manager=manager)

        should_start_db = with_db or create_initial_items or upgrade_head
        if should_start_db:
            manager_instance.ensure_database_running(project_root)

        if create_initial_items:
            manager_instance.create_initial_items_revision(
                project_root,
                setup_result.manager,
            )

        if upgrade_head:
            manager_instance.upgrade_head(project_root, setup_result.manager)

        console.print()
        if setup_result.initialized_now:
            console.print(
                "[bold green]✓[/bold green] [green]Alembic initialized![/green]"
            )
        else:
            console.print(
                "[bold yellow]ℹ[/bold yellow] "
                "[yellow]Alembic already initialized. Configuration refreshed.[/yellow]"
            )

        console.print(f"[dim]Config:[/dim] {setup_result.config_path}")
        console.print(f"[dim]Env:[/dim] {setup_result.env_path}")
        console.print(f"[dim]Versions:[/dim] {setup_result.versions_path}")

        if should_start_db:
            console.print("[dim]Database:[/dim] db service is up")
        if create_initial_items:
            console.print(
                '[dim]Revision:[/dim] created with message "create items table"'
            )
        if upgrade_head:
            console.print("[dim]Migration:[/dim] upgrade head applied")

        alembic_prefix = (
            "uv run alembic"
            if setup_result.manager == ManagerChoice.uv
            else "poetry run alembic"
        )

        console.print()
        console.print("[bold]Next steps:[/bold]")
        console.print(
            f'  1. [cyan]{alembic_prefix} revision --autogenerate -m "initial"[/cyan]'
        )
        console.print(f"  2. [cyan]{alembic_prefix} upgrade head[/cyan]")
        console.print()

    except (FileNotFoundError, ValueError, RuntimeError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1) from error
