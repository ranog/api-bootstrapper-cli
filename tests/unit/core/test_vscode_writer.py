from __future__ import annotations

import json
from pathlib import Path

from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


def test_should_create_vscode_directory(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3")

    writer.write_config(tmp_path, python_path)

    vscode_dir = tmp_path / ".vscode"

    assert vscode_dir.exists()
    assert vscode_dir.is_dir()


def test_should_write_python_interpreter_setting(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/home/user/.venv/bin/python")

    settings_path = writer.write_config(tmp_path, python_path)

    assert json.loads(settings_path.read_text())[
        "python.defaultInterpreterPath"
    ] == str(python_path)


def test_should_enable_pytest_by_default(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3")

    settings_path = writer.write_config(tmp_path, python_path)

    settings = json.loads(settings_path.read_text())

    assert settings["python.testing.pytestEnabled"] is True
    assert settings["python.testing.unittestEnabled"] is False
    assert settings["python.testing.pytestArgs"] == ["-s", "-vv"]
    assert "[python]" in settings
    assert settings["[python]"]["editor.defaultFormatter"] == "ms-python.python"
    assert settings["[python]"]["editor.formatOnType"] is True
    assert settings["[python]"]["editor.rulers"] == [88]


def test_should_merge_with_existing_settings(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"
    settings_file.write_text(json.dumps({"editor.fontSize": 14, "editor.tabSize": 4}))
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3")

    writer.write_config(tmp_path, python_path)

    settings = json.loads(settings_file.read_text())

    assert settings["editor.fontSize"] == 14
    assert settings["editor.tabSize"] == 4
    assert "python.defaultInterpreterPath" in settings


def test_should_handle_corrupt_existing_settings(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"
    settings_file.write_text("{ invalid json }")
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3")

    settings_path = writer.write_config(tmp_path, python_path)

    assert "python.defaultInterpreterPath" in json.loads(settings_path.read_text())


def test_should_return_settings_file_path(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3")

    settings_path = writer.write_config(tmp_path, python_path)

    assert settings_path == tmp_path / ".vscode" / "settings.json"
    assert settings_path.exists()
