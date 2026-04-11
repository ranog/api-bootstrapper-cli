from __future__ import annotations

from unittest.mock import patch

from api_bootstrapper_cli.api.server import main


@patch("api_bootstrapper_cli.api.server.uvicorn.run")
def test_should_run_uvicorn_with_expected_app_path(mock_run):
    main()

    mock_run.assert_called_once_with(
        "api_bootstrapper_cli.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
