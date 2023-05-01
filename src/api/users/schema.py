"""User schema."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from api.settings.router import settings
from api.utils import generator


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
        print(settings.users)
        if settings.users.password_policy.active:
            min_length = settings.users.password_policy.min_length
            max_length = settings.users.password_policy.max_length
            min_upper = settings.users.password_policy.min_upper
            min_lower = settings.users.password_policy.min_lower
            min_digits = settings.users.password_policy.min_digits
            min_special = settings.users.password_policy.min_special

            if len(v) < min_length:
                raise ValueError(f"Password must have at least {min_length} characters")

            if len(v) > max_length:
                raise ValueError(f"Password must have at most {max_length} characters")

            if min_upper > 0:
                if sum(1 for i in v if i.isupper()) < min_upper:
                    raise ValueError(f"Password must have at least {min_upper} uppercase letters")

            if min_lower > 0:
                if sum(1 for i in v if i.islower()) < min_lower:
                    raise ValueError(f"Password must have at least {min_lower} lowercase letters")

            if min_digits > 0:
                if sum(1 for i in v if i.isdigit()) < min_digits:
                    raise ValueError(f"Password must have at least {min_digits} digits")

            if min_special > 0:
                if sum(1 for i in v if not i.isalnum()) < min_special:
                    raise ValueError(f"Password must have at least {min_special} special characters")
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
    password_setting_date: datetime = Field(example="2021-01-01 00:00:00", title="Password Setting Date")

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserDB(UserBase):
    """User database model."""

    key: str = Field(default=generator.uuid(), example="280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Key")
    salt: str = Field(default=generator.salt(), example="12345678", title="Salt")
    active: bool = Field(default=settings.users.default_active, example=True, title="Active")
    blocked: bool = Field(default=settings.users.default_blocked, example=False, title="Blocked")
    verified: bool = Field(default=settings.users.default_verified, example=False, title="Verified")
    need_password_change: bool = Field(default=settings.users.default_needs_password_change, example=False, title="Need Password Change")
    password_attempts_count: int = Field(default=0, example=0, title="Password Strickes")
    password_hash: str = Field(example="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Password Hash")
    password_setting_date: datetime = Field(default=generator.now(), example="2021-01-01 00:00:00", title="Password Setting Date")

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
