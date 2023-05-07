"""User Settings."""
from pydantic import BaseModel, Field, root_validator

from api.core.schema import Singleton


class PasswordPolicy(BaseModel):
    """Password policy model."""

    active: bool = Field(
        title="Activate password policy",
        description="If disabled, no restrictions to passwords will be applied.",
        default=True,
    )
    min_length: int = Field(
        title="Minimum password length",
        description="Minimum number of characters in a password.",
        default=8,
    )
    max_length: int = Field(
        title="Maximum password length",
        description="Maximum number of characters in a password.",
        default=64,
    )
    min_upper: int = Field(
        title="Minimum number of upper case characters",
        description="Minimum number of upper case characters in a password.",
        default=1,
    )
    min_lower: int = Field(
        title="Minimum number of lower case characters",
        description="Minimum number of lower case characters in a password.",
        default=1,
    )
    min_digits: int = Field(
        title="Minimum number of digits",
        description="Minimum number of digits in a password.",
        default=1,
    )
    min_special: int = Field(
        title="Minimum number of special characters",
        description="Minimum number of special characters in a password.",
        default=1,
    )

    @root_validator
    def password_policy_validator(cls, properties):
        """Validate password policy."""
        if properties["min_upper"] < 0:
            raise ValueError("min_upper must be greater than or equal to 0")
        if properties["min_lower"] < 0:
            raise ValueError("min_lower must be greater than or equal to 0")
        if properties["min_digits"] < 0:
            raise ValueError("min_digits must be greater than or equal to 0")
        if properties["min_special"] < 0:
            raise ValueError("min_special must be greater than or equal to 0")
        if properties["min_length"] < 0:
            raise ValueError("min_length must be greater than or equal to 0")
        if properties["max_length"] < 0:
            raise ValueError("max_length must be greater than or equal to 0")
        if properties["min_length"] > properties["max_length"]:
            raise ValueError("min_length must be less than or equal to max_length")
        if (
            properties["min_upper"]
            + properties["min_lower"]
            + properties["min_digits"]
            + properties["min_special"]
        ) > properties["min_length"]:
            raise ValueError(
                "min_length must be more or equal to the sum of min_upper, min_lower, min_digits and min_special"
            )
        if properties["max_length"] > 128:
            raise ValueError("max_length must be less than or equal to 128")
        return properties

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class RunningPasswordPolicy(PasswordPolicy, Singleton):
    """Singleton password policy model."""


class UserSettings(BaseModel):
    """User configuration model."""

    allow_login_with_email: bool = Field(
        title="Allow login with email",
        description="If enabled, users can login with their email and password.",
        default=True,
    )

    allow_login_with_username: bool = Field(
        title="Allow login with username",
        description="If enabled, users can login with their username and password.",
        default=True,
    )

    allow_delete: bool = Field(
        title="Allow users to be deleted, ",
        description="If not enables users can be only deactivated.",
        default=True,
    )
    allow_password_reset: bool = Field(
        title="Allow password reset to the actual password",
        description="If enabled, users can reset their passwords if the new one is equal to the actual one.",
        default=True,
    )
    default_active: bool = Field(
        title="Default user active status",
        description="If disabled, users will be created as inactive.",
        default=True,
    )
    default_verified: bool = Field(
        title="Default user verified status",
        description="If disabled, users will be created as unverified.",
        default=True,
    )
    default_blocked: bool = Field(
        title="Default user blocked status",
        description="If enabled, users will be created as blocked.",
        default=False,
    )
    block_user_on_password_strickes: bool = Field(
        title="Block user on password strickes",
        description="If enabled, users will be blocked on password strickes.",
        default=True,
    )
    password_strikes: int = Field(
        title="Block the user with this numeber of fail authentications",
        description="It must be greater than or equal to 1, default is 3.",
        default=3,
    )
    password_policy: PasswordPolicy = Field(
        title="Password policy",
        description="Password policy to be applied to all users.",
        default=PasswordPolicy(),
    )

    @root_validator
    def settings_user_validator(cls, properties):
        """Validate settings user."""
        if properties["password_strikes"] < 1:
            raise ValueError("password_strikes must be greater than or equal to 1")
        if properties["password_strikes"] > 128:
            raise ValueError("password_strikes must be less than or equal to 128")
        if (
            properties["allow_login_with_email"] is False
            and properties["allow_login_with_username"] is False
        ):
            raise ValueError(
                "allow_login_with_email and allow_login_with_username can't be both False"
            )
        return properties

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class RunningUserSettings(UserSettings, Singleton):
    """Singleton User configuration model."""

    password_policy: RunningPasswordPolicy = Field(
        title="Password policy",
        description="Password policy to be applied to all users.",
        default=RunningPasswordPolicy(),
    )
