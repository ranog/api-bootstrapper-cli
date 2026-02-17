from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


@dataclass(frozen=True)
class PyenvManager:
    def is_installed(self) -> bool:
        try:
            exec_cmd(["pyenv", "--version"], check=True)
            return True
        except ShellError:
            return False

    def versions(self) -> set[str]:
        res = exec_cmd(["pyenv", "versions", "--bare"], check=True)
        return {line.strip() for line in res.stdout.splitlines() if line.strip()}

    def ensure_python(self, version: str) -> None:
        if version in self.versions():
            return

        exec_cmd(["pyenv", "install", "-s", version], check=True)

    def set_local(self, project_root: Path, version: str) -> None:
        exec_cmd(["pyenv", "local", version], cwd=str(project_root), check=True)

    def python_path(self, version: str) -> Path:
        res = exec_cmd(["pyenv", "which", "python"], check=True)
        return Path(res.stdout.strip())
