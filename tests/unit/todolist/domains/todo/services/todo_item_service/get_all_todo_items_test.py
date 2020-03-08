from asyncio import Future

import pytest

from todolist.domains.todo.services.todo_item_service import get_all_todo_items


FETCH_ALL_FN_NAME = "fetch_all_fn"


@pytest.fixture(name=FETCH_ALL_FN_NAME)
def fetch_all_fn_fixture(mocker):
    return mocker.MagicMock(name=FETCH_ALL_FN_NAME, return_value=Future())


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_all_todo_items(fetch_all_fn, todo_items):
    # Setup
    items = todo_items()
    fetch_all_fn.return_value.set_result(items)

    # Tests
    result = await get_all_todo_items(fetch_all_fn)

    # Assertions
    fetch_all_fn.assert_called_once_with()
    assert result == items
