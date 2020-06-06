import pytest
from pytest_factoryboy import register

from tests.factories.entitiy_factories import CredentialsFactory
from tests.factories.model_factories import register_user
from tests.utils.auth import build_form_data, oauth2_token_url
from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services import hash_service
from collections import namedtuple


LoggedUser = namedtuple("LoggedUser", ["user", "access_token"])


FACTORIES = [CredentialsFactory]

for factory in FACTORIES:
    register(factory)


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
