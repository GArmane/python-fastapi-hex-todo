import pytest

from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services.hash_service import hash_
from todolist.core.accounts.services.user_service import get_by_credentials, register

# Consts
FETCH_BY_EMAIL_FN_NAME = "fetch_by_email_fn"
PERSIST_ONE_FN_NAME = "persist_one_fn"


@pytest.fixture(name=FETCH_BY_EMAIL_FN_NAME)
def fetch_by_email_fixture(repo_fn_factory):
    return repo_fn_factory(FETCH_BY_EMAIL_FN_NAME)


@pytest.fixture(name=PERSIST_ONE_FN_NAME)
def persist_one_fixture(repo_fn_factory):
    return repo_fn_factory(PERSIST_ONE_FN_NAME)


# Tests
@pytest.mark.unit
@pytest.mark.asyncio
class TestGetByCredentials:
    async def test_valid_credentials(self, fetch_by_email_fn, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_(credentials.password)

        fetch_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result: User = await get_by_credentials(fetch_by_email_fn, credentials)

        # Assertions
        fetch_by_email_fn.assert_called_once_with(email)
        assert result.email == email
        assert result.password_hash == password_hash

    async def test_user_not_found(self, fetch_by_email_fn, credentials):
        # Setup
        fetch_by_email_fn.return_value.set_result(None)

        # Test
        result = await get_by_credentials(fetch_by_email_fn, credentials)

        # Assertions
        fetch_by_email_fn.assert_called_once_with(credentials.email)
        assert not result

    async def test_invalid_credentials(self, fetch_by_email_fn, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_("other password")

        fetch_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result = await get_by_credentials(fetch_by_email_fn, credentials)

        # Assertions
        fetch_by_email_fn.assert_called_once_with(email)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register(persist_one_fn, credentials, user):
    # Setup
    email = credentials.email
    password_hash = hash_(credentials.password)

    persist_one_fn.return_value.set_result(
        User(**{**user.dict(), "email": email, "password_hash": password_hash})
    )

    # Test
    result = await register(persist_one_fn, credentials)

    # Assertions
    persist_one_fn.assert_called_once()
    assert result.email == credentials.email
    assert result.password_hash != credentials.password
