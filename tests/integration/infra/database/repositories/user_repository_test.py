from operator import attrgetter

import pytest
from asyncpg.exceptions import UniqueViolationError
from pytest_factoryboy import register

from tests.factories.entitiy_factories import UserRegistryFactory
from tests.factories.model_factories import register_user
from todolist.infra.database.repositories import user_repository

# Factory registering
FACTORIES = [
    UserRegistryFactory,
]

for factory in FACTORIES:
    register(factory)


# Fixtures
@pytest.fixture(name="user_registry")
def user_registry_fixture(user_registry_factory):
    return user_registry_factory()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_by_email(database, user_registry):
    register_user({**user_registry.dict()})
    getter = attrgetter("email", "password_hash")

    async with database.transaction():
        result = await user_repository.fetch_by_email(user_registry.email)
        assert getter(result) == getter(user_registry)


@pytest.mark.integration
@pytest.mark.asyncio
class TestRegister:
    getter = attrgetter("email", "password_hash")

    async def test_unique_insertion(self, database, user_registry):
        async with database.transaction():
            result = await user_repository.register(user_registry)
            assert self.getter(result) == self.getter(user_registry)

    async def test_non_unique_insertion(self, database, user_registry):
        register_user({**user_registry.dict()})

        with pytest.raises(UniqueViolationError):
            async with database.transaction():
                await user_repository.register(user_registry)
