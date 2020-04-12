from asyncio import Future

import pytest
from passlib.hash import argon2

from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services.user_service import get_by_credentials, register


# Fixtures
@pytest.fixture(name="fetch_by_credentials_fn")
def fetch_by_credentials_fixture(mocker):
    def side_effect(credentials):
        future: Future[User] = Future()
        future.set_result(
            User(
                **{
                    "id": 1,
                    "email": credentials.email,
                    "password_hash": argon2.hash(credentials.password),
                }
            )
        )
        return future

    return mocker.MagicMock(side_effect=side_effect)


@pytest.fixture(name="fetch_by_credentials_none_fn")
def fetch_by_credentials_none_fixture(mocker):
    def side_effect(_):
        future: Future[None] = Future()
        future.set_result(None)
        return future

    return mocker.MagicMock(side_effect=side_effect)


@pytest.fixture(name="fetch_by_credentials_other_fn")
def fetch_by_credentials_other_fixture(mocker):
    def side_effect(credentials):
        future: Future[User] = Future()
        future.set_result(
            User(
                **{
                    "id": 1,
                    "email": credentials.email,
                    "password_hash": argon2.hash("other password"),
                }
            )
        )
        return future

    return mocker.MagicMock(side_effect=side_effect)


@pytest.fixture(name="persist_one_fn")
def persist_one_fn_fixture(mocker):
    def side_effect(registry):
        future: Future[User] = Future()
        future.set_result(User(**{**registry.dict(), "id": 1}))
        return future

    return mocker.MagicMock(side_effect=side_effect)


# Tests
@pytest.mark.unit
@pytest.mark.asyncio
class TestGetByCredentials:
    async def test_valid_credentials(self, fetch_by_credentials_fn, credentials):
        # Test
        result: User = await get_by_credentials(fetch_by_credentials_fn, credentials)

        # Assertions
        fetch_by_credentials_fn.assert_called_once_with(credentials)
        assert result.email == credentials.email

    async def test_user_not_found(self, fetch_by_credentials_none_fn, credentials):
        # Test
        result = await get_by_credentials(fetch_by_credentials_none_fn, credentials)

        # Assertions
        fetch_by_credentials_none_fn.assert_called_once_with(credentials)
        assert not result

    async def test_invalid_credentials(
        self, fetch_by_credentials_other_fn, credentials, user
    ):
        # Test
        result = await get_by_credentials(fetch_by_credentials_other_fn, credentials)

        # Assertions
        fetch_by_credentials_other_fn.assert_called_once_with(credentials)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register(persist_one_fn, credentials):
    # Test
    result = await register(persist_one_fn, credentials)

    # Assertions
    persist_one_fn.assert_called_once()
    assert result.email == credentials.email
    assert result.password_hash != credentials.password
