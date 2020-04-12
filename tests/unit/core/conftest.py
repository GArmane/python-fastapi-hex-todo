from asyncio import Future

import pytest


@pytest.fixture(name="repo_fn_factory")
def repo_fn_factory_fixture(mocker):
    return lambda name: mocker.MagicMock(name=name, return_value=Future())
