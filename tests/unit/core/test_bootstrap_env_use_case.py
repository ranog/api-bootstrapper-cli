from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from api_bootstrapper_cli.core.bootstrap_env_use_case import (
    BootstrapEnvironmentRequest,
    BootstrapEnvironmentResponse,
    BootstrapEnvironmentUseCase,
    create_bootstrap_service,
)
from api_bootstrapper_cli.core.environment_service import EnvironmentSetupResult
from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.uv_dependency_manager import UvDependencyManager
from api_bootstrapper_cli.core.uv_python_manager import UvPythonManager


def test_should_create_service_with_pyenv_and_poetry_by_default():
    service = create_bootstrap_service()

    assert isinstance(service._python_env, PyenvManager)
    assert isinstance(service._deps, PoetryManager)


def test_should_create_service_with_uv_managers_when_manager_is_uv():
    service = create_bootstrap_service(manager=ManagerChoice.uv)

    assert isinstance(service._python_env, UvPythonManager)
    assert isinstance(service._deps, UvDependencyManager)


def test_should_execute_bootstrap_using_request_payload():
    mock_service = MagicMock()
    expected_environment = EnvironmentSetupResult(
        python_version="3.12.12",
        python_path=Path("/tmp/python"),
        venv_path=Path("/tmp/.venv"),
        venv_python=Path("/tmp/.venv/bin/python"),
        editor_config_path=Path("/tmp/.vscode/settings.json"),
        has_poetry_project=True,
    )
    mock_service.bootstrap.return_value = expected_environment

    mock_factory = MagicMock(return_value=mock_service)
    use_case = BootstrapEnvironmentUseCase(service_factory=mock_factory)

    request = BootstrapEnvironmentRequest(
        project_root=Path("/workspace/sample-project"),
        python_version="3.12.12",
        install_dependencies=False,
        manager=ManagerChoice.uv,
    )

    response = use_case.execute(request)

    mock_factory.assert_called_once_with(ManagerChoice.uv)
    mock_service.bootstrap.assert_called_once_with(
        project_root=request.project_root,
        python_version=request.python_version,
        install_dependencies=request.install_dependencies,
    )
    assert response == BootstrapEnvironmentResponse(environment=expected_environment)
