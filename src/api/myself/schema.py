"""Myself schema."""
from pydantic import BaseModel, Field, root_validator

from api.users.schema import Password


class PasswordResetRequest(BaseModel):
    """Password reset request model."""

    old: str = Field(example="Pa@ssw0rdOld", title="Old password", description="Your actual password")
    new: Password
    confirm: Password

    @root_validator
    def passwords_match(cls, values):  # pylint: disable=no-self-argument
        """Validate that the passwords match."""
        if values["new"] != values["confirm"]:
            raise ValueError("New password and confirm password do not match")
        return values
