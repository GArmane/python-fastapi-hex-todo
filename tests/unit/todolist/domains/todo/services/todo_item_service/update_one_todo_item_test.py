import pytest

from todolist.domains.todo.services.todo_item_service import update_one_todo_item


UPDATE_ONE_FN_NAME = "update_one_fn"


@pytest.fixture(name=UPDATE_ONE_FN_NAME)
def update_many_fn_fixture(mocker):
    return mocker.stub(name=UPDATE_ONE_FN_NAME)


@pytest.mark.unit
def test_update_one_todo_item(update_one_fn, update_todo_item_dto, todo_item):
    # Setup
    id_ = 1
    update_one_fn.return_value = todo_item

    # Tests
    result = update_one_todo_item(update_one_fn, update_todo_item_dto, id_)

    # Assertions
    update_one_fn.assert_called_once_with(update_todo_item_dto, id_)
    assert result == todo_item
