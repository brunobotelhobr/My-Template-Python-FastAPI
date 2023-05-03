"""Auth Model."""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import get_db
from api.settings.router import settings
from api.users.model import UserORM
from api.users.schema import UserOut

bad_tokens = []


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
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.") from e
        # Is it expired?
        if datetime.utcfromtimestamp(data["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Token expired.")
        # Is it issued in the future?
        if datetime.utcfromtimestamp(data["iat"]) > datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        # Is it assigned to a user?
        if data["sub"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        # Is ir revoked?
        if settings.auth.jwt_bad_store == "memory":
            if token in bad_tokens:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        else:
            raise NotImplementedError
        return data["sub"]

    def revoke(self, token: str):
        """Revoke JWT."""
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            print("token", token)
        if settings.auth.jwt_bad_store == "memory":
            bad_tokens.append(token)

        else:
            raise NotImplementedError
        print("bad_tokens", bad_tokens)

    def __new__(cls):
        """Create a singleton."""
        if JWTFactory.__instance is None:
            JWTFactory.__instance = object.__new__(cls)
        return JWTFactory.__instance


jwt_factory = JWTFactory()


def authenticate(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")), database: Session = Depends(get_db)) -> UserOut:
    """Authenticate user."""
    email = jwt_factory.verify(token)
    q = database.query(UserORM).filter(UserORM.email == email).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    u = UserOut(**q.__dict__)  # type: ignore
    if u.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: User is blocked.")
    return u
