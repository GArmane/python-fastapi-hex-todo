from asyncio import Future
import pytest

from todolist.domains.todo.services.todo_item_service import create_one_todo_item


PERSIST_ONE_FN_NAME = "persist_one_fn"


@pytest.fixture(name=PERSIST_ONE_FN_NAME)
def persist_one_fn_fixture(mocker):
    return mocker.MagicMock(name=PERSIST_ONE_FN_NAME, return_value=Future())


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_one_todo_item(persist_one_fn, create_todo_item_dto, todo_item):
    # Setup
    persist_one_fn.return_value.set_result(todo_item)

    # Test
    result = await create_one_todo_item(persist_one_fn, create_todo_item_dto)

    # Assertions
    persist_one_fn.assert_called_once_with(create_todo_item_dto)
    assert result == todo_item
