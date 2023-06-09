"""temp."""
import pytest
from pydantic import ValidationError

from api.core.utils import generator
from api.settings.router import settings
from api.users.schema import UserBase, UserDB, UserIn, UserOut


@pytest.mark.order(2)
def test_user_base():
    """Test UserBase validator."""
    name = str(generator.name())
    email = str(generator.email())
    assert UserBase(name=name, email=email)

    with pytest.raises(ValidationError):
        UserBase(name="", email=email)

    with pytest.raises(ValidationError):
        UserBase(name="a" * 20, email=email)

    with pytest.raises(ValidationError):
        UserBase(name=name, email="a")


@pytest.mark.order(2)
def test_user_in():
    """Test UserIn validator."""
    name = str(generator.name())
    email = str(generator.email())
    password = generator.password()
    assert UserIn(name=name, email=email, password=password)


@pytest.mark.order(2)
def test_user_out():
    """Test UserOut validator."""
    name = generator.name()
    email = generator.email()
    key = generator.uuid()
    creation_date = generator.now()
    assert UserOut(
        name=name,
        email=email,
        key=key,
        active=True,
        verified=True,
        blocked=False,
        password_setting_date=creation_date,
        password_attempts_count=0,
        need_password_change=False,
    )


@pytest.mark.order(2)
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
        email=email,
        password_hash=password_hash,
        salt=salt,
        active=True,
        verified=True,
        blocked=False,
        password_setting_date=creation_date,
        password_attempts_count=0,
        need_password_change=False,
    )


@pytest.mark.order(2)
def test_user_password():
    """Test password validation."""
    # Test names must contain a speace
    with pytest.raises(ValidationError):
        UserBase(name="test", email=generator.email())

    # Test names must contain a speace
    with pytest.raises(ValidationError):
        UserIn(name="test", email=generator.email(), password=generator.password())

    # Test Password Policy
    s = settings.users.password_policy

    # Test Size
    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(size=s.min_length - 1),
        )

    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(size=s.max_length + 1),
        )

    # Test Password Requirements
    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(lower=0),
        )

    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(uper=0),
        )

    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(special=0),
        )

    with pytest.raises(ValidationError):
        UserIn(
            name=generator.name(),
            email=generator.email(),
            password=generator.password(numbers=0),
        )

    # Disable requirements
    s.active = False
    assert UserIn(name=generator.name(), email=generator.email(), password="a")

    # Enable requirements
    s.active = True
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email=generator.email(), password="a")


@pytest.mark.order(2)
def test_user_name():
    """Test name validation."""
    with pytest.raises(ValidationError):
        UserIn(name="A", email=generator.email(), password=generator.password())


@pytest.mark.order(2)
def test_user_email():
    """Test email validation."""
    with pytest.raises(ValidationError):
        UserIn(name=generator.name(), email="a", password=generator.password())
