def assert_validation_error(len_, loc, type_, excinfo):
    def write_message(expected, gotten):
        return f"expected: '{expected}', got: '{gotten}'"

    errors = excinfo.value.errors()
    assert len(errors) == len_, write_message(len_, len(errors))

    error, *_ = errors
    assert error["loc"] == (loc,), write_message(loc, error.get("loc", None))
    assert error["type"] == type_, write_message(type_, error.get("type", None))
