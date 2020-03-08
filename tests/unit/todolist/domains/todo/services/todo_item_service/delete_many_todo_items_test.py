import pytest

from todolist.domains.todo.services.todo_item_service import delete_many_todo_items


DELETE_MANY_FN_NAME = "delete_many_fn"


@pytest.fixture(name=DELETE_MANY_FN_NAME)
def delete_many_fn_fixture(mocker):
    return mocker.stub(name=DELETE_MANY_FN_NAME)


@pytest.mark.unit
def test_delete_many_todo_items(delete_many_fn):
    # Setup
    ids = range(1, 6)
    delete_many_fn.return_value = True

    # Test
    result = delete_many_todo_items(delete_many_fn, ids)

    #  Assertions
    delete_many_fn.assert_called_once_with(ids)
    assert result is True
