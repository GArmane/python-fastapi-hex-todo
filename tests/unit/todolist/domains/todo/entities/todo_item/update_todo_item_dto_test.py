from functools import partial
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from tests.utils import assert_validation_error
from todolist.domains.todo.entities.todo_item import UpdateTodoItemDto


# Types
DataType = Dict[str, Any]


@pytest.fixture(name="valid_data")
def valid_data_fixture() -> DataType:
    return {
        "msg": "some message",
        "is_done": True,
    }


@pytest.fixture(name="invalid_data")
def invalid_data_fixture() -> DataType:
    return {"msg": ["some string"], "is_done": "some bool"}


class TestCreateTodoItemDto:
    class TestModel:
        def test_validation(self, valid_data):
            assert UpdateTodoItemDto(**valid_data)

        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                UpdateTodoItemDto(**invalid_data)

        def test_immutability(self, valid_data):
            entity = UpdateTodoItemDto(**valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestMsg:
        assert_validation_error = partial(assert_validation_error, 1, "msg")

        def test_must_be_str(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": ["some string"]})
                UpdateTodoItemDto(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_optional(self, valid_data):
            valid_data.pop("msg")
            entity = UpdateTodoItemDto(**valid_data)
            assert entity.msg is None

        def test_min_length_gte_3(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": "a" * 2})
                UpdateTodoItemDto(**valid_data)

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length_lte_100(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": "a" * 101})
                UpdateTodoItemDto(**valid_data)

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestIsDone:
        assert_validation_error = partial(assert_validation_error, 1, "is_done")

        def test_must_be_bool(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"is_done": "some bool"})
                UpdateTodoItemDto(**valid_data)

            self.assert_validation_error("type_error.bool", excinfo)

        def test_is_optional(self, valid_data):
            valid_data.pop("is_done")
            entity = UpdateTodoItemDto(**valid_data)
            assert entity.is_done is None
