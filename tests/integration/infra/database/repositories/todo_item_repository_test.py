from functools import partial
from operator import attrgetter

import pytest
from pytest_factoryboy import register

from tests.factories.entitiy_factories import (
    CreateTodoItemDtoFactory,
    UpdateTodoItemDtoFactory,
    UserFactory,
)
from tests.factories.model_factories import insert_todo_item, register_user
from tests.factories.utils import make_many
from todolist.core.accounts.entities.user import UserRegistry
from todolist.infra.database.repositories import todo_item_repository

FACTORIES = [
    CreateTodoItemDtoFactory,
    UpdateTodoItemDtoFactory,
    UserFactory,
]

for factory in FACTORIES:
    register(factory)


@pytest.fixture(name="create_todo_item_dto")
def create_todo_item_dto_fixture(create_todo_item_dto_factory):
    return create_todo_item_dto_factory()


@pytest.fixture(name="create_todo_item_dtos")
def create_todo_item_dtos_fixture(create_todo_item_dto_factory):
    return partial(make_many, create_todo_item_dto_factory)


@pytest.fixture(name="update_todo_item_dto")
def update_todo_item_dto_fixture(update_todo_item_dto_factory):
    return update_todo_item_dto_factory()


@pytest.fixture(name="update_todo_item_dtos")
def update_todo_item_dtos_fixture(update_todo_item_dto_factory):
    return partial(make_many, update_todo_item_dto_factory)


@pytest.fixture(name="user_registry")
def user_registry(user_factory):
    values = user_factory().dict()
    register_user(values)
    return UserRegistry(**values)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete(database, user_registry, create_todo_item_dto):
    id_ = 1
    insert_todo_item(
        {**create_todo_item_dto.dict(), "id": id_, "user_id": user_registry.id}
    )

    async with database.transaction():
        assert await todo_item_repository.delete(user_registry, id_)
        assert not await todo_item_repository.delete(user_registry, id_)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exists_by_id(database, user_registry, create_todo_item_dtos):
    values = [
        {**value.dict(), "id": idx + 1, "user_id": user_registry.id}
        for idx, value in enumerate(create_todo_item_dtos(5))
    ]
    insert_todo_item(values)

    async with database.transaction():
        for id_ in range(1, 6):
            assert await todo_item_repository.exists_by_id(id_)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_all_by_user(database, user_registry, create_todo_item_dtos):
    values = create_todo_item_dtos(5)
    insert_todo_item([{**dto.dict(), "user_id": user_registry.id} for dto in values])
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        results = await todo_item_repository.fetch_all_by_user(user_registry)
        for result, value in zip(results, values):
            assert getter(result) == getter(value)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch(database, user_registry, create_todo_item_dto):
    id_ = 1
    insert_todo_item(
        {**create_todo_item_dto.dict(), "id": id_, "user_id": user_registry.id}
    )
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await todo_item_repository.fetch(user_registry, id_)
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_persist(database, user_registry, create_todo_item_dto):
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await todo_item_repository.persist(user_registry, create_todo_item_dto)
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_replace(database, user_registry, create_todo_item_dto):
    id_ = 1
    insert_todo_item(
        {
            **create_todo_item_dto.dict(),
            "msg": "message to replace",
            "is_done": False,
            "id": id_,
            "user_id": user_registry.id,
        }
    )
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await todo_item_repository.replace(
            user_registry, create_todo_item_dto, id_
        )
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update(
    database, user_registry, create_todo_item_dto, update_todo_item_dto
):
    id_ = 1
    insert_todo_item(
        {**create_todo_item_dto.dict(), "id": id_, "user_id": user_registry.id}
    )
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await todo_item_repository.update(
            user_registry, update_todo_item_dto, id_
        )
        assert getter(result) == getter(update_todo_item_dto)
