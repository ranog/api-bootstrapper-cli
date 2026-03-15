from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from api_bootstrapper_cli.core.files import create_dockerfile


console = Console()


def add_docker(
    path: Path = typer.Option(
        Path("."),
        "--path",
        help="Project directory path",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    python_version: str = typer.Option(
        "3.13",
        "--python",
        help="Python version for Docker image (e.g., 3.13, 3.12)",
    ),
) -> None:
    """
    Add Dockerfile to a Python project.

    Creates a multi-stage Dockerfile optimized for Python applications using uvicorn.

    Example usage:

    \b
    # Add Dockerfile with default Python 3.13
    api-bootstrapper add-docker

    \b
    # Add Dockerfile with specific Python version
    api-bootstrapper add-docker --python 3.12

    \b
    # Add Dockerfile to specific project
    api-bootstrapper add-docker --path ./my-project --python 3.13
    """
    project_root = path.resolve()

    try:
        console.print("\n[bold cyan]🐳 Adding Docker support...[/bold cyan]\n")

        dockerfile_path = project_root / "Dockerfile"

        if dockerfile_path.exists():
            console.print(
                f"[yellow]⚠ Dockerfile already exists at {dockerfile_path}[/yellow]"
            )
            console.print("Skipping creation to avoid overwriting.\n")
            return

        create_dockerfile(project_root, python_version=python_version)

        console.print(f"[green]✓ Created Dockerfile (Python {python_version})[/green]")
        console.print(f"  Location: {dockerfile_path}\n")

        console.print("[bold]Next steps:[/bold]")
        console.print("  1. Create requirements.txt with your dependencies")
        console.print("  2. Ensure src/main.py exists with your FastAPI app")
        console.print("  3. Build: docker build -t my-app .")
        console.print("  4. Run: docker run -p 8080:8080 my-app\n")

    except (ValueError, RuntimeError, OSError) as e:
        console.print(f"\n[bold red]✗ Failed to add Docker support:[/bold red] {e}\n")
        raise typer.Exit(1) from e
