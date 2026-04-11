from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api_bootstrapper_cli.core.bootstrap_env_use_case import (
    BootstrapEnvironmentRequest,
    BootstrapEnvironmentUseCase,
)
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.shell import ShellError


app = FastAPI(title="API Bootstrapper Platform API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str


class BootstrapEnvironmentApiRequest(BaseModel):
    path: Path
    python_version: str
    install_dependencies: bool = True
    manager: ManagerChoice = ManagerChoice.pyenv


class BootstrapEnvironmentApiResponse(BaseModel):
    python_version: str
    python_path: str
    venv_path: str | None
    venv_python: str | None
    editor_config_path: str
    has_poetry_project: bool


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/bootstrap-env", response_model=BootstrapEnvironmentApiResponse)
def bootstrap_environment(
    payload: BootstrapEnvironmentApiRequest,
) -> BootstrapEnvironmentApiResponse:
    use_case = BootstrapEnvironmentUseCase()
    request = BootstrapEnvironmentRequest(
        project_root=payload.path.resolve(),
        python_version=payload.python_version,
        install_dependencies=payload.install_dependencies,
        manager=payload.manager,
    )

    try:
        result = use_case.execute(request).environment
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (RuntimeError, OSError, ShellError) as exc:
        raise HTTPException(
            status_code=500, detail="bootstrap execution failed"
        ) from exc

    return BootstrapEnvironmentApiResponse(
        python_version=result.python_version,
        python_path=str(result.python_path),
        venv_path=str(result.venv_path) if result.venv_path else None,
        venv_python=str(result.venv_python) if result.venv_python else None,
        editor_config_path=str(result.editor_config_path),
        has_poetry_project=result.has_poetry_project,
    )
