import pytest

from todolist.core.accounts.services.exceptions import EmailNotUniqueError


def test_email_not_unique_error():
    email = "some@email.com"
    msg = "some message"

    error = EmailNotUniqueError(email, msg)
    assert error.as_dict() == {"msg": msg, "email": email}

    with pytest.raises(EmailNotUniqueError):
        raise error
