from operator import attrgetter

import pytest
from asyncpg.exceptions import UniqueViolationError
from pytest_factoryboy import register

from tests.factories.entitiy_factories import UserFactory
from tests.factories.model_factories import register_user
from todolist.infra.database.repositories import user_repository

# Factory registering
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
async def test_fetch_by_email(database, user):
    register_user({**user.dict()})
    getter = attrgetter("email", "password_hash")

    async with database.transaction():
        result = await user_repository.fetch_by_email(user.email)
        assert getter(user) == getter(result)


@pytest.mark.integration
@pytest.mark.asyncio
class TestRegister:
    async def test_unique_insertion(self, database, user):
        getter = attrgetter("email", "password_hash")
        email, password_hash = getter(user)

        async with database.transaction():
            result = await user_repository.register(email, password_hash)
            assert email, password_hash == getter(result)

    async def test_non_unique_insertion(self, database, user):
        email, password_hash = attrgetter("email", "password_hash")(user)
        register_user({**user.dict()})

        with pytest.raises(UniqueViolationError):
            async with database.transaction():
                await user_repository.register(email, password_hash)
