from functools import partial
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from tests.utils.asserts import assert_validation_error
from todolist.core.accounts.entities.user import Credentials

DataType = Dict[str, Any]


@pytest.fixture(name="valid_data")
def valid_data_fixture() -> DataType:
    return {
        "email": "example@example.com",
        "password": "some password",
    }


@pytest.fixture(name="invalid_data")
def invalid_data_fixture() -> DataType:
    return {
        "email": "some email",
        "password_hash": ["some_hash"],
    }


@pytest.mark.unit
class TestCredentials:
    class TestModel:
        def test_validation(self, valid_data):
            assert Credentials(**valid_data)

        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                assert Credentials(**invalid_data)

        def test_immutability(self, valid_data):
            entity = Credentials(**valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"email": ["some string"]})
                Credentials(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("email")
                Credentials(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPassword:
        assert_validation_error = partial(assert_validation_error, 1, "password")

        def test_must_be_secret_str(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"password": ["some string"]})
                Credentials(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("password")
                Credentials(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

        def test_min_length_gte_8(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"password": "a" * 7})
                Credentials(**valid_data)

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length_lte_128(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"password": "a" * 129})
                Credentials(**valid_data)

            self.assert_validation_error("value_error.any_str.max_length", excinfo)
