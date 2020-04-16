import pytest

from todolist.core.accounts.services.exceptions import (
    EmailNotUniqueError,
    UserNotFoundError,
)


@pytest.mark.unit
def test_email_not_unique_error():
    email = "some@email.com"
    msg = "some message"

    error = EmailNotUniqueError(email, msg)
    assert error.as_dict() == {"msg": msg, "email": email}

    with pytest.raises(EmailNotUniqueError):
        raise error


@pytest.mark.unit
def test_user_not_found_error():
    id_ = 1
    msg = "some message"

    error = UserNotFoundError(id_, msg)
    assert error.as_dict() == {"msg": msg, "user_id": id_}

    with pytest.raises(UserNotFoundError):
        raise error
