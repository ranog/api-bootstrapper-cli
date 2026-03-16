from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.skills_installer import install_agentskills


console = Console()


def install_agent_skills(
    target: Path | None = typer.Option(
        None,
        "--target",
        help="Custom destination for Agent Skills (defaults to $AGENT_SKILLS_HOME or ~/.agent-skills).",
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
    """Install bundled Agent Skills to a local Agent Skills directory."""
    try:
        result = install_agentskills(target_root=target, overwrite=overwrite)
        bundled_skills_count = (
            len(result.installed_skills)
            + len(result.overwritten_skills)
            + len(result.skipped_skills)
        )

        console.print()
        console.print(
            "[bold green]✓[/bold green] [green]Agent Skills installed[/green]"
        )
        console.print(f"[dim]Source:[/dim] {result.source_root}")
        console.print(f"[dim]Target:[/dim] {result.target_root}")

        console.print(
            f"[dim]Installed:[/dim] {len(result.installed_skills)} | "
            f"[dim]Overwritten:[/dim] {len(result.overwritten_skills)} | "
            f"[dim]Skipped:[/dim] {len(result.skipped_skills)}"
        )
        console.print(
            f"[dim]Bundled api-bootstrapper skills in this release:[/dim] {bundled_skills_count}"
        )
        console.print(
            "[dim]Note:[/dim] This command installs only bundled api-bootstrapper skills. System skills are managed separately."
        )

        if result.skipped_skills:
            console.print("[yellow]Skipped skills (already existed):[/yellow]")
            for skill_name in result.skipped_skills:
                console.print(f"  - {skill_name}")

        console.print()

    except (RuntimeError, OSError, ValueError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1) from error
