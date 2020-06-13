from operator import attrgetter

import pytest
from asyncpg.exceptions import UniqueViolationError
from pytest_factoryboy import register

from tests.factories.entity_factories import UserFactory
from tests.factories.model_factories import register_user
from todolist.infra.database.repositories import user_repository


FACTORIES = [
    UserFactory,
]

for factory in FACTORIES:
    register(factory)


# Fixtures
@pytest.fixture(name="user")
def user_fixture(user_factory):
    return user_factory()


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetch:
    async def test_has_result(self, database, user):
        register_user({**user.dict()})
        getter = attrgetter("email", "password_hash")

        async with database.transaction():
            result = await user_repository.fetch(user.id)
            assert getter(user) == getter(result)

    async def test_has_no_result(self, database, user):
        async with database.transaction():
            result = await user_repository.fetch(user.id)
            assert not result


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchByEmail:
    async def test_has_result(self, database, user):
        register_user({**user.dict()})
        getter = attrgetter("email", "password_hash")

        async with database.transaction():
            result = await user_repository.fetch_by_email(user.email)
            assert getter(user) == getter(result)

    async def test_has_no_result(self, database, user):
        async with database.transaction():
            result = await user_repository.fetch_by_email(user.email)
            assert not result


@pytest.mark.integration
@pytest.mark.asyncio
class TestPersist:
    async def test_unique_insertion(self, database, user):
        getter = attrgetter("email", "password_hash")
        email, password_hash = getter(user)

        async with database.transaction():
            result = await user_repository.persist(email, password_hash)
            assert email, password_hash == getter(result)

    async def test_non_unique_insertion(self, database, user):
        email, password_hash = attrgetter("email", "password_hash")(user)
        register_user({**user.dict()})

        with pytest.raises(UniqueViolationError):
            async with database.transaction():
                await user_repository.persist(email, password_hash)
