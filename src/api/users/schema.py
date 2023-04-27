"""User models."""
import string
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator  # type: ignore

from api.config import configuration
from api.utils import generator


class UserBase(BaseModel):  # pylint: disable=too-few-public-methods
    """User model."""

    name: str = Field(example="John Doe", title="Full name", max_length=250, min_length=5)
    email: EmailStr = Field(example="john.doe@email.com", title="Email")

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserIn(UserBase):
    """User model for creating a new user."""

    password: str = Field(example="P@ssw0rd", title="Password")

    @validator("password")
    def password_validator(cls, password) -> str:  # pylint: disable=no-self-argument
        """Validate password."""
        if configuration.users.password_policy.active is True:
            if len(password) < configuration.users.password_policy.min_length:
                raise ValueError(
                    f"Password is too short. It must be at least {configuration.users.password_policy.min_length} characters long."  # flake8: noqa: E501
                )
            if len(password) > configuration.users.password_policy.max_length:
                raise ValueError(
                    f"Password is too long. It must be at most {configuration.users.password_policy.max_length} characters long."  # flake8: noqa: E501
                )
            if sum(1 for c in password if c.isupper()) < configuration.users.password_policy.min_upper:
                raise ValueError(
                    f"Password must contain at least {configuration.users.password_policy.min_upper} uppercase letter(s)."  # flake8: noqa: E501
                )
            if sum(1 for c in password if c.islower()) < configuration.users.password_policy.min_lower:
                raise ValueError(
                    f"Password must contain at least {configuration.users.password_policy.min_lower} lowercase letter(s)."  # flake8: noqa: E501
                )
            if sum(1 for c in password if c.isdigit()) < configuration.users.password_policy.min_digits:
                raise ValueError(
                    f"Password must contain at least {configuration.users.password_policy.min_digits} digit(s)."
                )
            if sum(1 for c in password if c in string.punctuation) < configuration.users.password_policy.min_special:
                raise ValueError(
                    f"Password must contain at least {configuration.users.password_policy.min_special} special character(s)."  # flake8: noqa: E501
                )

        return password

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserOut(BaseModel):
    """User model for returning a user."""

    key: str = Field(example="a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6", title="Unique Key")
    email: EmailStr = Field(example="john.doe@email.com", title="Email")
    created_at: datetime = Field(example="2021-01-01T00:00:00.000000", title="Created at", default=datetime.now())
    changed_at: datetime = Field(
        example="2021-01-01T00:00:00.000000",
        title="Last changed date",
        default=datetime.now(),
    )
    is_verified: bool = Field(example="false", title="Is the user email verified?")
    is_active: bool = Field(example="true", title="Is the user email active?")
    is_blocked: bool = Field(example="false", title="Is the user email blocked?")
    needs_password_reset: bool = False

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserDB(UserBase):
    """User model for storing a user in the database."""

    key: str = generator.get_uuid()
    is_verified: bool = configuration.users.default_verified
    is_active: bool = configuration.users.default_active
    is_blocked: bool = configuration.users.default_blocked
    needs_password_reset: bool = False
    hashed_password: str
    salt: str = generator.get_salt()
    created_at: datetime = datetime.now()
    changed_at: datetime = datetime.now()

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
