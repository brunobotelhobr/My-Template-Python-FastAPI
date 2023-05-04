"""Myself schema."""
from pydantic import BaseModel, Field, root_validator

from api.users.schema import Password


class PasswordResetRequest(BaseModel):
    """Password reset request model."""

    password: str = Field(example="P@ssw0rd", title="Old password", description="Your actual password")
    password_new: str = Field(example="P@ssw0rdNew", title="New password", description="Your new password")
    password_confirm: str = Field(example="P@ssw0rdNew", title="Confirm password", description="Your new password")

    @root_validator
    def passwords_match(cls, values):  # pylint: disable=no-self-argument
        """Validate that the passwords match."""
        if values["password_new"] != values["password_confirm"]:
            raise ValueError("New password and confirm password do not match")
        # Validate Password Policy
        Password(password=values["password_new"])
        return values
