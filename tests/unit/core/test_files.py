from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.files import (
    create_minimal_pyproject,
    ensure_dir,
    read_text,
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
    # Test with full version (major.minor.patch)
    result = create_minimal_pyproject(tmp_path, python_version="3.13.9")
    content = result.read_text()
    assert 'python = "^3.13"' in content

    # Test with just major.minor (using a different directory)
    test2_dir = tmp_path / "test2"
    test2_dir.mkdir()
    result2 = create_minimal_pyproject(test2_dir, python_version="3.12")
