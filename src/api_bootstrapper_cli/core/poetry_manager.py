from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.shell import exec_cmd


@dataclass(frozen=True)
class PoetryManager:
    def ensure_installed(self) -> None:
        exec_cmd(["poetry", "--version"], check=True)

    def set_in_project_venv(self, project_root: Path, enabled: bool = True) -> None:
        value = "true" if enabled else "false"
        exec_cmd(
            ["poetry", "config", "virtualenvs.in-project", value, "--local"],
            cwd=str(project_root),
            check=True,
        )

    def env_use(self, project_root: Path, python_path: Path) -> None:
        exec_cmd(
            ["poetry", "env", "use", str(python_path)],
            cwd=str(project_root),
            check=True,
        )

    def env_path(self, project_root: Path) -> Path:
        res = exec_cmd(["poetry", "env", "info", "-p"], cwd=str(project_root), check=True)
        return Path(res.stdout.strip())

    def install(self, project_root: Path) -> None:
        exec_cmd(["poetry", "install"], cwd=str(project_root), check=True)
