import factory

from tests.factories.providers import PasswordHashProvider
from todolist.core.accounts.entities.user import Credentials, User, UserRegistry
from todolist.core.todo.entities.todo_item import (
    CreateTodoItemDto,
    TodoItem,
    UpdateTodoItemDto,
)


# Register providers
providers = [PasswordHashProvider]

for provider in providers:
    factory.Faker.add_provider(provider)


# User
class CredentialsFactory(factory.Factory):
    class Meta:
        model = Credentials

    email = factory.Faker("email")
    password = factory.Faker("password", length=16)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    email = factory.Faker("email")
    password_hash = factory.Faker("password_hash")


class UserRegistryFactory(factory.Factory):
    class Meta:
        model = UserRegistry

    email = factory.Faker("email")
    password_hash = factory.Faker("password_hash")


# TodoItem
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
