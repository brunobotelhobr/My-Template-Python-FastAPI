"""User schema."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from api.core.utils import generator
from api.settings.utils import global_settings


class Password(BaseModel):
    """User input model."""

    password: str = Field(
        example="P@ssw0rd",
        title="Password",
        description="User password, it comply with the password policy.",
    )

    @validator("password")
    def passwords_match(cls, v):
        """Validate password policy."""
        if global_settings.users.password_policy.active:
            min_length = global_settings.users.password_policy.min_length
            max_length = global_settings.users.password_policy.max_length
            min_upper = global_settings.users.password_policy.min_upper
            min_lower = global_settings.users.password_policy.min_lower
            min_digits = global_settings.users.password_policy.min_digits
            min_special = global_settings.users.password_policy.min_special

            if len(v) < min_length:
                raise ValueError(f"Password must have at least {min_length} characters")

            if len(v) > max_length:
                raise ValueError(f"Password must have at most {max_length} characters")

            if min_upper > 0:
                if sum(1 for i in v if i.isupper()) < min_upper:
                    raise ValueError(
                        f"Password must have at least {min_upper} uppercase letters"
                    )

            if min_lower > 0:
                if sum(1 for i in v if i.islower()) < min_lower:
                    raise ValueError(
                        f"Password must have at least {min_lower} lowercase letters"
                    )

            if min_digits > 0:
                if sum(1 for i in v if i.isdigit()) < min_digits:
                    raise ValueError(f"Password must have at least {min_digits} digits")

            if min_special > 0:
                if sum(1 for i in v if not i.isalnum()) < min_special:
                    raise ValueError(
                        f"Password must have at least {min_special} special characters"
                    )
        return v

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
    def name_must_contain_space(cls, v):
        """Validate property."""
        if " " not in v:
            raise ValueError("must contain a space")
        if len(v) < 5:
            raise ValueError("length must be greater than 5")
        if len(v) > 128:
            raise ValueError("length must be less than 128")
        return v.title()

    @validator("username")
    def username_must_contain_space(cls, v):
        """Validate property."""
        if " " in v:
            raise ValueError("must not contain a space")
        if len(v) < 5:
            raise ValueError("length must be greater than 5")
        if len(v) > 64:
            raise ValueError("length must be less than 64")
        return v.lower()

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
    active: bool = Field(example=True, title="Active", description="User active status.")
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
    active: bool = Field(
        default=global_settings.users.default_active,
        example=True,
        title="Active",
        description="User active status.",
    )
    blocked: bool = Field(
        default=global_settings.users.default_blocked,
        example=False,
        title="Blocked",
        description="User blocked status.",
    )
    verified: bool = Field(
        default=global_settings.users.default_verified,
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
