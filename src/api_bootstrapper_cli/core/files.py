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
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/app_db
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


MAIN_PY_TEMPLATE = """from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import Base, engine, get_db
from src.models import Item
from src.schemas import HealthResponse, ItemCreate, ItemRead, ItemUpdate

app = FastAPI(title="API Bootstrapper App")

# Ensure local development has tables available without extra setup steps.
Base.metadata.create_all(bind=engine)


@app.get("/health", response_model=HealthResponse)
def healthcheck(db: Session = Depends(get_db)) -> HealthResponse:
    db.execute(text("SELECT 1"))
    return HealthResponse(status="ok", database="up")


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    return db.query(Item).order_by(Item.id).all()


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = payload.name
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return None
"""

DATABASE_PY_TEMPLATE = """from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/app_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

MODELS_PY_TEMPLATE = """from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
"""

SCHEMAS_PY_TEMPLATE = """from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    status: str
    database: str


class ItemCreate(BaseModel):
    name: str


class ItemUpdate(BaseModel):
    name: str


class ItemRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
"""

TESTS_CONFTEST_TEMPLATE = """from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app

# Keep tests fast and deterministic with an isolated in-memory database.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
"""

TESTS_API_FLOW_TEMPLATE = """from __future__ import annotations


def test_should_return_healthcheck_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}


def test_should_execute_basic_crud_flow(client):
    created_response = client.post("/items", json={"name": "first item"})

    assert created_response.status_code == 201
    created_payload = created_response.json()
    assert created_payload["name"] == "first item"
    item_id = created_payload["id"]

    fetched_response = client.get(f"/items/{item_id}")

    assert fetched_response.status_code == 200
    assert fetched_response.json()["name"] == "first item"

    listed_response = client.get("/items")

    assert listed_response.status_code == 200
    listed_payload = listed_response.json()
    assert len(listed_payload) == 1
    assert listed_payload[0]["id"] == item_id

    updated_response = client.put(f"/items/{item_id}", json={"name": "updated item"})

    assert updated_response.status_code == 200
    assert updated_response.json()["name"] == "updated item"

    deleted_response = client.delete(f"/items/{item_id}")
    assert deleted_response.status_code == 204

    missing_response = client.get(f"/items/{item_id}")
    assert missing_response.status_code == 404
"""


def create_project_structure(project_root: Path) -> None:
    """Create project folders and a runnable FastAPI + PostgreSQL scaffold.

    Logic:
    - Creates src/ directory if it doesn't exist
    - Creates src modules for API, DB and schemas if missing
    - Creates tests/ directory if it doesn't exist
    - Creates test packages and a minimal integration flow if missing

    Args:
        project_root: Root directory of the project.
    """
    src_dir = project_root / "src"
    tests_dir = project_root / "tests"
    tests_unit_dir = tests_dir / "unit"
    tests_integration_dir = tests_dir / "integration"
    tests_e2e_dir = tests_dir / "e2e"

    for directory in [
        src_dir,
        tests_dir,
        tests_unit_dir,
        tests_integration_dir,
        tests_e2e_dir,
    ]:
        ensure_dir(directory)

    for init_path in [
        src_dir / "__init__.py",
        tests_dir / "__init__.py",
        tests_unit_dir / "__init__.py",
        tests_integration_dir / "__init__.py",
        tests_e2e_dir / "__init__.py",
    ]:
        _write_if_missing(init_path, "")

    scaffold_files = {
        src_dir / "main.py": MAIN_PY_TEMPLATE,
        src_dir / "database.py": DATABASE_PY_TEMPLATE,
        src_dir / "models.py": MODELS_PY_TEMPLATE,
        src_dir / "schemas.py": SCHEMAS_PY_TEMPLATE,
        tests_dir / "conftest.py": TESTS_CONFTEST_TEMPLATE,
        tests_integration_dir / "test_api_flow.py": TESTS_API_FLOW_TEMPLATE,
    }
    for path, content in scaffold_files.items():
        _write_if_missing(path, content)


def _write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        write_text(path, content)


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


def create_docker_compose(project_root: Path) -> Path:
    """Create docker-compose.yml with a PostgreSQL service."""
    compose_path = project_root / "docker-compose.yml"

    if compose_path.exists():
        return compose_path

    content = """services:
  db:
    image: postgres:16-alpine
    container_name: app-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d app_db"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
"""
    write_text(compose_path, content)
    return compose_path


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
