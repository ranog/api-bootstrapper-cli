from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

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
    project_root = path.resolve()

    pyenv = PyenvManager()
    poetry = PoetryManager()
    vscode = VSCodeWriter()

    if not pyenv.is_installed():
        raise typer.BadParameter("pyenv not found in PATH. Install pyenv first.")

    console.print(f"[cyan]pyenv[/cyan] ensure python {python_version}")
    pyenv.ensure_python(python_version)

    console.print(f"[cyan]pyenv[/cyan] set local {python_version} in {project_root}")
    pyenv.set_local(project_root, python_version)

    python_path = pyenv.python_path(python_version)
    console.print(f"[green]python[/green] {python_path}")

    pyproject_file = project_root / "pyproject.toml"
    has_poetry_project = pyproject_file.exists()

    if has_poetry_project:
        console.print("[cyan]poetry[/cyan] ensure installed")
        poetry.ensure_installed()

        console.print("[cyan]poetry[/cyan] set in-project venv (.venv)")
        poetry.set_in_project_venv(project_root, enabled=True)

        console.print("[cyan]poetry[/cyan] use python")
        poetry.env_use(project_root, python_path)

        if install:
            console.print("[cyan]poetry[/cyan] install")
            poetry.install(project_root)

        venv_path = poetry.env_path(project_root)
        console.print(f"[green]venv[/green] {venv_path}")

        venv_python = venv_path / "bin" / "python"
        if not venv_python.exists():
            venv_python = venv_path / "Scripts" / "python.exe"

        settings_path = vscode.write_python_interpreter(project_root, venv_python)
        console.print(f"[green]vscode[/green] wrote {settings_path}")

        console.print()
        console.print("[bold green]✓[/bold green] [green]Environment ready![/green]")
        console.print(
            "[dim]To activate the virtual environment, run:[/dim]\n"
            "  [cyan]source $(poetry env info --path)/bin/activate[/cyan]"
        )
        console.print()
    else:
        console.print(
            "[yellow]warning[/yellow] no pyproject.toml found, skipping poetry setup"
        )
        console.print(
            f"[dim]run 'poetry init' in {project_root} to create a Poetry project[/dim]"
        )

        settings_path = vscode.write_python_interpreter(project_root, python_path)
        console.print(f"[green]vscode[/green] wrote {settings_path}")
