from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.files import (
    create_dockerfile,
    create_env_example,
    create_minimal_pyproject,
    create_project_structure,
    ensure_dir,
    read_text,
    update_gitignore,
    update_python_constraint,
    write_text,
)


def test_should_create_directory(tmp_path: Path):
    test_dir = tmp_path / "new_dir"

    ensure_dir(test_dir)

    assert test_dir.exists()
    assert test_dir.is_dir()


def test_should_create_nested_directories(tmp_path: Path):
    test_dir = tmp_path / "parent" / "child" / "grandchild"

    ensure_dir(test_dir)

    assert test_dir.exists()
    assert test_dir.is_dir()


def test_should_not_fail_if_directory_exists(tmp_path: Path):
    test_dir = tmp_path / "existing"
    test_dir.mkdir()

    ensure_dir(test_dir)

    assert test_dir.exists()


def test_should_read_file_content(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!", encoding="utf-8")

    content = read_text(test_file)

    assert content == "Hello, World!"


@pytest.mark.parametrize("content", ["Hello, World!", "こんにちは 🚀", "", "Hello 🌍"])
def test_should_handle_utf8_content(tmp_path: Path, content: str):
    test_file = tmp_path / "utf8.txt"
    test_file.write_text(content, encoding="utf-8")

    read_content = read_text(test_file)

    assert read_content == content


def test_should_write_content_to_new_file(tmp_path: Path):
    test_file = tmp_path / "new.txt"

    write_text(test_file, "content", overwrite=False)

    assert test_file.read_text() == "content"


def test_should_raise_error_if_file_exists_and_no_overwrite(tmp_path: Path):
    test_file = tmp_path / "existing.txt"
    test_file.write_text("original")

    with pytest.raises(FileExistsError, match="File already exists"):
        write_text(test_file, "new", overwrite=False)


def test_should_overwrite_when_flag_is_true(tmp_path: Path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("old")

    write_text(test_file, "new", overwrite=True)

    assert test_file.read_text() == "new"


def test_should_create_minimal_pyproject_toml(tmp_path: Path):
    result = create_minimal_pyproject(tmp_path, python_version="3.12")

    assert result == tmp_path / "pyproject.toml"
    assert result.exists()

    content = result.read_text()
    assert "[tool.poetry]" in content
    assert f'name = "{tmp_path.name}"' in content
    assert 'version = "0.1.0"' in content
    assert "authors = []" in content
    assert 'python = "^3.12"' in content
    assert "[build-system]" in content


def test_should_use_custom_project_name_in_pyproject(tmp_path: Path):
    result = create_minimal_pyproject(tmp_path, project_name="custom-name")

    content = result.read_text()
    assert 'name = "custom-name"' in content


def test_should_not_overwrite_existing_pyproject(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    original_content = "[tool.poetry]\nname = 'existing'\n"
    pyproject.write_text(original_content)

    result = create_minimal_pyproject(tmp_path)

    assert result == pyproject
    assert result.read_text() == original_content


def test_should_extract_major_minor_version_from_python_version(tmp_path: Path):
    result = create_minimal_pyproject(tmp_path, python_version="3.13.9")
    content = result.read_text()

    assert 'python = "^3.13"' in content

    test2_dir = tmp_path / "test2"
    test2_dir.mkdir()
    result2 = create_minimal_pyproject(test2_dir, python_version="3.12")
    content2 = result2.read_text()

    assert 'python = "^3.12"' in content2


def test_update_python_constraint_should_update_existing_version(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.12"
requests = "^2.28"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""")

    updated = update_python_constraint(pyproject, "3.9.24")

    assert updated is True
    content = pyproject.read_text()
    assert 'python = "^3.9"' in content
    assert 'requests = "^2.28"' in content


def test_update_python_constraint_should_return_false_if_already_correct(
    tmp_path: Path,
):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[tool.poetry]
name = "test-project"

[tool.poetry.dependencies]
python = "^3.12"
""")

    updated = update_python_constraint(pyproject, "3.12.3")

    assert updated is False
    content = pyproject.read_text()
    assert 'python = "^3.12"' in content


def test_update_python_constraint_should_return_false_if_file_not_exists(
    tmp_path: Path,
):
    pyproject = tmp_path / "pyproject.toml"

    updated = update_python_constraint(pyproject, "3.12")

    assert updated is False


def test_update_python_constraint_should_handle_single_quotes(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[tool.poetry]
name = "test-project"

[tool.poetry.dependencies]
python = '^3.12'
""")

    updated = update_python_constraint(pyproject, "3.11")

    assert updated is True
    content = pyproject.read_text()
    assert 'python = "^3.11"' in content


def test_update_python_constraint_should_handle_spaces_around_equals(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[tool.poetry]
name = "test-project"

[tool.poetry.dependencies]
python   =   "^3.12"
""")

    updated = update_python_constraint(pyproject, "3.10.5")

    assert updated is True
    content = pyproject.read_text()
    assert 'python = "^3.10"' in content or 'python   =   "^3.10"' in content


def test_create_env_example_should_create_template_file(tmp_path: Path):
    create_env_example(tmp_path)

    env_file = tmp_path / ".env.example"
    assert env_file.exists()

    content = env_file.read_text()
    assert "PYTHONDONTWRITEBYTECODE=1" in content
    assert "Environment variables template" in content
    assert "Copy this file to .env" in content


def test_create_env_example_should_add_variable_to_existing(tmp_path: Path):
    env_example = tmp_path / ".env.example"
    original_content = "# Custom content\nMY_VAR=value\n"
    env_example.write_text(original_content)

    create_env_example(tmp_path)

    content = env_example.read_text()
    assert "PYTHONDONTWRITEBYTECODE=1" in content
    assert "MY_VAR=value" in content
    assert content.startswith("# Python Configuration")


def test_create_env_example_should_not_duplicate_variable(tmp_path: Path):
    env_example = tmp_path / ".env.example"
    original_content = "# My config\nPYTHONDONTWRITEBYTECODE=1\nMY_VAR=value\n"
    env_example.write_text(original_content)

    create_env_example(tmp_path)

    content = env_example.read_text()
    assert content.count("PYTHONDONTWRITEBYTECODE") == 1
    assert content == original_content


def test_create_env_example_should_handle_env_local(tmp_path: Path):
    env_local = tmp_path / ".env.local"
    env_local.write_text("DATABASE_URL=localhost\n")

    create_env_example(tmp_path)

    content = env_local.read_text()
    assert "PYTHONDONTWRITEBYTECODE=1" in content
    assert "DATABASE_URL=localhost" in content


def test_create_env_example_should_handle_env_testing(tmp_path: Path):
    env_testing = tmp_path / ".env.testing"
    env_testing.write_text("TEST_MODE=true\n")

    create_env_example(tmp_path)

    content = env_testing.read_text()
    assert "PYTHONDONTWRITEBYTECODE=1" in content
    assert "TEST_MODE=true" in content


def test_update_gitignore_should_do_nothing_if_not_exists(tmp_path: Path):
    update_gitignore(tmp_path)

    gitignore = tmp_path / ".gitignore"
    assert not gitignore.exists()


def test_update_gitignore_should_add_env_patterns_to_existing(tmp_path: Path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("# Existing patterns\n*.pyc\n__pycache__/\n")

    update_gitignore(tmp_path)

    content = gitignore.read_text()
    assert "*.pyc" in content  # Original content preserved
    assert "__pycache__/" in content
    assert ".env" in content
    assert ".env.local" in content
    assert "!.env.example" in content


def test_update_gitignore_should_not_duplicate_env_patterns(tmp_path: Path):
    gitignore = tmp_path / ".gitignore"
    original_content = """# Environment variables
.env
.env.local
!.env.example
*.pyc
"""
    gitignore.write_text(original_content)

    update_gitignore(tmp_path)

    content = gitignore.read_text()
    # Count occurrences
    assert content.count(".env\n") == 1
    assert content.count(".env.local\n") == 1
    assert content.count("!.env.example\n") == 1


def test_create_project_structure_should_create_directories(tmp_path: Path):
    create_project_structure(tmp_path)

    src_dir = tmp_path / "src"
    tests_dir = tmp_path / "tests"

    assert src_dir.exists()
    assert src_dir.is_dir()
    assert tests_dir.exists()
    assert tests_dir.is_dir()


def test_create_project_structure_should_create_init_files(tmp_path: Path):
    create_project_structure(tmp_path)

    src_init = tmp_path / "src" / "__init__.py"
    tests_init = tmp_path / "tests" / "__init__.py"

    assert src_init.exists()
    assert tests_init.exists()
    assert src_init.read_text() == ""
    assert tests_init.read_text() == ""


def test_create_project_structure_should_not_overwrite_existing_init(tmp_path: Path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    src_init = src_dir / "__init__.py"
    src_init.write_text("# Existing content")

    create_project_structure(tmp_path)

    assert src_init.read_text() == "# Existing content"


def test_create_dockerfile_should_create_file(tmp_path: Path):
    result = create_dockerfile(tmp_path, python_version="3.13")

    assert result == tmp_path / "Dockerfile"
    assert result.exists()

    content = result.read_text()
    assert "FROM python:3.13-slim as builder" in content
    assert "uvicorn" in content
    assert "src.main:app" in content
    assert "COPY ./src ./src" in content


def test_create_dockerfile_should_use_custom_python_version(tmp_path: Path):
    result = create_dockerfile(tmp_path, python_version="3.12")

    content = result.read_text()
    assert "FROM python:3.12-slim as builder" in content
    assert "FROM python:3.12-slim" in content


def test_create_dockerfile_should_extract_major_minor_from_full_version(tmp_path: Path):
    result = create_dockerfile(tmp_path, python_version="3.12.12")

    content = result.read_text()
    assert "FROM python:3.12-slim as builder" in content
    assert "FROM python:3.12-slim" in content
    # Should not include patch version
    assert "3.12.12" not in content


def test_create_dockerfile_should_handle_version_with_two_parts(tmp_path: Path):
    result = create_dockerfile(tmp_path, python_version="3.13")

    content = result.read_text()
    assert "FROM python:3.13-slim as builder" in content
    assert "FROM python:3.13-slim" in content


def test_create_dockerfile_should_not_overwrite_existing(tmp_path: Path):
    dockerfile = tmp_path / "Dockerfile"
    original_content = "FROM ubuntu:latest\n"
    dockerfile.write_text(original_content)

    result = create_dockerfile(tmp_path)

    assert result == dockerfile
    assert result.read_text() == original_content
