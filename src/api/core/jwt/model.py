"""JWT Schema."""
from datetime import datetime, timedelta

from fastapi import Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field

from api.core.database import session
from api.core.jwt.orm import RevokedTokenORM
from api.core.model import Singleton
from api.core.settings.utils import running_settings
from api.core.utils import environment

# To fix!
bad_tokens = []


class Token(BaseModel):
    """JWT Token Model."""

    access_token: str
    token_type: str = "bearer"


class RevokedToken(BaseModel):
    """JWT Token Revoked Model."""

    token: str
    expiration: datetime

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class JWTFactory(BaseModel, Singleton):
    """JWT Factory."""

    def parce(self, token: str):
        """Parce a JWT, and return the payload as a dict."""
        try:
            data = jwt.decode(
                token=token,
                key=environment.jwt_key,
                algorithms=running_settings.jwt.jwt_algorithm,
            )
        except JWTError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Invalid token.",
            ) from error
        return data

    def check_revoked(self, token: str) -> bool:
        """Check if token is revoked."""
        data = self.parce(token)
        revoked = RevokedToken(token=token, expiration=datetime.utcfromtimestamp(data["exp"]))
        if running_settings.jwt.jwt_revokes_store == "memory":
            if revoked in bad_tokens:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authorized: Invalid token.",
                )
        if running_settings.jwt.jwt_revokes_store == "database":
            with session() as database_session:
                if database_session.query(RevokedTokenORM).filter(RevokedTokenORM.token == token).first():
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not authorized: Invalid token.",
                    )
        if running_settings.jwt.jwt_revokes_store == "cache":
            raise NotImplementedError
        return True

    def create(self, email: str) -> str:
        """Generate JWT."""
        return str(
            jwt.encode(
                {
                    "sub": email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(minutes=running_settings.jwt.jwt_expiration_initial),
                },
                key=environment.jwt_key,
                algorithm=running_settings.jwt.jwt_algorithm,
            )
        )

    def verify(self, token: str) -> str:
        """Verify JWT."""
        # Is it a Valit Token?
        data = self.parce(token)
        # Is it expired?
        if datetime.utcfromtimestamp(float(data["exp"])) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Token expired.",
            )
        # Is it issued in the future?
        if datetime.utcfromtimestamp(float(data["iat"])) > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Invalid token.",
            )
        # Is it assigned to a user?
        if data["sub"] is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Invalid token.",
            )
        # Is ir revoked?
        self.check_revoked(token)
        return str(data["sub"])

    def revoke(self, token: str) -> bool:
        """Revoke JWT."""
        # Fix Format
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            # Is it a Valit Tokern?
        data = self.parce(token)
        # Add to bad tokens
        revoked = RevokedToken(token=token, expiration=datetime.utcfromtimestamp(data["exp"]))
        if self.check_revoked(token):
            if running_settings.jwt.jwt_revokes_store == "memory":
                bad_tokens.append(revoked)
            if running_settings.jwt.jwt_revokes_store == "database":
                with session() as database_session:
                    if database_session.query(RevokedTokenORM).filter(RevokedTokenORM.token == token).first() is None:
                        database_session.add(revoked)
                        database_session.commit()
            if running_settings.jwt.jwt_revokes_store == "cache":
                raise NotImplementedError
        return True

    def renew(self, token: str) -> str:
        """Renew JWT."""
        # Fix Format
        if token.startswith("Bearer ") or token.startswith("bearer "):
            token = token.split(" ")[1]
        data = self.parce(token)
        # Calculate new expiration
        old_expiration = datetime.utcfromtimestamp(float(data["exp"]))
        new_expiration = old_expiration + timedelta(minutes=running_settings.jwt.jwt_expiration_step)
        max_expiration = datetime.utcnow() + timedelta(minutes=running_settings.jwt.jwt_expiration_max)
        new_expiration = min(new_expiration, max_expiration)
        # Renew token
        return str(
            jwt.encode(
                {
                    "sub": data["sub"],
                    "iat": data["iat"],
                    "exp": new_expiration.utcnow(),
                },
                key=environment.jwt_key,
                algorithm=running_settings.jwt.jwt_algorithm,
            )
        )


class AuthRequest(BaseModel):
    """Auth Request Model."""

    username: str = Field(
        title="Username or Email",
        description="Username or Email, depending on the configuration.",
        example="john.doe@example.com",
    )
    password: str = Field(title="Password", description="Password.", example="P@ssw0rd")


class AuthForm(OAuth2PasswordRequestForm):
    """Auth Form Model."""

    grant_type: str = Form(default="password", regex="password")
    username: str = Form(
        title="Username or Email",
        description="Username or Email, depending on the configuration.",
        example="john.doe@example.com",
    )
    password: str = Form(title="Password", description="Password.", example="P@ssw0rd")
