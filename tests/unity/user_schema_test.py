import pytest  # type: ignore
from pydantic import ValidationError

from api.settings.router import settings
from api.users.schema import UserBase, UserDB, UserIn, UserOut
from api.utils import generator


def test_user_base():
    """Test UserBase validator."""
    name = str(generator.name())
    email = str(generator.email())
    assert UserBase(name=name, email=email)  # type: ignore

    with pytest.raises(ValidationError):
        UserBase(name="a", email=email)  # type: ignore

    with pytest.raises(ValidationError):
        UserBase(name=name, email="a")  # type: ignore


def test_user_in():
    """Test UserIn validator."""
    name = str(generator.name())
    email = str(generator.email())
    password = generator.password()
    assert UserIn(name=name, email=email, password=password)  # type: ignore


def test_user_out():
    """Test UserOut validator."""
    name = generator.name()
    email = generator.email()
    key = generator.uuid()
    creation_date = generator.now()
    assert UserOut(
        name=name,
        email=email,  # type: ignore
        key=key,
        active=True,
        verified=True,
        blocked=False,
        password_setting_date=creation_date,
        password_attempts_count=0,
        need_password_change=False,
    )  # type: ignore


def test_user_db():
    """Test UserDB validator."""
    key = generator.uuid()
    name = generator.name()
    email = generator.email()
    password = generator.password()
    salt = generator.salt()
    password_hash = generator.hasher(password, salt)
    creation_date = generator.now()
    assert UserDB(
        key=key,
        name=name,
        email=email,  # type: ignore
        password_hash=password_hash,
        salt=salt,
        active=True,
        verified=True,
        blocked=False,
        password_setting_date=creation_date,
        password_attempts_count=0,
        need_password_change=False,
    )


def test_user_password():  # type: ignore
    """Test password validation."""
    # Test names must contain a speace
    with pytest.raises(ValidationError):
        UserBase(name="test", email=generator.email())  # type: ignore

    # Test names must contain a speace
    with pytest.raises(ValidationError):
        UserIn(name="test", email=generator.email(), password=generator.password())  # type: ignore

    # Test Password Policy
    s = settings.users.password_policy

    # Test Size
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(size=s.min_length - 1))  # type: ignore

    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(size=s.max_length + 1))  # type: ignore

    # Test Password Requirements
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(lower=0))  # type: ignore

    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(uper=0))  # type: ignore

    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(special=0))  # type: ignore

    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password=generator.password(numbers=0))  # type: ignore

    # Disable requirements
    s.active = False
    assert UserIn(name=generator.name(), email=generator.email(), password="a")  # type: ignore

    # Enable requirements
    s.active = True
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password="a")  # type: ignore


def test_user_name():
    """Test name validation."""
    with pytest.raises(ValidationError):
        UserIn(name="A", email=generator.email(), password=generator.password())  # type: ignore


def test_user_email():
    """Test email validation."""
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email="a", password=generator.password())  # type: ignore
