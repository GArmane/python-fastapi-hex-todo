from functools import partial
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from tests.utils.asserts import assert_validation_error
from todolist.core.accounts.entities.user import User

DataType = Dict[str, Any]


@pytest.fixture(name="valid_data")
def valid_data_fixture() -> DataType:
    return {
        "id": 1,
        "email": "example@example.com",
        "password_hash": """
            $argon2i$v=19$m=512,t=2,p=2$aI2R0hpDyLm3ltLa+1/rvQ$LqPKjd6n8yniKtAithoR7A
        """,
    }


@pytest.fixture(name="invalid_data")
def invalid_data_fixture() -> DataType:
    return {
        "id": "some string",
        "email": "some email",
        "password_hash": ["some_hash"],
    }


@pytest.mark.unit
class TestUser:
    class TestModel:
        def test_validation(self, valid_data):
            assert User(**valid_data)

        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                assert User(**invalid_data)

        def test_immutability(self, valid_data):
            entity = User(**valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"id": "some_id"})
                User(**valid_data)

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("id")
                User(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"email": ["some string"]})
                User(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("email")
                User(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPasswordHash:
        assert_validation_error = partial(assert_validation_error, 1, "password_hash")

        def test_must_be_secret_str(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"password_hash": ["some string"]})
                User(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("password_hash")
                User(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)
