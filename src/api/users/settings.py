"""User configuration model."""
from pydantic import BaseModel, Field


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

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserConfig(BaseModel):
    """User configuration model."""

    allow_delete: bool = Field(title="Allow users to be deleted, ", description="If not enables users can be on deactivated.", default=True)
    password_policy: PasswordPolicy = Field(title="Password policy", description="Password policy to be applied to all users.", default=PasswordPolicy())
    default_active: bool = Field(title="Default user active status", description="If disabled, users will be created as inactive.", default=True)
    default_verified: bool = Field(
        title="Default user verified status",
        description="If disabled, users will be created as unverified.",
        default=False,
    )
    default_blocked: bool = Field(title="Default user blocked status", description="If enabled, users will be created as blocked.", default=False)
    default_needs_password_reset: bool = Field(
        title="Default user needs password reset status",
        description="If enabled, users will be created with a password reset flag.",
        default=False,
    )

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
