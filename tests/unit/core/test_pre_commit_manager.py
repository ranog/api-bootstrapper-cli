from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from api_bootstrapper_cli.core.pre_commit_manager import PreCommitManager
from api_bootstrapper_cli.core.protocols import ManagerChoice


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_create_pre_commit_config_file(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, versions, already_existed = manager.create_config(tmp_path)

    assert config_path.exists()
    assert config_path.name == ".pre-commit-config.yaml"
    assert config_path.parent == tmp_path
    assert isinstance(versions, dict)
    assert already_existed is False


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_generate_valid_yaml_content(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "repos:" in content
    assert "repo:" in content


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_include_ruff_hooks(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "astral-sh/ruff-pre-commit" in content
    assert "id: ruff" in content
    assert "id: ruff-format" in content
    assert "--fix" in content
    assert "--exit-non-zero-on-fix" in content


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_include_commitizen_hooks(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _, _ = manager.create_config(tmp_path)
    content = config_path.read_text()

    assert "commitizen-tools/commitizen" in content
    assert "id: commitizen" in content
    assert "stages: [commit-msg]" in content


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_preserve_existing_config(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')
    config_path = tmp_path / ".pre-commit-config.yaml"
    original_content = "# Custom configuration\nrepos:\n  - repo: https://github.com/custom/hook\n    rev: v1.0.0"
    config_path.write_text(original_content)

    new_config_path, _, already_existed = manager.create_config(tmp_path)
    content = new_config_path.read_text()

    assert new_config_path == config_path
    assert already_existed is True
    assert "# Custom configuration" in content
    assert "custom/hook" in content
    assert "astral-sh/ruff-pre-commit" not in content


def test_should_raise_error_if_project_root_not_exists():
    manager = PreCommitManager()
    non_existent_path = Path("/non/existent/path")

    with pytest.raises(ValueError, match="Project root does not exist"):
        manager.create_config(non_existent_path)


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_return_correct_config_path(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    (tmp_path / "pyproject.toml").write_text('[tool.poetry]\nname = "test"')

    config_path, _, _ = manager.create_config(tmp_path)

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

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.pyenv)

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

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.pyenv)

    assert versions["pre-commit"] == "4.5.0"
    assert versions["ruff"] == "0.16.0"
    assert versions["commitizen"] == "4.14.0"


def test_should_return_empty_dict_when_no_pyproject_exists(tmp_path: Path):
    manager = PreCommitManager()

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.pyenv)

    assert versions == {}


def test_should_return_empty_dict_when_no_dependencies_exist(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[tool.poetry]\nname = 'test'")

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.pyenv)

    assert versions == {}


def test_should_handle_partial_version_matches(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_content = """\
[tool.poetry.group.dev.dependencies]
ruff = "^0.16.0"
"""
    pyproject_path.write_text(pyproject_content)

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.pyenv)

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


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
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

    manager._add_dependencies(tmp_path, ManagerChoice.pyenv)

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
        ["poetry", "install", "--no-root"],
        cwd=str(tmp_path),
        check=True,
    )


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_handle_missing_pyproject_file(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()

    with pytest.raises(FileNotFoundError, match="pyproject.toml not found"):
        manager._add_dependencies(tmp_path, ManagerChoice.pyenv)


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_call_correct_command_to_install_hooks(
    mock_exec: MagicMock, tmp_path: Path
):
    manager = PreCommitManager()

    manager._install_hooks(tmp_path, ManagerChoice.pyenv)

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


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_handle_install_command_failure(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    mock_exec.side_effect = Exception("Command failed")

    manager._install_hooks(tmp_path, ManagerChoice.pyenv)


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_execute_full_config_creation_flow(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = """\[tool.poetry.group.dev.dependencies]
ruff = "^0.16.0"
commitizen = "^4.14.0"
"""
    pyproject_path.write_text(pyproject_content)

    config_path, versions, already_existed = manager.create_config(tmp_path)

    assert config_path.exists()
    assert "ruff" in versions
    assert "commitizen" in versions
    assert already_existed is False
    assert mock_exec.call_count == 3


def test_should_detect_poetry_manager_format(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[tool.poetry]\nname = 'test'")

    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.pyenv


def test_should_detect_uv_manager_format(tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[project]\nname = 'test'")

    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.uv


def test_should_default_to_pyenv_when_no_pyproject(tmp_path: Path):
    manager = PreCommitManager()

    detected = manager._detect_manager(tmp_path)

    assert detected == ManagerChoice.pyenv


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_add_uv_dependencies_to_pyproject(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        """[project]
name = "test"
version = "0.1.0"

[build-system]
requires = ["hatchling"]
"""
    )

    manager._add_dependencies(tmp_path, ManagerChoice.uv)

    content = pyproject_path.read_text()
    assert "[project.optional-dependencies]" in content
    assert "dev = [" in content
    assert "pre-commit>=4.5.1" in content
    assert "ruff>=0.15.2" in content
    assert "commitizen>=4.13.8,<4.14" in content

    mock_exec.assert_called_once_with(
        ["uv", "sync", "--all-groups"],
        cwd=str(tmp_path),
        check=True,
    )


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_extract_versions_from_uv_format(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = """\
[project.optional-dependencies]
dev = [
    "pre-commit>=4.5.1",
    "ruff>=0.15.2",
    "commitizen>=4.13.8,<4.14",
]
"""
    pyproject_path.write_text(pyproject_content)

    versions = manager._extract_versions_from_pyproject(tmp_path, ManagerChoice.uv)

    assert "pre-commit" in versions
    assert "ruff" in versions
    assert "commitizen" in versions
    assert versions["pre-commit"] == "4.5.1"
    assert versions["ruff"] == "0.15.2"
    assert versions["commitizen"] == "4.13.8"


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_call_uv_run_to_install_hooks(mock_exec: MagicMock, tmp_path: Path):
    manager = PreCommitManager()

    manager._install_hooks(tmp_path, ManagerChoice.uv)

    mock_exec.assert_called_once_with(
        [
            "uv",
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


@patch("api_bootstrapper_cli.core.pre_commit_manager.exec_cmd")
def test_should_execute_full_config_creation_flow_with_uv(
    mock_exec: MagicMock, tmp_path: Path
):
    manager = PreCommitManager()
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = """\
[project]
name = "test"
version = "0.1.0"

[project.optional-dependencies]
dev = [
    "ruff>=0.16.0",
    "commitizen>=4.14.0",
]
"""
    pyproject_path.write_text(pyproject_content)

    config_path, versions, already_existed = manager.create_config(
        tmp_path, ManagerChoice.uv
    )

    assert config_path.exists()
    assert "ruff" in versions
    assert "commitizen" in versions
    assert already_existed is False
    assert mock_exec.call_count == 2  # uv sync + uv run pre-commit install
