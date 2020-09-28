from unittest.mock import Mock

import pytest

from tg_file_uploader.api import app
from tg_file_uploader.api.app import create_app


@pytest.fixture
def mock_setup_aiohttp_apispec(monkeypatch):
    mock_setup_aiohttp_apispec = Mock()
    monkeypatch.setattr(app, 'setup_aiohttp_apispec', mock_setup_aiohttp_apispec)
    return mock_setup_aiohttp_apispec


@pytest.fixture
def mock_application(monkeypatch):
    mock_application = Mock()
    monkeypatch.setattr(app.web, 'Application', mock_application)
    return mock_application


def test_create_app(mock_setup_aiohttp_apispec, mock_application):
    app = create_app()

    assert mock_application() == app
    mock_setup_aiohttp_apispec.assert_called_once()
    mock_application().router.add_route.assert_called()
