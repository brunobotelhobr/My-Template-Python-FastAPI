"""User Schema."""
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator

from api.core.paginator.schema import PageBase
from api.core.settings.schema import RunningSettings
from api.core.utils import generator


class Password(BaseModel):
    """User input model."""

    password: str = Field(
        example="P@ssw0rd",
        title="Password",
        description="User password, it comply with the password policy.",
    )

    @validator("password")
    def passwords_match(cls, value):
        """Validate password policy."""
        if RunningSettings().users.password_policy.active:
            min_length = RunningSettings().users.password_policy.min_length
            max_length = RunningSettings().users.password_policy.max_length
            min_upper = RunningSettings().users.password_policy.min_upper
            min_lower = RunningSettings().users.password_policy.min_lower
            min_digits = RunningSettings().users.password_policy.min_digits
            min_special = RunningSettings().users.password_policy.min_special

            if len(value) < min_length:
                raise ValueError(f"Password must have at least {min_length} characters")

            if len(value) > max_length:
                raise ValueError(f"Password must have at most {max_length} characters")

            if min_upper > 0:
                if sum(1 for caracter in value if caracter.isupper()) < min_upper:
                    raise ValueError(
                        f"Password must have at least {min_upper} uppercase letters"
                    )

            if min_lower > 0:
                if sum(1 for caracter in value if caracter.islower()) < min_lower:
                    raise ValueError(
                        f"Password must have at least {min_lower} lowercase letters"
                    )

            if min_digits > 0:
                if sum(1 for caracter in value if caracter.isdigit()) < min_digits:
                    raise ValueError(f"Password must have at least {min_digits} digits")

            if min_special > 0:
                if sum(1 for caracter in value if not caracter.isalnum()) < min_special:
                    raise ValueError(
                        f"Password must have at least {min_special} special characters"
                    )
        return value

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserBase(BaseModel):
    """User BaseModelORM model."""

    username: str = Field(
        example="johndoe",
        title="Username",
        description=(
            "User username, it must be unique, bigger than 5 and smaller than 64 characters"
            ", must not contain spaces."
        ),
    )
    name: str = Field(
        example="John Doe",
        title="Full name",
        description=(
            "User full name, it must contain a space character, bigger than 5 and smaller "
            "than 128 characters."
        ),
    )
    email: EmailStr = Field(
        example="john.doe@email.com",
        title="Email",
        description="It can be an email binded to another account.",
    )

    @validator("name")
    def name_must_contain_space(cls, value):
        """Validate property."""
        if " " not in value:
            raise ValueError("must contain a space")
        if len(value) < 5:
            raise ValueError("length must be greater than 5")
        if len(value) > 128:
            raise ValueError("length must be less than 128")
        return value.title()

    @validator("username")
    def username_must_contain_space(cls, value):
        """Validate property."""
        if " " in value:
            raise ValueError("must not contain a space")
        if len(value) < 5:
            raise ValueError("length must be greater than 5")
        if len(value) > 64:
            raise ValueError("length must be less than 64")
        return value.lower()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserIn(UserBase, Password):
    """User input model."""

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserOut(UserBase):
    """User output model."""

    key: str = Field(
        example="280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        title="Key",
        description="User key, it is a unique identifier.",
    )
    blocked: bool = Field(
        example=False, title="Blocked", description="User blocked status."
    )
    verified: bool = Field(
        example=False, title="Verified", description="User verified status."
    )
    password_strikes: int = Field(
        example=0, title="Password Strikes", description="User password strikes."
    )
    password_birthday: datetime = Field(
        example="2021-01-01 00:00:00",
        title="Password Setting Date",
        description="User password setting date.",
    )

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserDB(UserBase):
    """User database model."""

    key: str = Field(
        default=generator.uuid(),
        example="280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        title="Key",
        description="User key, it is a unique identifier.",
    )
    blocked: bool = Field(
        default=RunningSettings().users.default_blocked,
        example=False,
        title="Blocked",
        description="User blocked status.",
    )
    verified: bool = Field(
        default=RunningSettings().users.default_verified,
        example=False,
        title="Verified",
        description="User verified status.",
    )
    password_hash: str = Field(
        example="argon2id$v=19$m=65536,t=3,p=4$sC2MrzQvIT5v0reVS4eK5A$bLBwdKS2uMME7MF9ln06cGrEtiLK294YtQz8t44wcKw",
        title="Password Hash",
        description="User password hash, used to authenticate localy.",
    )
    password_strikes: int = Field(
        default=0,
        example=0,
        title="Password Strikes",
        description="User password strikes.",
    )
    password_birthday: datetime = Field(
        default=generator.now(),
        example="2021-01-01 00:00:00",
        title="Password Setting Date",
    )

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class PageUserOut(PageBase):
    """Page of UserOut."""

    records: List[UserOut]  # type: ignore
    # MyPy does not support recursive types yet
