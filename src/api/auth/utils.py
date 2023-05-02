"""Auth Model."""
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

from api.settings.router import settings


class JWTFactory(BaseModel):
    """JWT Factory."""

    __instance = None

    def create(self, email: str):
        """Generate JWT."""
        return jwt.encode(
            {
                "sub": email,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=settings.auth.jwt_expiration),
            },
            key=settings.auth.jwt_key,
            algorithm=settings.auth.jwt_algorithm,
        )

    def verify(self, token: str):
        """Verify JWT."""
        # Is it a Valit Tokern?
        try:
            data = jwt.decode(
                token,
                key=settings.auth.jwt_key,
                algorithms=[settings.auth.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")  # type: ignore
        # Is it expired?
        if datetime.utcfromtimestamp(data["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Token expired.")
        # Is it issued in the future?
        if datetime.utcfromtimestamp(data["iat"]) > datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        # Is it assigned to a user?
        if data["sub"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        return data["sub"]

    def __new__(cls):
        """Create a singleton."""
        if JWTFactory.__instance is None:
            JWTFactory.__instance = object.__new__(cls)
        return JWTFactory.__instance


jwt_factory = JWTFactory()
