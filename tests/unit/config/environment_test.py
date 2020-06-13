import pytest

from todolist.config.environment import Settings, get_settings


@pytest.mark.unit
def test_settings():
    assert Settings()


@pytest.mark.unit
def test_initial_settings():
    assert get_settings()
