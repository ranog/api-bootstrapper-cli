from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from api_bootstrapper_cli.core.precommit_manager import PreCommitManager


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_create_precommit_config_file(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, versions = manager.create_config(tmp_path)

    assert config_path.exists()
    assert config_path.name == ".pre-commit-config.yaml"
    assert config_path.parent == tmp_path
    assert isinstance(versions, dict)


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_generate_valid_yaml_content(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "repos:" in content
    assert "repo:" in content


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_include_ruff_hooks(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "astral-sh/ruff-pre-commit" in content
    assert "id: ruff" in content
    assert "id: ruff-format" in content
    assert "--fix" in content
    assert "--exit-non-zero-on-fix" in content


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_include_commitizen_hooks(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "commitizen-tools/commitizen" in content
    assert "id: commitizen" in content
    assert "stages: [commit-msg]" in content


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_overwrite_existing_config(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')
    config_path = tmp_path / ".pre-commit-config.yaml"
    config_path.write_text("# Old configuration\nrepos: []")

    new_config_path, _ = manager.create_config(tmp_path)
    content = new_config_path.read_text()

    assert new_config_path == config_path
    assert "# Old configuration" not in content
    assert "astral-sh/ruff-pre-commit" in content


def test_should_raise_error_if_project_root_not_exists():
    manager = PreCommitManager()
    non_existent_path = Path("/non/existent/path")

    with pytest.raises(ValueError, match="Project root does not exist"):
        manager.create_config(non_existent_path)


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_return_correct_config_path(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _ = manager.create_config(tmp_path)

    assert config_path == tmp_path / ".pre-commit-config.yaml"


def test_should_extract_versions_from_pyproject(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_content = """\
[tool.poetry.group.dev.dependencies]
pre-commit = "^4.0.1"
ruff = "^0.15.1"
commitizen = "^4.13.8"
"""
    pyproject_path.write_text(pyproject_content)

    versions = manager._extract_versions_from_pyproject(tmp_path)

    assert "pre-commit" in versions
    assert "ruff" in versions
    assert "commitizen" in versions
    assert versions["pre-commit"] == "4.0.1"
    assert versions["ruff"] == "0.15.1"
    assert versions["commitizen"] == "4.13.8"


def test_should_extract_versions_without_caret(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_content = """\
[tool.poetry.group.dev.dependencies]
pre-commit = "4.5.0"
ruff = "0.16.0"
commitizen = "4.14.0"
"""
    pyproject_path.write_text(pyproject_content)

    versions = manager._extract_versions_from_pyproject(tmp_path)

    assert versions["pre-commit"] == "4.5.0"
    assert versions["ruff"] == "0.16.0"
    assert versions["commitizen"] == "4.14.0"


def test_should_return_empty_dict_when_no_pyproject_exists(tmp_path: Path):
    manager = PreCommitManager()

    versions = manager._extract_versions_from_pyproject(tmp_path)

    assert versions == {}


def test_should_return_empty_dict_when_no_dependencies_exist(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[tool.poetry]\nname = 'test'")

    versions = manager._extract_versions_from_pyproject(tmp_path)

    assert versions == {}


def test_should_handle_partial_version_matches(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_content = """\
[tool.poetry.group.dev.dependencies]
ruff = "^0.16.0"
"""
    pyproject_path.write_text(pyproject_content)

    versions = manager._extract_versions_from_pyproject(tmp_path)

    assert "ruff" in versions
    assert "commitizen" not in versions


def test_should_update_ruff_rev_in_config(tmp_path: Path):
    manager = PreCommitManager()
    config_path = tmp_path / ".pre-commit-config.yaml"

    config_content = """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: ""
    hooks:
      - id: ruff
"""
    config_path.write_text(config_content)

    versions = {"ruff": "0.16.0"}
    manager._update_config_versions(config_path, versions)

    content = config_path.read_text()
    assert 'rev: "v0.16.0"' in content


def test_should_update_commitizen_rev_in_config(tmp_path: Path):
    manager = PreCommitManager()
    config_path = tmp_path / ".pre-commit-config.yaml"

    config_content = """\
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: ""
    hooks:
      - id: commitizen
"""
    config_path.write_text(config_content)

    versions = {"commitizen": "4.14.0"}
    manager._update_config_versions(config_path, versions)

    content = config_path.read_text()
    assert 'rev: "v4.14.0"' in content


def test_should_update_both_versions_in_config(tmp_path: Path):
    manager = PreCommitManager()
    config_path = tmp_path / ".pre-commit-config.yaml"

    config_content = """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: ""
    hooks:
      - id: ruff
  - repo: https://github.com/commitizen-tools/commitizen
    rev: ""
    hooks:
      - id: commitizen
"""
    config_path.write_text(config_content)

    versions = {"ruff": "0.16.0", "commitizen": "4.14.0"}
    manager._update_config_versions(config_path, versions)

    content = config_path.read_text()
    assert 'rev: "v0.16.0"' in content
    assert 'rev: "v4.14.0"' in content


def test_should_skip_update_when_file_not_exists(tmp_path: Path):
    manager = PreCommitManager()
    config_path = tmp_path / ".pre-commit-config.yaml"

    versions = {"ruff": "0.16.0"}
    manager._update_config_versions(config_path, versions)


def test_should_handle_empty_versions_dict(tmp_path: Path):
    manager = PreCommitManager()
    config_path = tmp_path / ".pre-commit-config.yaml"
    config_path.write_text("repos:\n  - repo: test\n    rev: ''\n")

    manager._update_config_versions(config_path, {})

    assert config_path.exists()


def test_generate_config_should_return_string():
    manager = PreCommitManager()

    content = manager._generate_config_content()

    assert isinstance(content, str)
    assert len(content) > 0


def test_generate_config_should_have_empty_revisions():
    manager = PreCommitManager()

    content = manager._generate_config_content()

    assert 'rev: ""' in content


def test_generate_config_should_include_both_repos():
    manager = PreCommitManager()

    content = manager._generate_config_content()

    assert "astral-sh/ruff-pre-commit" in content
    assert "commitizen-tools/commitizen" in content


def test_generate_config_should_have_correct_hook_ids():
    manager = PreCommitManager()

    content = manager._generate_config_content()

    assert "id: ruff" in content
    assert "id: ruff-format" in content
    assert "id: commitizen" in content


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_write_dependencies_to_pyproject(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        """[tool.poetry]
name = "test"
version = "0.1.0"

[build-system]
requires = ["poetry-core"]
"""
    )

    manager._add_dependencies(tmp_path)

    content = pyproject_path.read_text()
    assert "[tool.poetry.group.dev.dependencies]" in content
    assert 'pre-commit = "^4.5.1"' in content
    assert 'ruff = "^0.15.2"' in content
    assert 'commitizen = "^4.13.8"' in content

    assert mock_exec.call_count == 2
    mock_exec.assert_any_call(
        ["poetry", "lock"],
        cwd=str(tmp_path),
        check=True,
    )
    mock_exec.assert_any_call(
        ["poetry", "install"],
        cwd=str(tmp_path),
        check=True,
    )


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_handle_missing_pyproject_file(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()

    with pytest.raises(FileNotFoundError, match="pyproject.toml not found"):
        manager._add_dependencies(tmp_path)


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_call_correct_command_to_install_hooks(
    mock_exec: MagicMock, tmp_path: Path
):
    manager = PreCommitManager()

    manager._install_hooks(tmp_path)

    mock_exec.assert_called_once_with(
        [
            "poetry",
            "run",
            "pre-commit",
            "install",
            "--hook-type",
            "pre-commit",
            "--hook-type",
            "commit-msg",
        ],
        cwd=str(tmp_path),
        check=True,
    )


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_handle_install_command_failure(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    mock_exec.side_effect = Exception("Command failed")

    manager._install_hooks(tmp_path)


@patch("api_bootstrapper_cli.core.precommit_manager.exec_cmd")
def test_should_execute_full_config_creation_flow(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = """\
[tool.poetry.group.dev.dependencies]
ruff = "^0.16.0"
commitizen = "^4.14.0"
"""
    pyproject_path.write_text(pyproject_content)

    config_path, versions = manager.create_config(tmp_path)

    assert config_path.exists()
    assert "ruff" in versions
    assert "commitizen" in versions
    assert mock_exec.call_count == 3
