import jwt
import pytest
from operator import attrgetter

from tests.factories.model_factories import register_user
from todolist.core.accounts.services import hash_service
from todolist.core.accounts.entities.user import User
from todolist.config.environment import get_initial_settings


secret_key = attrgetter("JWT_SECRET_KEY")(get_initial_settings())
oauth2_token_url = "/account/oauth2/token"
oauth2_instrospect_url = "/account/oauth2/instrospect"


def build_form_data(credentials):
    return {
        "grant_type": "password",
        "username": credentials.email,
        "password": credentials.password,
    }


@pytest.fixture(name="user_login")
def user_login(test_client, credentials):
    id_ = 1
    email = credentials.email
    password_hash = hash_service.hash_(credentials.password)

    register_user(
        {"id": id_, "email": credentials.email, "password_hash": password_hash}
    )
    with test_client as client:
        response = client.post(oauth2_token_url, data=build_form_data(credentials))
        body = response.json()
        return (
            User(id=id_, email=email, password_hash=password_hash),
            body["access_token"],
        )


@pytest.mark.integration
class TestOAuth2Token:
    def test_success(self, test_client, credentials):
        register_user(
            {
                "email": credentials.email,
                "password_hash": hash_service.hash_(credentials.password),
            }
        )
        with test_client as client:
            response = client.post(oauth2_token_url, data=build_form_data(credentials))
            body = response.json()
            assert body["access_token"]
            assert body["expire"]
            assert body["token_type"] == "bearer"
            assert response.status_code == 200

    def test_unauthorized(self, test_client, credentials):
        with test_client as client:
            response = client.post(oauth2_token_url, data=build_form_data(credentials))
            assert response.json().get("detail") == "invalid authentication credentials"
            assert response.status_code == 401


@pytest.mark.integration
class TestOAuth2Introspect:
    def test_success(self, test_client, user_login):
        user, access_token = user_login
        with test_client as client:
            response = client.get(
                oauth2_instrospect_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            body = response.json()
            assert body == {
                "id": user.id,
                "email": user.email,
            }
            assert response.status_code == 200

    def test_unauthorized(self, test_client):
        with test_client as client:
            token = str(jwt.encode({"sub": "userid:1"}, secret_key))
            response = client.get(
                oauth2_instrospect_url, headers={"Authorization": f"Bearer {token}"},
            )

            assert response.json().get("detail") == "invalid token"
            assert response.status_code == 401
