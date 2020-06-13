from functools import partial

import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import (
    CreateTodoItemDtoFactory,
    TodoItemFactory,
    UpdateTodoItemDtoFactory,
)
from tests.factories.utils import make_many

FACTORIES = [
    CreateTodoItemDtoFactory,
    TodoItemFactory,
    UpdateTodoItemDtoFactory,
]

for factory in FACTORIES:
    register(factory)


@pytest.fixture()
def create_todo_item_dto(create_todo_item_dto_factory):
    return create_todo_item_dto_factory()


@pytest.fixture()
def create_todo_item_dtos(create_todo_item_dto_factory):
    return partial(make_many, create_todo_item_dto_factory)


@pytest.fixture()
def todo_item(todo_item_factory):
    return todo_item_factory()


@pytest.fixture()
def todo_items(todo_item_factory):
    return partial(make_many, todo_item_factory)


@pytest.fixture()
def update_todo_item_dto(update_todo_item_dto_factory):
    return update_todo_item_dto_factory()


@pytest.fixture()
def update_todo_item_dtos(update_todo_item_dto_factory):
    return partial(make_many, update_todo_item_dto_factory)
