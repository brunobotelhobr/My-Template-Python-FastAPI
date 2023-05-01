"""User schema."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from api.settings.router import settings


class UserBase(BaseModel):
    """User model."""

    name: str = Field(example="John Doe", title="Full name", max_length=250, min_length=5)
    email: EmailStr = Field(example="john.doe@email.com", title="Email")

    @validator("name")
    def name_must_contain_space(cls, v):  # pylint: disable=E0213
        """Validate name must contain a space."""
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserIn(UserBase):
    """User input model."""

    password: str = Field(example="P@ssw0rd", title="Password")

    @validator("password")
    def passwords_match(cls, v):  # pylint: disable=E0213
        """Validate password and confirm_password match."""
        if settings.users.password_policy.active:
            if len(v) < settings.users.password_policy.min_length:
                raise ValueError("must be at least " + str(settings.users.password_policy.min_length) + " characters")
            if len(v) > settings.users.password_policy.max_length:
                raise ValueError("must be less than " + str(settings.users.password_policy.max_length) + " characters")
            if settings.users.password_policy.min_upper > 0:
                c = 0
                for i in v:
                    if i.isupper():
                        c = c + 1
                if c < settings.users.password_policy.min_upper:
                    raise ValueError("must contain at least " + str(settings.users.password_policy.min_upper) + " upper case characters")
            if settings.users.password_policy.min_lower > 0:
                c = 0
                for i in v:
                    if i.islower():
                        c = c + 1
                if c < settings.users.password_policy.min_lower:
                    raise ValueError("must contain at least " + str(settings.users.password_policy.min_lower) + " lower case characters")
            if settings.users.password_policy.min_digits > 0:
                c = 0
                for i in v:
                    if i.isdigit():
                        c = c + 1
                if c < settings.users.password_policy.min_digits:
                    raise ValueError("must contain at least " + str(settings.users.password_policy.min_digits) + " digits")
            if settings.users.password_policy.min_special > 0:
                c = 0
                for i in v:
                    if not i.isalnum():
                        c = c + 1
                if c < settings.users.password_policy.min_special:
                    raise ValueError("must contain at least " + str(settings.users.password_policy.min_special) + " special characters")
        return v

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserOut(UserBase):
    """User output model."""

    key: str = Field(example="280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Key")
    active: bool = Field(example=True, title="Active")
    blocked: bool = Field(example=False, title="Blocked")
    verified: bool = Field(example=False, title="Verified")
    need_password_change: bool = Field(example=False, title="Need Password Change")
    password_attempts_count: int = Field(example=0, title="Password Strickes")
    password_setiing_date: datetime = Field(example="2021-01-01 00:00:00", title="Password Setting Date")

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserDB(UserBase):
    """User database model."""

    key: str = Field(example="280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Key")
    salt: str = Field(example="12345678", title="Salt")
    active: bool = Field(example=True, title="Active")
    blocked: bool = Field(example=False, title="Blocked")
    verified: bool = Field(example=False, title="Verified")
    need_password_change: bool = Field(example=False, title="Need Password Change")
    password_attempts_count: int = Field(example=0, title="Password Strickes")
    password_hash: str = Field(example="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Password Hash")
    password_setiing_date: datetime = Field(example="2021-01-01 00:00:00", title="Password Setting Date")

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
