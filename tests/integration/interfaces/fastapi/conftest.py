import pytest
from fastapi.testclient import TestClient  # type: ignore

from tests.utils.database import clear_database
from todolist.config.environment import get_current_settings, get_initial_settings
from todolist.interfaces.fastapi.app import init_app


# Settings fixtures
@pytest.fixture(name="current_env_settings")
def current_env_settings_fixture():
    return get_current_settings()


@pytest.fixture(name="initial_env_settings")
def initial_env_settings_fixture():
    return get_initial_settings()


@pytest.fixture(name="web_app")
def web_app_fixture(initial_env_settings):
    return init_app(initial_env_settings)


# Test client fixtures
@pytest.fixture(name="test_client")
def test_client_fixture(web_app):
    with clear_database():
        yield TestClient(web_app)
