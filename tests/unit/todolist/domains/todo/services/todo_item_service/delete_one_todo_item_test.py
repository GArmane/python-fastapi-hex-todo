import pytest

from todolist.domains.todo.services.todo_item_service import delete_one_todo_item


DELETE_ONE_FN_NAME = "delete_one_fn"


@pytest.fixture(name=DELETE_ONE_FN_NAME)
def delete_one_fn_fixture(mocker):
    return mocker.stub(name=DELETE_ONE_FN_NAME)


@pytest.mark.unit
def test_delete_one_todo_item(delete_one_fn):
    # Setup
    id_ = 1
    delete_one_fn.return_value = True

    # Tests
    result = delete_one_todo_item(delete_one_fn, id_)

    # Assertions
    delete_one_fn.assert_called_once_with(id_)
    assert result is True
