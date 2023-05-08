"""Auth Model."""
from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """Auth Request Model."""

    username: str = Field(
        title="Username or Email",
        description="Username or Email, depending on the configuration.",
        example="john.doe@email.com",
    )
    password: str = Field(title="Password", description="Password.", example="P@ssw0rd")
