from functools import partial
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from tests.utils import assert_validation_error
from todolist.domains.todo.entities.todo_item import TodoItem

# Types
DataType = Dict[str, Any]


# Fixtures
@pytest.fixture(name="valid_data")
def valid_data_fixture() -> DataType:
    return {
        "id": 1,
        "msg": "some message",
        "is_done": True,
    }


@pytest.fixture(name="invalid_data")
def invalid_data_fixture() -> DataType:
    return {"id": "some integer", "msg": ["some string"], "is_done": "some bool"}


@pytest.mark.unit
class TestTodoItem:
    class TestModel:
        def test_validation(self, valid_data):
            assert TodoItem(**valid_data)

        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                TodoItem(**invalid_data)

        def test_immutability(self, valid_data):
            tdi = TodoItem(**valid_data)
            for key in tdi.dict().keys():
                with pytest.raises(TypeError):
                    setattr(tdi, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"id": "some integer"})
                TodoItem(**valid_data)

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("id")
                TodoItem(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestMsg:
        assert_validation_error = partial(assert_validation_error, 1, "msg")

        def test_must_be_str(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": ["some string"]})
                TodoItem(**valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("msg")
                TodoItem(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

        def test_min_length_gte_3(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": "a" * 2})
                TodoItem(**valid_data)

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length_lte_100(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"msg": "a" * 101})
                TodoItem(**valid_data)

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestIsDone:
        assert_validation_error = partial(assert_validation_error, 1, "is_done")

        def test_must_be_bool(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.update({"is_done": "some bool"})
                TodoItem(**valid_data)

            self.assert_validation_error("type_error.bool", excinfo)

        def test_is_required(self, valid_data):
            with pytest.raises(ValidationError) as excinfo:
                valid_data.pop("is_done")
                TodoItem(**valid_data)

            self.assert_validation_error("value_error.missing", excinfo)
