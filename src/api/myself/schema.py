from pydantic import BaseModel, Field, root_validator


class PasswordResetRequest(BaseModel):
    """Password reset request model."""

    old: str = Field(example="Pa@ssw0rd", title="Old password", description="Your actual password")
    new: str = Field(example="Pa@ssw0rdNew", title="New password", description="Your new password")
    confirm: str = Field(example="Pa@ssw0rdNew", title="Confirm password", description="Your new password again")

    @root_validator
    def passwords_match(cls, values):  # pylint: disable=no-self-argument,no-self-use
        """Validate that the passwords match."""
        if values["new"] != values["confirm"]:
            raise ValueError("Passwords do not match.")
        return values
