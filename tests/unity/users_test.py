"""Test the main module."""
from pytest import raises

from api.users import settings
from api.utils import generator
from src.api.users import crud, model, router, schema


def test_config_user() -> None:
    """Test config."""
    c = settings.UserConfig()
    # check if is bool
    assert isinstance(c.allow_delete, bool)
    assert isinstance(c.default_active, bool)
    assert isinstance(c.default_blocked, bool)
    assert isinstance(c.default_verified, bool)
    assert isinstance(c.password_policy, settings.PasswordPolicy)


def test_config_user_password_policy():
    """Test password policy."""
    p = settings.PasswordPolicy()
    assert isinstance(p.active, bool)
    assert isinstance(p.min_length, int)
    assert isinstance(p.max_length, int)
    assert isinstance(p.min_upper, int)
    assert isinstance(p.min_lower, int)
    assert isinstance(p.min_digits, int)
    assert isinstance(p.min_special, int)


def test_schema_user_base():
    """Test user base."""
    b = schema.UserBase(name="John Doe", email="john@example.com")  # type: ignore
    assert isinstance(b.name, str)
    assert isinstance(b.email, str)
    # test for exception, user withou email
    raises(ValueError, schema.UserBase, name="John Doe", email="")
    # test for exception, user withou name
    raises(ValueError, schema.UserBase, name="", email="john@example.com")
    # Test for a null user
    raises(ValueError, schema.UserBase, name="", email="")
    # Test for a user with a name that is too short
    raises(ValueError, schema.UserBase, name="a", email="john@example.com")  # type: ignore
    # Test for a user with a name that is too long
    raises(ValueError, schema.UserBase, name="a" * 257, email="john@example.com")
    # Test for a user with an invalid email
    raises(ValueError, schema.UserBase, name="John Doe", email="john@example")


def test_schema_user_in():
    """Test user in."""
    i = schema.UserIn(name="John Doe", email="john@ezample.com", password="P@ssw0rd")  # type: ignore
    assert isinstance(i.name, str)
    assert isinstance(i.email, str)
    assert isinstance(i.password, str)
    # Test for a null user
    raises(ValueError, schema.UserIn, name="", email="", password="")
    # Test for a too big password
    raises(ValueError, schema.UserIn, name="John Doe", email="john@example.com", password="a" * 129)


def test_schema_user_out():
    """Test user out."""
    o = schema.UserOut(
        name="John Doe",
        email="john@ezample.com",
        changed_at="2020-01-01T00:00:00.000Z",
        created_at="2020-01-01T00:00:00.000Z",
        is_active=True,
        is_blocked=False,
        is_verified=True,
        needs_password_reset=False,
    )  # type: ignore
    assert isinstance(o.name, str)
    assert isinstance(o.email, str)
    assert isinstance(o.changed_at, str)
    assert isinstance(o.created_at, str)
    assert isinstance(o.is_active, bool)
    assert isinstance(o.is_blocked, bool)
    assert isinstance(o.is_verified, bool)
    assert isinstance(o.needs_password_reset, bool)
    # Test for a null user
    raises(
        ValueError,
        schema.UserOut,
        name="",
        email="",
        changed_at="",
        created_at="",
        is_active=False,
        is_blocked=False,
        is_verified=False,
        needs_password_reset=False,
    )
