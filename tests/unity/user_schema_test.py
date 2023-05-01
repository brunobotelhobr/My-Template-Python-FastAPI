import pytest  # type: ignore
from pydantic import ValidationError

from api.users.schema import UserBase, UserDB, UserIn, UserOut
from api.utils import generator


def test_user_base():
    """Test UserBase validator."""
    name = generator.name()
    email = generator.email()
    user = UserBase(name=name, email=email)  # type: ignore
    assert user.name == name
    assert user.email == email


def test_user_in():
    """Test UserIn validator."""
    name = generator.name()
    email = generator.email()
    password = generator.password()
    user = UserIn(name=name, email=email, password=password)  # type: ignore
    assert user.name == name
    assert user.email == email
    assert user.password == password


# def test_user_out():
#     """Test UserOut validator."""
#     name = generator.name()
#     email = generator.email()
#     key = generator.uuid()
#     creation_date = generator.now()
#     user = UserOut(name=name, email=email, key=key, active=True, verified=True, blocked=False,
#                    password_setiing_date=creation_date, password_attempts_count=0, need_password_change=False)  # type: ignore
#     assert user.name == name
#     assert user.email == email
#     assert user.key == key
#     assert user.active
#     assert user.verified
#     assert not user.blocked
#     assert user.password_setiing_date == creation_date
#     assert user.password_attempts_count == 0
#     assert not user.need_password_change

#     #Test invalid values
#     with pytest.raises(ValidationError):
#         UserOut(name=name, email=email, key=key, active=True, verified=True, blocked=False,
#                 password_setiing_date=creation_date, password_attempts_count=-1, need_password_change=False)

#     with pytest.raises(ValidationError):
#         UserOut(name=name, email=email, key=key, active=True, verified=True, blocked=False,
#                 password_setiing_date=creation_date, password_attempts_count=0, need_password_change=1)


# def test_user_db():
#     """Test UserDB validator."""
#     key = generator.uuid()
#     name = generator.name()
#     email = generator.email()
#     password = generator.password()
#     salt = generator.salt()
#     password_hash = generator.hasher(password, salt)
#     creation_date = generator.now()
#     user = UserDB(key=key, name=name, email=email, password_hash=password_hash, salt=salt, active=True, verified=True,
#                   locked=False, password_setiing_date=creation_date, password_attempts_count=0, need_password_change=False)  # type: ignore
#     assert user.name == name
#     assert user.email == email
#     assert user.password_hash
#     assert user.salt == salt
#     assert user.active
#     assert user.verified
#     assert not user.blocked
#     assert user.password_setiing_date == creation_date
#     assert user.password_attempts_count == 0
#     assert not user.need_password_change
