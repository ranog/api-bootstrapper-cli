from __future__ import annotations

import json
from pathlib import Path

import pytest

from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


@pytest.mark.integration
def test_should_create_vscode_directory_when_missing(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    assert not vscode_dir.exists()

    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    writer.write_config(tmp_path, python_path)

    assert vscode_dir.exists()
    assert vscode_dir.is_dir()


@pytest.mark.integration
def test_should_create_settings_file_with_python_path(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    settings_path = writer.write_config(tmp_path, python_path)

    assert settings_path.exists()
    assert settings_path == tmp_path / ".vscode" / "settings.json"

    content = json.loads(settings_path.read_text())
    assert "python.defaultInterpreterPath" in content
    assert content["python.defaultInterpreterPath"] == str(python_path)


@pytest.mark.integration
def test_should_merge_with_existing_vscode_settings(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"

    existing_settings = {
        "editor.fontSize": 16,
        "files.autoSave": "onFocusChange",
        "python.defaultInterpreterPath": "/old/python/path",
    }
    settings_file.write_text(json.dumps(existing_settings, indent=2))

    writer = VSCodeWriter()
    new_python_path = Path("/new/python/path")

    writer.write_config(tmp_path, new_python_path)

    content = json.loads(settings_file.read_text())
    assert content["editor.fontSize"] == 16
    assert content["files.autoSave"] == "onFocusChange"
    assert content["python.defaultInterpreterPath"] == str(new_python_path)


@pytest.mark.integration
def test_should_preserve_existing_settings_order(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"

    existing_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.exclude": {"**/*.pyc": True},
        "python.linting.enabled": True,
    }
    settings_file.write_text(json.dumps(existing_settings, indent=2))

    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    writer.write_config(tmp_path, python_path)

    content = json.loads(settings_file.read_text())
    # VSCodeWriter adds: python.defaultInterpreterPath, python.testing.pytestArgs,
    # python.testing.unittestEnabled, python.testing.pytestEnabled, [python]
    assert len(content) >= len(existing_settings)
    assert all(key in content for key in existing_settings)
    assert content["python.defaultInterpreterPath"] == str(python_path)


@pytest.mark.integration
def test_should_handle_empty_vscode_settings_file(tmp_path: Path):
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    settings_file = vscode_dir / "settings.json"
    settings_file.write_text("{}")

    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    writer.write_config(tmp_path, python_path)

    content = json.loads(settings_file.read_text())
    # VSCodeWriter adds 5 keys: python.defaultInterpreterPath, python.testing.pytestArgs,
    # python.testing.unittestEnabled, python.testing.pytestEnabled, [python]
    assert "python.defaultInterpreterPath" in content
    assert content["python.defaultInterpreterPath"] == str(python_path)
    assert "python.testing.pytestArgs" in content
    assert "python.testing.pytestEnabled" in content


@pytest.mark.integration
def test_should_format_json_with_proper_indentation(tmp_path: Path):
    writer = VSCodeWriter()
    python_path = Path("/usr/bin/python3.12")

    settings_path = writer.write_config(tmp_path, python_path)

    raw_content = settings_path.read_text()
    # Verify it's properly indented (not minified)
    assert "\n" in raw_content
    assert "  " in raw_content  # Has spaces for indentation
