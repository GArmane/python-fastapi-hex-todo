import pytest

from todolist.core.todo.protocols import TodoItemRepo
from todolist.core.todo.services import todo_item_service


@pytest.fixture()
def repo(mock_module):
    return mock_module("todo_item_repo", TodoItemRepo)


# Tests
@pytest.mark.unit
@pytest.mark.asyncio
async def test_create(repo, user_registry, create_todo_item_dto, todo_item):
    # Setup
    repo.persist.return_value = todo_item

    # Test
    result = await todo_item_service.create(repo, user_registry, create_todo_item_dto)

    # Assertions
    repo.persist.assert_called_once_with(user_registry, create_todo_item_dto)
    assert result == todo_item


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete(repo, user_registry):
    # Setup
    id_ = 1
    repo.delete.return_value = True

    # Tests
    result = await todo_item_service.delete(repo, user_registry, id_)

    # Assertions
    repo.delete.assert_called_once_with(user_registry, id_)
    assert result is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get(repo, user_registry, todo_item):
    # Setup
    id_ = todo_item.id
    repo.fetch.return_value = todo_item

    # Tests
    result = await todo_item_service.get(repo, user_registry, id_)

    # Assertions
    repo.fetch.assert_called_once_with(user_registry, id_)
    assert result == todo_item


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_all_by_user(repo, user_registry, todo_items):
    # Setup
    items = todo_items()
    repo.fetch_all_by_user.return_value = items

    # Tests
    result = await todo_item_service.get_all(repo, user_registry)

    # Assertions
    repo.fetch_all_by_user.assert_called_once_with(user_registry)
    assert result == items


@pytest.mark.unit
@pytest.mark.asyncio
class TestUpdate:
    async def test_when_is_create(
        self, repo, user_registry, create_todo_item_dto, todo_item
    ):
        # Setup
        id_ = 1
        repo.replace.return_value = todo_item

        # Tests
        result = await todo_item_service.update(
            repo, user_registry, create_todo_item_dto, id_
        )

        # Assertions
        repo.replace.assert_called_once_with(user_registry, create_todo_item_dto, id_)
        assert result == todo_item

    async def test_when_is_update(
        self, repo, user_registry, update_todo_item_dto, todo_item
    ):
        # Setup
        id_ = 1
        repo.update.return_value = todo_item

        # Tests
        result = await todo_item_service.update(
            repo, user_registry, update_todo_item_dto, id_
        )

        # Assertions
        repo.update.assert_called_once_with(user_registry, update_todo_item_dto, id_)
        assert result == todo_item
