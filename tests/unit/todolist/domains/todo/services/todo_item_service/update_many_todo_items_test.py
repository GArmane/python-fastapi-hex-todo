from asyncio import Future

import pytest

from todolist.domains.todo.services.todo_item_service import update_many_todo_items


UPDATE_MANY_FN_NAME = "update_many_fn"


@pytest.fixture(name=UPDATE_MANY_FN_NAME)
def update_many_fn_fixture(mocker):
    return mocker.MagicMock(name=UPDATE_MANY_FN_NAME, return_value=Future())


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_many_todo_items(
    update_many_fn, update_todo_item_dtos, todo_items
):
    # Setup
    dtos = update_todo_item_dtos()
    ids = range(1, len(dtos) + 1)
    items = todo_items()
    update_many_fn.return_value.set_result(items)

    # Tests
    result = await update_many_todo_items(update_many_fn, dtos, ids)

    # Assertions
    update_many_fn.assert_called_once()
    assert result == items
