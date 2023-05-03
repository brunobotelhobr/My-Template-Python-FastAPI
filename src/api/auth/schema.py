"""Auth Model."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    """Auth Request Model."""

    email: EmailStr = Field(alias="email", example="john.doe@email.com")
    password: str = Field(alias="password", example="P@ssw0rd")


class Token(BaseModel):
    """JWT Token Model."""

    access_token: str
    token_type: str


class RevokedToken(BaseModel):
    """JWT Token Revoked Model."""

    token: str
    expiration: datetime

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
