import factory

from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)


class TodoItemFactory(factory.Factory):
    class Meta:
        model = TodoItem

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    msg = factory.Faker("pystr", min_chars=3, max_chars=50)
    is_done = factory.Faker("pybool")


class CreateTodoItemDtoFactory(factory.Factory):
    class Meta:
        model = CreateTodoItemDto

    msg = factory.Faker("pystr", min_chars=3, max_chars=50)
    is_done = factory.Faker("pybool")


class UpdateTodoItemDtoFactory(factory.Factory):
    class Meta:
        model = UpdateTodoItemDto

    msg = factory.Faker("pystr", min_chars=3, max_chars=50)
    is_done = factory.Faker("pybool")
