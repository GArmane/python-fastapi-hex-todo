import factory

from todolist.domains.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)


class TodoItemFactory(factory.Factory):
    class Meta:
        model = TodoItem

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    msg = factory.Faker("sentence", variable_nb_words=True)
    is_done = factory.Faker("pybool")


class CreateTodoItemDtoFactory(factory.Factory):
    class Meta:
        model = CreateTodoItemDto

    msg = factory.Faker("sentence", variable_nb_words=True)
    is_done = factory.Faker("pybool")


class UpdateTodoItemDtoFactory(factory.Factory):
    class Meta:
        model = UpdateTodoItemDto

    msg = factory.Faker("sentence", variable_nb_words=True)
    is_done = factory.Faker("pybool")
