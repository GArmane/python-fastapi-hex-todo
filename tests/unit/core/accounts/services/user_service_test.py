import pytest

from todolist.core.accounts.entities.user import User
from todolist.core.accounts.services import hash_service, user_service
from todolist.core.accounts.services.exceptions import (
    EmailNotUniqueError,
    UserNotFoundError,
)

# Consts
FETCH_BY_EMAIL_FN_NAME = "fetch_user_by_email_fn"
FETCH_BY_ID_FN_NAME = "fetch_by_id_fn"
PERSIST_ONE_FN_NAME = "persist_user_fn"


@pytest.fixture(name=FETCH_BY_EMAIL_FN_NAME)
def fetch_by_email_fixture(repo_fn_factory):
    return repo_fn_factory(FETCH_BY_EMAIL_FN_NAME)


@pytest.fixture(name=FETCH_BY_ID_FN_NAME)
def fetch_by_id_fixture(repo_fn_factory):
    return repo_fn_factory(FETCH_BY_ID_FN_NAME)


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
        password_hash = hash_service.hash_(credentials.password)

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result = await user_service.get_by_credentials(
            fetch_user_by_email_fn, credentials
        )

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(email)
        assert result and result.email == email

    async def test_user_not_found(self, fetch_user_by_email_fn, credentials):
        # Setup
        fetch_user_by_email_fn.return_value.set_result(None)

        # Test
        result = await user_service.get_by_credentials(
            fetch_user_by_email_fn, credentials
        )

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(credentials.email)
        assert not result

    async def test_invalid_credentials(self, fetch_user_by_email_fn, credentials, user):
        # Setup
        email = credentials.email
        password_hash = hash_service.hash_("other password")

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        result = await user_service.get_by_credentials(
            fetch_user_by_email_fn, credentials
        )

        # Assertions
        fetch_user_by_email_fn.assert_called_once_with(email)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetById:
    async def test_valid_id(self, fetch_by_id_fn, user):
        # Setup
        id_ = 1
        fetch_by_id_fn.return_value.set_result(User(**{**user.dict(), "id": id_}))

        # Test
        result = await user_service.get_by_id(fetch_by_id_fn, id_)

        # Assertions
        fetch_by_id_fn.assert_called_once_with(id_)
        assert result and result.id == id_

    async def test_invalid_id(self, fetch_by_id_fn):
        # Setup
        id_ = 1
        fetch_by_id_fn.return_value.set_result(None)

        # Test
        result = await user_service.get_by_id(fetch_by_id_fn, id_)

        # Assertions
        fetch_by_id_fn.assert_called_once_with(id_)
        assert not result


@pytest.mark.unit
@pytest.mark.asyncio
class TestGetByIdOrRaise:
    async def test_valid_id(self, fetch_by_id_fn, user):
        # Setup
        id_ = 1
        fetch_by_id_fn.return_value.set_result(User(**{**user.dict(), "id": id_}))

        # Test
        result = await user_service.get_by_id_or_raise(fetch_by_id_fn, id_)

        # Assertions
        fetch_by_id_fn.assert_called_once_with(id_)
        assert result and result.id == id_

    async def test_invalid_id(self, fetch_by_id_fn):
        # Setup
        id_ = 1
        fetch_by_id_fn.return_value.set_result(None)

        # Test
        with pytest.raises(UserNotFoundError) as excinfo:
            await user_service.get_by_id_or_raise(fetch_by_id_fn, id_)

        # Assertions
        fetch_by_id_fn.assert_called_once_with(id_)
        error = excinfo.value
        assert error.msg == "user not found"
        assert error.user_id == id_


@pytest.mark.unit
@pytest.mark.asyncio
class TestRegister:
    async def test_register_unique(
        self, fetch_user_by_email_fn, persist_user_fn, credentials, user
    ):
        # Setup
        email = credentials.email
        password_hash = hash_service.hash_(credentials.password)

        persist_user_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )
        fetch_user_by_email_fn.return_value.set_result(None)

        # Test
        result = await user_service.register(
            fetch_user_by_email_fn, persist_user_fn, credentials
        )

        # Assertions
        persist_user_fn.assert_called_once()
        assert result.email == credentials.email

    async def test_register_not_unique(
        self, fetch_user_by_email_fn, persist_user_fn, credentials, user
    ):
        # Setup
        email = credentials.email
        password_hash = hash_service.hash_(credentials.password)

        fetch_user_by_email_fn.return_value.set_result(
            User(**{**user.dict(), "email": email, "password_hash": password_hash})
        )

        # Test
        with pytest.raises(EmailNotUniqueError) as excinfo:
            await user_service.register(
                fetch_user_by_email_fn, persist_user_fn, credentials
            )

        # Assertions
        error = excinfo.value
        assert error.msg == "email already registered"
        assert error.email == email
