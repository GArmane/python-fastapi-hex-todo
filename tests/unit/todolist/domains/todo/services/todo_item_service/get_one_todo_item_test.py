import pytest

from todolist.domains.todo.services.todo_item_service import get_one_todo_item


FETCH_ONE_FN_NAME = "fetch_one_fn"


@pytest.fixture(name=FETCH_ONE_FN_NAME)
def fetch_one_fn_fixture(mocker):
    return mocker.stub(name=FETCH_ONE_FN_NAME)


@pytest.mark.unit
def test_fetch_one_item(fetch_one_fn, todo_item):
    # Setup
    id_ = todo_item.id
    fetch_one_fn.return_value = todo_item

    # Tests
    result = get_one_todo_item(fetch_one_fn, id_)

    # Assertions
    fetch_one_fn.assert_called_once_with(id_)
    assert result == todo_item
