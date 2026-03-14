from __future__ import annotations

import re
from pathlib import Path

from api_bootstrapper_cli.core.protocols import ManagerChoice


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, overwrite: bool = False) -> None:
    if not overwrite and path.exists():
        raise FileExistsError(f"File already exists: {path}")
    path.write_text(content, encoding="utf-8")


def create_minimal_pyproject(
    project_root: Path,
    project_name: str | None = None,
    python_version: str = "3.10",
    use_pep621: bool = False,
) -> Path:
    """Create a minimal pyproject.toml in *project_root*.

    Args:
        project_root: Directory where the file will be created.
        project_name: Project name (defaults to directory name).
        python_version: Python version string (e.g. ``"3.12.3"``).
        use_pep621: When ``True`` generate a PEP 621 ``[project]`` file
            (required by ``uv``). Otherwise generate a Poetry-style file.
    """
    if project_name is None:
        project_name = project_root.name

    pyproject_path = project_root / "pyproject.toml"

    if pyproject_path.exists():
        return pyproject_path

    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    if use_pep621:
        content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">={major_minor}"
dependencies = []
"""
    else:
        content = f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = ""
authors = []
readme = "README.md"

[tool.poetry.dependencies]
python = "^{major_minor}"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

    write_text(pyproject_path, content)
    return pyproject_path


def update_python_constraint(pyproject_path: Path, python_version: str) -> bool:
    """Update the Python version constraint in an existing pyproject.toml.

    Handles both PEP 621 (``requires-python = ">=X.Y"``) and Poetry-style
    (``python = "^X.Y"``) formats.
    """
    if not pyproject_path.exists():
        return False

    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    content = read_text(pyproject_path)

    pep621_pattern = r'(requires-python\s*=\s*)["\']([^"\'\n]+)["\']'
    if pep621_match := re.search(pep621_pattern, content):
        target = f">={major_minor}"
        if pep621_match.group(2) == target:
            return False
        new_content = re.sub(
            pep621_pattern, f'requires-python = "{target}"', content, count=1
        )
        write_text(pyproject_path, new_content, overwrite=True)
        return True

    poetry_pattern = r'(python\s*=\s*)["\']([^"\'\n]+)["\']'
    if poetry_match := re.search(poetry_pattern, content):
        target = f"^{major_minor}"
        if poetry_match.group(2) == target:
            return False
        new_content = re.sub(poetry_pattern, f'\\1"{target}"', content, count=1)
        write_text(pyproject_path, new_content, overwrite=True)
        return True

    return False


def create_env_example(project_root: Path) -> None:
    """Create or update .env.example template file with PYTHONDONTWRITEBYTECODE=1.

    Logic:
    - Checks if .env.example, .env.local, or .env.testing exist
    - If any exist: ensures PYTHONDONTWRITEBYTECODE=1 is present
    - If none exist: creates .env.example with PYTHONDONTWRITEBYTECODE=1

    Args:
        project_root: Directory where the file will be created or updated.
    """
    env_files = [
        project_root / ".env.example",
        project_root / ".env.local",
        project_root / ".env.testing",
    ]

    # Find existing env files
    existing_env_files = [f for f in env_files if f.exists()]

    if existing_env_files:
        # Check and update existing files
        for env_file in existing_env_files:
            content = read_text(env_file)
            if "PYTHONDONTWRITEBYTECODE" not in content:
                # Add the variable at the beginning
                new_content = (
                    "# Python Configuration\nPYTHONDONTWRITEBYTECODE=1\n\n" + content
                )
                write_text(env_file, new_content, overwrite=True)
    else:
        # Create new .env.example
        env_example_path = project_root / ".env.example"
        content = """# Environment variables template
# Copy this file to .env and fill in your actual values

# Python Configuration
PYTHONDONTWRITEBYTECODE=1

# Add your project-specific environment variables below
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# SECRET_KEY=your-secret-key-here
# DEBUG=False
"""
        write_text(env_example_path, content)


def update_gitignore(project_root: Path) -> None:
    """Update .gitignore to exclude environment files (only if .gitignore exists).

    Logic:
    - If .gitignore does NOT exist: do nothing (don't create it)
    - If .gitignore exists: add .env exclusion rules if not present

    Ensures that .env (with sensitive data) is not committed to git,
    while .env.example (template) can be versioned.

    Args:
        project_root: Directory containing the .gitignore file.
    """
    gitignore_path = project_root / ".gitignore"

    # Only proceed if .gitignore already exists
    if not gitignore_path.exists():
        return

    env_patterns = {
        "# Environment variables",
        ".env",
        ".env.local",
        "!.env.example",
    }

    content = read_text(gitignore_path)
    lines = set(content.splitlines())

    # Check if env patterns are already present
    if env_patterns.issubset(lines):
        return

    # Add env patterns if missing
    missing_patterns = env_patterns - lines
    if missing_patterns:
        # Add a newline before the section if file doesn't end with one
        separator = "\n" if content and not content.endswith("\n") else ""
        new_content = (
            content + separator + "\n" + "\n".join(sorted(missing_patterns)) + "\n"
        )
        write_text(gitignore_path, new_content, overwrite=True)


def create_project_structure(project_root: Path) -> None:
    """Create src/ and tests/ directories with __init__.py files.

    Logic:
    - Creates src/ directory if it doesn't exist
    - Creates src/__init__.py if it doesn't exist
    - Creates tests/ directory if it doesn't exist
    - Creates tests/__init__.py if it doesn't exist

    Args:
        project_root: Root directory of the project.
    """
    # Create src/ directory and __init__.py
    src_dir = project_root / "src"
    ensure_dir(src_dir)

    src_init = src_dir / "__init__.py"
    if not src_init.exists():
        write_text(src_init, "")

    # Create tests/ directory and __init__.py
    tests_dir = project_root / "tests"
    ensure_dir(tests_dir)

    tests_init = tests_dir / "__init__.py"
    if not tests_init.exists():
        write_text(tests_init, "")


def create_makefile(
    project_root: Path,
    manager: ManagerChoice = ManagerChoice.pyenv,
) -> Path:
    """Create a Makefile tailored to the selected dependency manager."""
    makefile_path = project_root / "Makefile"

    if makefile_path.exists():
        return makefile_path

    image_name = _normalize_project_name(project_root.name)
    container_name = image_name.replace("_", "-")

    if manager == ManagerChoice.uv:
        content = f"""\
.PHONY: init install-deps run deps-export build-container run-container tests

init: install-deps

install-deps:
\t@uv sync --all-groups
\t@uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
\t@uv run pre-commit run --all-files

run: init
\t@uv run env $$(grep -v '^\\#' .env | xargs) uvicorn src.main:app --reload --port 8080

deps-export:
\t@uv export --all-groups --no-hashes -o requirements.txt

build-container:
\t@docker build \\
\t\t--tag {image_name}:latest \\
\t\t--build-arg GIT_HASH=$$(git rev-parse HEAD) \\
\t\t-f Dockerfile \\
\t\t.

run-container: deps-export build-container
\t@docker run --rm -it \\
\t\t--name {container_name} \\
\t\t--env-file .env \\
\t\t--env PORT=8080 \\
\t\t--publish 8080:8080 \\
\t\t{image_name}:latest

tests: init
\t@uv run env $$(grep -v '^\\#' .env | xargs) pytest
"""
    else:
        content = f"""\
.PHONY: init install-deps run poetry-export build-container run-container tests

init: install-deps

install-deps:
\t@pip install --upgrade pip setuptools wheel
\t@pip install --upgrade poetry
\t@poetry install --no-root
\t@poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg
\t@poetry run pre-commit run --all-files

run: init
\t@poetry run env $$(grep -v '^\\#' .env | xargs) uvicorn src.main:app --reload --port 8080

poetry-export:
\t@poetry export --with dev -vv --no-ansi --no-interaction --without-hashes --format requirements.txt --output requirements.txt

build-container:
\t@docker build \\
\t\t--tag {image_name}:latest \\
\t\t--build-arg GIT_HASH=$$(git rev-parse HEAD) \\
\t\t-f Dockerfile \\
\t\t.

run-container: poetry-export build-container
\t@docker run --rm -it \\
\t\t--name {container_name} \\
\t\t--env-file .env \\
\t\t--env PORT=8080 \\
\t\t--publish 8080:8080 \\
\t\t{image_name}:latest

tests: init
\t@poetry run env $$(grep -v '^\\#' .env | xargs) pytest
"""

    write_text(makefile_path, content)
    return makefile_path


def _normalize_project_name(project_name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", project_name).strip("-")
    return normalized.lower() or "python-app"


def create_dockerfile(project_root: Path, python_version: str = "3.13") -> Path:
    """Create a Dockerfile for a Python application.

    Args:
        project_root: Root directory of the project.
        python_version: Python version for the base image (e.g., "3.13", "3.12.12").
                       If a full version is provided (e.g., "3.12.12"),
                       only major.minor will be used (e.g., "3.12").

    Returns:
        Path to the created Dockerfile.
    """
    dockerfile_path = project_root / "Dockerfile"

    if dockerfile_path.exists():
        return dockerfile_path

    # Extract major.minor from version (e.g., "3.12.12" -> "3.12")
    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    content = f"""FROM python:{major_minor}-slim-bookworm as builder

RUN apt-get update && apt-get install -y --no-install-recommends \\
\tbuild-essential && \\
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:{major_minor}-slim-bookworm

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

COPY --from=builder /opt/venv /opt/venv
COPY ./src ./src
"""

    write_text(dockerfile_path, content)
    return dockerfile_path
