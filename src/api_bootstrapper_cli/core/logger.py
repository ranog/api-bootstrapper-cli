from __future__ import annotations

from dataclasses import dataclass, field

from rich.console import Console


@dataclass
class RichLogger:
    _console: Console = field(default_factory=Console)

    def debug(self, message: str) -> None:
        self._console.print(f"[dim]{message}[/dim]")

    def info(self, message: str) -> None:
        self._console.print(f"[cyan]{message}[/cyan]")

    def success(self, message: str) -> None:
        self._console.print(f"[green]{message}[/green]")

    def warning(self, message: str) -> None:
        self._console.print(f"[yellow]{message}[/yellow]")

    def error(self, message: str) -> None:
        self._console.print(f"[red]{message}[/red]")

    def print(self, message: str) -> None:
        self._console.print(message)


# Default logger instance
logger = RichLogger()
