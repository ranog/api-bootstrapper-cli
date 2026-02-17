from __future__ import annotations

import subprocess
from dataclasses import dataclass


class ShellError(Exception):
    pass


@dataclass(frozen=True)
class CommandResult:
    stdout: str
    stderr: str
    returncode: int


def exec_cmd(
    cmd: list[str],
    cwd: str | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> CommandResult:
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            env=env,
        )
        return CommandResult(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
        )
    except subprocess.CalledProcessError as e:
        raise ShellError(
            f"Command failed: {' '.join(cmd)}\nExit code: {e.returncode}\n{e.stderr}"
        ) from e
