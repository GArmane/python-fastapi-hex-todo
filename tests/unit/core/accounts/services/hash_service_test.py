import pytest

from todolist.core.accounts.services import hash_service


@pytest.mark.unit
def test_hash_returns_hashed_value():
    value = "some value"
    result = hash_service.hash_(value)
    second_result = hash_service.hash_(value)

    assert result != value
    assert result != second_result


@pytest.mark.unit
def test_verify_valid_value():
    value = "some value"
    result = hash_service.hash_(value)

    assert hash_service.verify(value, result)


@pytest.mark.unit
def test_verify_invalid_value():
    value = "some value"
    result = hash_service.hash_("other value")

    assert not hash_service.verify(value, result)
