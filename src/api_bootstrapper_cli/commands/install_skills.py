from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.skills_installer import install_codex_skills


console = Console()


def install_skills(
    target: Path | None = typer.Option(
        None,
        "--target",
        help="Custom destination for Codex skills (defaults to $CODEX_HOME/skills or ~/.codex/skills).",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    overwrite: bool = typer.Option(
        True,
        "--overwrite/--no-overwrite",
        help="Overwrite existing skill folders when already present.",
    ),
) -> None:
    """Install bundled Codex skills to the local Codex skills directory."""
    try:
        result = install_codex_skills(target_root=target, overwrite=overwrite)

        console.print()
        console.print("[bold green]✓[/bold green] [green]Skills installed[/green]")
        console.print(f"[dim]Source:[/dim] {result.source_root}")
        console.print(f"[dim]Target:[/dim] {result.target_root}")

        console.print(
            f"[dim]Installed:[/dim] {len(result.installed_skills)} | "
            f"[dim]Overwritten:[/dim] {len(result.overwritten_skills)} | "
            f"[dim]Skipped:[/dim] {len(result.skipped_skills)}"
        )

        if result.skipped_skills:
            console.print("[yellow]Skipped skills (already existed):[/yellow]")
            for skill_name in result.skipped_skills:
                console.print(f"  - {skill_name}")

        console.print()

    except (RuntimeError, OSError, ValueError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1) from error
