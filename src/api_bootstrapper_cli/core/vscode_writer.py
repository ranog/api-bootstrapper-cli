from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.files import ensure_dir, read_text, write_text


@dataclass(frozen=True)
class VSCodeWriter:
    def write_python_interpreter(self, project_root: Path, python_path: Path) -> Path:
        vscode_dir = project_root / ".vscode"
        ensure_dir(vscode_dir)
        settings_path = vscode_dir / "settings.json"

        existing = {}
        if settings_path.exists():
            try:
                existing = json.loads(read_text(settings_path))
            except Exception:
                existing = {}
        try:
            relative_path = python_path.relative_to(project_root)
            existing["python.defaultInterpreterPath"] = str(relative_path)
        except ValueError:
            existing["python.defaultInterpreterPath"] = str(python_path)

        existing.setdefault("python.testing.pytestArgs", ["-s", "-vv"])
        existing.setdefault("python.testing.unittestEnabled", False)
        existing.setdefault("python.testing.pytestEnabled", True)
        existing.setdefault(
            "[python]",
            {
                "editor.defaultFormatter": "ms-python.python",
                "editor.formatOnType": True,
                "editor.rulers": [88],
            },
        )

        write_text(settings_path, json.dumps(existing, indent=2) + "\n", overwrite=True)
        return settings_path
