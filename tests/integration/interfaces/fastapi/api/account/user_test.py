import pytest

from tests.factories.model_factories import register_user


@pytest.mark.integration
class TestRegister:
    def test_success(self, test_client, credentials):
        with test_client as client:
            response = client.post("/account/user", json=credentials.dict())
            data, status_code = response.json(), response.status_code
            assert status_code == 201
            assert data == {
                "id": 1,
                "email": credentials.email,
            }

    def test_validation_error(self, test_client):
        with test_client as client:
            response = client.post("/account/user", json={})
            data, status_code = response.json(), response.status_code
            assert status_code == 422
            assert data == {
                "detail": [
                    {
                        "loc": ["body", "credentials", "email"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "credentials", "password"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            }

    def test_conflict(self, test_client, user, credentials):
        with test_client as client:
            email = credentials.email
            register_user({**user.dict(), "email": email})

            response = client.post("/account/user", json=credentials.dict())
            data, status_code = response.json(), response.status_code

            assert status_code == 409
            assert data == {
                "detail": {"msg": "email already registered", "email": email},
            }
