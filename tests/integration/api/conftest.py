from collections import namedtuple

import pytest
from fastapi.testclient import TestClient  # type: ignore
from pytest_factoryboy import register

from tests.factories.entity_factories import CredentialsFactory
from tests.factories.model_factories import register_user
from tests.utils.auth import build_form_data, oauth2_token_url
from tests.utils.database import clear_database
from todolist.config.environment import get_settings
from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services import hash_service
from todolist.api import init_app


LoggedUser = namedtuple("LoggedUser", ["user", "access_token"])


FACTORIES = [CredentialsFactory]

for factory in FACTORIES:
    register(factory)


@pytest.fixture(name="env_settings")
def env_settings():
    return get_settings()


@pytest.fixture(name="web_app")
def web_app_fixture(env_settings):
    return init_app(env_settings)


@pytest.fixture(name="test_client")
def test_client_fixture(web_app):
    with clear_database():
        yield TestClient(web_app)


@pytest.fixture(name="credentials")
def credentials_fixture(credentials_factory):
    return credentials_factory()


@pytest.fixture()
def logged_user(test_client, credentials):
    id_ = 1
    email = credentials.email
    password_hash = hash_service.hash_(credentials.password)

    register_user(
        {"id": id_, "email": credentials.email, "password_hash": password_hash}
    )
    with test_client as client:
        response = client.post(oauth2_token_url, data=build_form_data(credentials))
        body = response.json()
        return LoggedUser(
            User(id=id_, email=email, password_hash=password_hash),
            body["access_token"],
        )
