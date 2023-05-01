"""User configuration model."""
from pydantic import BaseModel, Field, root_validator


class PasswordPolicy(BaseModel):
    """Password policy model."""

    active: bool = Field(
        title="Activate password policy",
        description="If disabled, no restrictions to passwords will be applied.",
        default=True,
    )
    min_length: int = Field(title="Minimum password length", description="Minimum number of characters in a password.", default=8)
    max_length: int = Field(title="Maximum password length", description="Maximum number of characters in a password.", default=64)
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
    min_digits: int = Field(title="Minimum number of digits", description="Minimum number of digits in a password.", default=1)
    min_special: int = Field(
        title="Minimum number of special characters",
        description="Minimum number of special characters in a password.",
        default=1,
    )

    @root_validator
    def password_policy_validator(cls, v):  # pylint: disable=E0213
        """Validate password policy."""
        if v["min_upper"] < 0:
            raise ValueError("min_upper must be greater than or equal to 0")
        if v["min_lower"] < 0:
            raise ValueError("min_lower must be greater than or equal to 0")
        if v["min_digits"] < 0:
            raise ValueError("min_digits must be greater than or equal to 0")
        if v["min_special"] < 0:
            raise ValueError("min_special must be greater than or equal to 0")
        if v["min_length"] < 0:
            raise ValueError("min_length must be greater than or equal to 0")
        if v["max_length"] < 0:
            raise ValueError("max_length must be greater than or equal to 0")
        if v["min_length"] > v["max_length"]:
            raise ValueError("min_length must be less than or equal to max_length")
        if v["min_upper"] + v["min_lower"] + v["min_digits"] + v["min_special"] > v["min_length"]:
            raise ValueError("min_length must be greater than or equal to the sum of min_upper, min_lower, min_digits and min_special")
        if v["max_length"] > 128:
            raise ValueError("max_length must be less than or equal to 128")
        return v

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class SettingsUser(BaseModel):
    """User configuration model."""

    allow_delete: bool = Field(title="Allow users to be deleted, ", description="If not enables users can be on deactivated.", default=True)
    default_active: bool = Field(title="Default user active status", description="If disabled, users will be created as inactive.", default=True)
    default_verified: bool = Field(
        title="Default user verified status",
        description="If disabled, users will be created as unverified.",
        default=True,
    )
    default_blocked: bool = Field(title="Default user blocked status", description="If enabled, users will be created as blocked.", default=False)
    default_needs_password_change: bool = Field(
        title="Default user needs password reset status",
        description="If enabled, users will be created with a password reset flag.",
        default=False,
    )
    block_user_on_password_strickes: bool = Field(
        title="Block user on password strickes", description="If enabled, users will be blocked on password strickes.", default=True
    )
    strickes: int = Field(title="Block the user with this numeber of fail authentications", description="Default number of password strickes.", default=3)
    password_policy: PasswordPolicy = Field(title="Password policy", description="Password policy to be applied to all users.", default=PasswordPolicy())

    @root_validator
    def settings_user_validator(cls, v):  # pylint: disable=E0213
        """Validate settings user."""
        if v["strickes"] < 1:
            raise ValueError("strickes must be greater than or equal to 1")
        return v

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
