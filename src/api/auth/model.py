"""Auth Model"""

import datetime
import hashlib

import jose.jwt as jwt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from api.users.model import UserBase


class PasswordManager:
    """Password Validator Class"""

    # def generate_hash(self, password: str, salt: str):
    #     """Generate hash"""
    #     return hashlib.sha256(
    #         self.salt.encode() + self.password.encode()
    #     ).hexdigest()

    def validate(self):
        """Validate password"""
        return self.hash == self._generate_hash()


class JWTFactory:
    """JWT Class"""

    def generate(self, user: UserBase):
        """Generate JWT"""
        return jwt.encode(
            {
                "sub": user.email,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            key="abc123",
            algorithm="HS256",
        )

    def decode(self, token: str):
        """Decode JWT"""
        return jwt.decode(token, key="abc123", algorithms="HS256")

    def validate(self, token: str):
        """Validate JWT"""
        try:
            return jwt.decode(token, key="abc123", algorithms="HS256")
        except:
            return False

    def extend(self, token: str):
        """Extend JWT"""
        return jwt.encode(
            {
                "sub": token["sub"],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            key="abc123",
            algorithm="HS256",
        )

    def validate_and_extend(self, token: str):
        if self.validate(token):
            return self.extend(token)
        return False


class AuthRequest(BaseModel):
    """Auth Request Model"""

    email: EmailStr = Field(alias="email", example="john@example.com")
    password: SecretStr = Field(alias="password", example="P@ssw0rd")
