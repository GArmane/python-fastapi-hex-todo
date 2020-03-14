import pytest

from todolist.config.environment import (
    Settings,
    get_current_settings,
    get_initial_settings,
)


@pytest.mark.unit
def test_settings():
    assert Settings()


@pytest.mark.unit
def test_get_current_settings():
    assert get_current_settings()


@pytest.mark.unit
def test_initial_settings():
    assert get_initial_settings()
