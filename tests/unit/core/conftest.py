from asyncio import Future
from functools import partial

import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import UserRegistryFactory
from tests.factories.utils import make_many


FACTORIES = [UserRegistryFactory]

for factory in FACTORIES:
    register(factory)


@pytest.fixture(name="repo_fn_factory")
def repo_fn_factory_fixture(mocker):
    return lambda name: mocker.MagicMock(name=name, return_value=Future())


@pytest.fixture()
def user_registry(user_registry_factory):
    return user_registry_factory()


@pytest.fixture()
def user_registries(user_registry_factory):
    return partial(make_many, user_registry_factory)
