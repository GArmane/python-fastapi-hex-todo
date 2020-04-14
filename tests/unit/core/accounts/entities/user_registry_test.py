from functools import partial
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from tests.utils.asserts import assert_validation_error
from todolist.core.accounts.entities.user import UserRegistry

DataType = Dict[str, Any]


@pytest.fixture(name="valid_data")
def valid_data_fixture() -> DataType:
    return {
        "id": 1,
        "email": "example@example.com",
    }


@pytest.fixture(name="invalid_data")
def invalid_data_fixture() -> DataType:
    return {
        "id": "some id",
        "email": "some email",
    }


@pytest.mark.unit
class TestUser:
    class TestModel:
        def test_validation(self, valid_data):
            assert UserRegistry(**valid_data)

        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                assert UserRegistry(**invalid_data)

        def test_immutability(self, valid_data):
            entity = UserRegistry(**valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"id": "some_id"})
                UserRegistry(**valid_data)

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("id")
                UserRegistry(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"email": ["some string"]})
                UserRegistry(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("email")
                UserRegistry(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)
