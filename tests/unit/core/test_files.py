from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.files import ensure_dir, read_text, write_text


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
