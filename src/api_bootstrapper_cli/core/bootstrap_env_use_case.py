from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.environment_service import (
    EnvironmentBootstrapService,
    EnvironmentSetupResult,
)
from api_bootstrapper_cli.core.logger import RichLogger
from api_bootstrapper_cli.core.poetry_manager import PoetryManager
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.pyenv_manager import PyenvManager
from api_bootstrapper_cli.core.uv_dependency_manager import UvDependencyManager
from api_bootstrapper_cli.core.uv_python_manager import UvPythonManager
from api_bootstrapper_cli.core.vscode_writer import VSCodeWriter


ServiceFactory = Callable[[ManagerChoice], EnvironmentBootstrapService]


@dataclass(frozen=True)
class BootstrapEnvironmentRequest:
    project_root: Path
    python_version: str
    install_dependencies: bool
    manager: ManagerChoice


@dataclass(frozen=True)
class BootstrapEnvironmentResponse:
    environment: EnvironmentSetupResult


def create_bootstrap_service(
    manager: ManagerChoice = ManagerChoice.pyenv,
) -> EnvironmentBootstrapService:
    if manager == ManagerChoice.uv:
        return EnvironmentBootstrapService(
            python_env_manager=UvPythonManager(),
            dependency_manager=UvDependencyManager(),
            editor_writer=VSCodeWriter(),
            logger=RichLogger(),
        )

    return EnvironmentBootstrapService(
        python_env_manager=PyenvManager(),
        dependency_manager=PoetryManager(),
        editor_writer=VSCodeWriter(),
        logger=RichLogger(),
    )


class BootstrapEnvironmentUseCase:
    def __init__(
        self, service_factory: ServiceFactory = create_bootstrap_service
    ) -> None:
        self._service_factory = service_factory

    def execute(
        self, request: BootstrapEnvironmentRequest
    ) -> BootstrapEnvironmentResponse:
        service = self._service_factory(request.manager)
        environment = service.bootstrap(
            project_root=request.project_root,
            python_version=request.python_version,
            install_dependencies=request.install_dependencies,
        )
        return BootstrapEnvironmentResponse(environment=environment)
