from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.files import ensure_dir, read_text, write_text


@dataclass(frozen=True)
class VSCodeWriter:
    def write_config(self, project_root: Path, python_path: Path) -> Path:
        settings_path = self._get_settings_path(project_root)
        self._ensure_vscode_dir(project_root)

        settings = self._load_existing_settings(settings_path)
        settings = self._update_settings(settings, project_root, python_path)

        self._write_settings(settings_path, settings)
        return settings_path

    def _get_settings_path(self, project_root: Path) -> Path:
        return project_root / ".vscode" / "settings.json"

    def _ensure_vscode_dir(self, project_root: Path) -> None:
        vscode_dir = project_root / ".vscode"
        ensure_dir(vscode_dir)

    def _load_existing_settings(self, settings_path: Path) -> dict:
        if not settings_path.exists():
            return {}

        try:
            return (
                result
                if isinstance(result := json.loads(read_text(settings_path)), dict)
                else {}
            )
        except Exception:
            return {}

    def _update_settings(
        self,
        settings: dict,
        project_root: Path,
        python_path: Path,
    ) -> dict:
        settings["python.defaultInterpreterPath"] = self._get_interpreter_path(
            project_root, python_path
        )

        settings.setdefault("python.testing.pytestArgs", ["-s", "-vv"])
        settings.setdefault("python.testing.unittestEnabled", False)
        settings.setdefault("python.testing.pytestEnabled", True)

        settings.setdefault(
            "[python]",
            {
                "editor.defaultFormatter": "ms-python.python",
                "editor.formatOnType": True,
                "editor.rulers": [88],
            },
        )

        return settings

    def _get_interpreter_path(self, project_root: Path, python_path: Path) -> str:
        try:
            relative_path = python_path.relative_to(project_root)
            return str(relative_path)
        except ValueError:
            return str(python_path)

    def _write_settings(self, settings_path: Path, settings: dict) -> None:
        content = json.dumps(settings, indent=2) + "\n"
        write_text(settings_path, content, overwrite=True)
