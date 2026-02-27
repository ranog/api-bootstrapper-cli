from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.pre_commit_manager import PreCommitManager
from api_bootstrapper_cli.core.protocols import ManagerChoice


console = Console()


def add_pre_commit(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Target project folder (default: current).",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    manager: ManagerChoice | None = None,
) -> None:
    """Add pre-commit configuration with Ruff and Commitizen hooks.

    Args:
        path: Target project folder
        manager: Optional manager choice. If None, auto-detect from pyproject.toml
    """
    project_root = path.resolve()

    try:
        manager_instance = PreCommitManager()
        config_path, versions, config_already_existed = manager_instance.create_config(
            project_root, manager
        )

        console.print()
        if config_already_existed:
            console.print(
                "[bold yellow]ℹ[/bold yellow] [yellow]Pre-commit config already exists[/yellow]"
            )
            console.print(
                f"[dim]Existing file preserved:[/dim] {config_path.relative_to(project_root)}"
            )
            console.print(
                "[dim]Dependencies and hooks have been updated if needed[/dim]"
            )
        else:
            console.print(
                "[bold green]✓[/bold green] [green]Pre-commit configured![/green]"
            )
            console.print(
                f"[dim]Created:[/dim] {config_path.relative_to(project_root)}"
            )

        if versions:
            console.print()
            console.print("[dim]Installed versions:[/dim]")
            for package, version in versions.items():
                console.print(f"  • {package}: [cyan]{version}[/cyan]")

        console.print()

        git_hooks_dir = project_root / ".git" / "hooks"
        if git_hooks_dir.exists():
            console.print("[bold green]✓[/bold green] [green]Hooks installed![/green]")
            console.print("[dim]Pre-commit will now run automatically on commits[/dim]")
        else:
            console.print("[yellow]⚠[/yellow] [dim]Not a git repository[/dim]")
            console.print("[dim]To enable hooks after git init, run:[/dim]")
            console.print(
                "  [cyan]poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg[/cyan]"
            )

        console.print()

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(code=1)
