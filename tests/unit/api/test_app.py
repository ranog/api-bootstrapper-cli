from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from api_bootstrapper_cli.api.app import (
    BootstrapEnvironmentApiRequest,
    bootstrap_environment,
    health,
)
from api_bootstrapper_cli.core.bootstrap_env_use_case import (
    BootstrapEnvironmentRequest,
    BootstrapEnvironmentResponse,
)
from api_bootstrapper_cli.core.environment_service import EnvironmentSetupResult
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.shell import ShellError


def _build_response() -> BootstrapEnvironmentResponse:
    return BootstrapEnvironmentResponse(
        environment=EnvironmentSetupResult(
            python_version="3.12.12",
            python_path=Path("/tmp/python"),
            venv_path=Path("/tmp/.venv"),
            venv_python=Path("/tmp/.venv/bin/python"),
            editor_config_path=Path("/tmp/.vscode/settings.json"),
            has_poetry_project=True,
        )
    )


def test_should_return_health_status():
    response = health()
    assert response.status == "ok"


@patch("api_bootstrapper_cli.api.app.BootstrapEnvironmentUseCase")
def test_should_execute_bootstrap_env_and_return_serialized_result(
    mock_use_case: MagicMock, tmp_path: Path
):
    mock_use_case.return_value.execute.return_value = _build_response()
    payload = BootstrapEnvironmentApiRequest(
        path=tmp_path,
        python_version="3.12.12",
        install_dependencies=False,
        manager=ManagerChoice.uv,
    )

    response = bootstrap_environment(payload)

    assert response.python_version == "3.12.12"
    assert response.python_path == "/tmp/python"
    assert response.venv_path == "/tmp/.venv"
    assert response.venv_python == "/tmp/.venv/bin/python"
    assert response.editor_config_path == "/tmp/.vscode/settings.json"
    assert response.has_poetry_project is True

    execute_call = mock_use_case.return_value.execute.call_args
    request = execute_call.args[0]
    assert isinstance(request, BootstrapEnvironmentRequest)
    assert request.project_root == tmp_path.resolve()
    assert request.python_version == "3.12.12"
    assert request.install_dependencies is False
    assert request.manager == ManagerChoice.uv


def test_should_return_422_when_payload_is_invalid():
    with pytest.raises(ValidationError):
        BootstrapEnvironmentApiRequest(path=Path("."), manager=ManagerChoice.pyenv)


@patch("api_bootstrapper_cli.api.app.BootstrapEnvironmentUseCase")
def test_should_return_400_when_requirement_validation_fails(
    mock_use_case: MagicMock, tmp_path: Path
):
    mock_use_case.return_value.execute.side_effect = ValueError("pyenv not found")
    payload = BootstrapEnvironmentApiRequest(
        path=tmp_path,
        python_version="3.12.12",
        install_dependencies=True,
        manager=ManagerChoice.pyenv,
    )

    with pytest.raises(HTTPException) as exc_info:
        bootstrap_environment(payload)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "pyenv not found"


@patch("api_bootstrapper_cli.api.app.BootstrapEnvironmentUseCase")
def test_should_return_500_when_execution_fails(
    mock_use_case: MagicMock, tmp_path: Path
):
    mock_use_case.return_value.execute.side_effect = ShellError("command failed")
    payload = BootstrapEnvironmentApiRequest(
        path=tmp_path,
        python_version="3.12.12",
        install_dependencies=True,
        manager=ManagerChoice.pyenv,
    )

    with pytest.raises(HTTPException) as exc_info:
        bootstrap_environment(payload)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "bootstrap execution failed"
