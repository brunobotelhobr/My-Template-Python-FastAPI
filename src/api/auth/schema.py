"""Auth Model."""
from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    """Auth Request Model."""

    email: EmailStr = Field(alias="email", example="john.doe@email.com")
    password: str = Field(alias="password", example="P@ssw0rd")


class Token(BaseModel):
    """JWT Token Model."""

    access_token: str
    token_type: str
