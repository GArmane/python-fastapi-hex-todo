import pytest

from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services.exceptions import EmailNotUniqueError
from todolist.core.accounts.services.hash_service import hash_
from todolist.core.accounts.services.user_service import get_by_credentials, register

# Consts
FETCH_BY_EMAIL_FN_NAME = "fetch_user_by_email_fn"
PERSIST_ONE_FN_NAME = "persist_user_fn"


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
    async def test_valid_credentials(self, fetch_user_by_email_fn, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_(credentials.password)

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result: User = await get_by_credentials(fetch_user_by_email_fn, credentials)

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(email)
        assert result.email == email
        assert result.password_hash == password_hash

    async def test_user_not_found(self, fetch_user_by_email_fn, credentials):
        # Setup
        fetch_user_by_email_fn.return_value.set_result(None)

        # Test
        result = await get_by_credentials(fetch_user_by_email_fn, credentials)

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(credentials.email)
        assert not result

    async def test_invalid_credentials(self, fetch_user_by_email_fn, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_("other password")

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result = await get_by_credentials(fetch_user_by_email_fn, credentials)

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(email)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
class TestRegister:
    async def test_register_unique(
        self, fetch_user_by_email_fn, persist_user_fn, credentials, user
    ):
        # Setup
        email = credentials.email
        password_hash = hash_(credentials.password)

        persist_user_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )
        fetch_user_by_email_fn.return_value.set_result(None)

        # Test
        result = await register(fetch_user_by_email_fn, persist_user_fn, credentials)

        # Assertions
        persist_user_fn.assert_called_once()
        assert result.email == credentials.email
        assert result.password_hash != credentials.password

    async def test_register_not_unique(
        self, fetch_user_by_email_fn, persist_user_fn, credentials, user
    ):
        # Setup
        email = credentials.email
        password_hash = hash_(credentials.password)

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        with pytest.raises(EmailNotUniqueError) as excinfo:
            await register(fetch_user_by_email_fn, persist_user_fn, credentials)

        # Assertions
        error = excinfo.value
        assert error.msg == "email already registered"
        assert error.details == {"email": email}
