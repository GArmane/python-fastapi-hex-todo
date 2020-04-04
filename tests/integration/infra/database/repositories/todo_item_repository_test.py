from functools import partial
from operator import attrgetter

import pytest
from pytest_factoryboy import register

from tests.factories.entitiy_factories import (
    CreateTodoItemDtoFactory,
    UpdateTodoItemDtoFactory,
)
from tests.factories.model_factories import insert_todo_item
from todolist.infra.database.repositories.todo_item_repository import (
    create_one,
    delete_one,
    exist_by_id,
    get_all,
    get_one_by_id,
    replace_one_by_id,
    update_one_by_id,
)

FACTORIES = [
    CreateTodoItemDtoFactory,
    UpdateTodoItemDtoFactory,
]

for factory in FACTORIES:
    register(factory)


def make_many(factory, amount=3):
    return [factory() for _ in range(amount)]


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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_one(database, create_todo_item_dto):
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await create_one(create_todo_item_dto)
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_one(database, create_todo_item_dto):
    id_ = 1
    insert_todo_item({**create_todo_item_dto.dict(), "id": id_})

    async with database.transaction():
        assert await delete_one(id_)
        assert not await delete_one(id_)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_exists_by_id(database, create_todo_item_dtos):
    values = [
        {**value.dict(), "id": idx + 1}
        for idx, value in enumerate(create_todo_item_dtos(5))
    ]
    insert_todo_item(values)

    async with database.transaction():
        for id_ in range(1, 6):
            assert await exist_by_id(id_)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all(database, create_todo_item_dtos):
    values = create_todo_item_dtos(5)
    insert_todo_item([dto.dict() for idx, dto in enumerate(values)])
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        results = await get_all()
        for result, value in zip(results, values):
            assert getter(result) == getter(value)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_one(database, create_todo_item_dto):
    id_ = 1
    insert_todo_item({**create_todo_item_dto.dict(), "id": id_})
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await get_one_by_id(id_)
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_replace_one_by_id(database, create_todo_item_dto):
    id_ = 1
    insert_todo_item(
        {
            **create_todo_item_dto.dict(),
            "msg": "message to replace",
            "is_done": False,
            "id": id_,
        }
    )
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await replace_one_by_id(create_todo_item_dto, id_)
        assert getter(result) == getter(create_todo_item_dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_one_by_id(database, create_todo_item_dto, update_todo_item_dto):
    id_ = 1
    insert_todo_item(
        {
            **create_todo_item_dto.dict(),
            "id": id_,
        }
    )
    getter = attrgetter("msg", "is_done")

    async with database.transaction():
        result = await update_one_by_id(update_todo_item_dto, id_)
        assert getter(result) == getter(update_todo_item_dto)
