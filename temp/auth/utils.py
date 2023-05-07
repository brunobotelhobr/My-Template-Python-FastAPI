"""Auth Model."""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.auth.model import RevokedTokenORM
from api.auth.schema import RevokedToken
from api.core.database import get_database_session
from api.core.dependencies import Settings
from api.users.model import UserORM
from api.users.schema import UserOut

bad_tokens = []


class JWTFactory(BaseModel):
    """JWT Factory."""

    __instance = None

    def __parce(self, token: str):
        """Parce JWT."""
        try:
            data = jwt.decode(
                token,
                key=Settings.auth.jwt_key,
                algorithms=Settings.auth.jwt_algorithm,
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Invalid token.",
            ) from e
        return data

    def __check_revoked(self, token: str) -> bool:
        """Check if token is revoked."""
        data = self.__parce(token)
        if Settings.auth.jwt_revokes_store == "memory":
            if (
                RevokedToken(
                    token=token, expiration=datetime.utcfromtimestamp(float(data["exp"]))
                )
                in bad_tokens
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authorized: Invalid token.",
                )
        if Settings.auth.jwt_revokes_store == "database":
            with get_database_session() as session:
                if (
                    session.query(RevokedTokenORM)
                    .filter(RevokedTokenORM.token == token)
                    .first()
                ):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not authorized: Invalid token.",
                    )
        if Settings.auth.jwt_revokes_store == "cache":
            raise NotImplementedError
        return True

    def create(self, email: str) -> str:
        """Generate JWT."""
        return str(
            jwt.encode(
                {
                    "sub": email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow()
                    + timedelta(minutes=Settings.auth.jwt_expiration_initial),
                },
                key=Settings.auth.jwt_key,
                algorithm=Settings.auth.jwt_algorithm,
            )
        )

    def verify(self, token: str):
        """Verify JWT."""
        # Is it a Valit Token?
        data = self.__parce(token)
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
        self.__check_revoked(token)
        return data["sub"]

    def revoke(self, token: str) -> bool:
        """Revoke JWT."""
        # Fix Format
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            # Is it a Valit Tokern?
        data = self.__parce(token)
        # Add to bad tokens
        if self.__check_revoked(token):
            if Settings.auth.jwt_revokes_store == "memory":
                bad_tokens.append(
                    RevokedToken(
                        token=token, expiration=datetime.utcfromtimestamp(data["exp"])
                    )
                )
            if Settings.auth.jwt_revokes_store == "database":
                with get_database_session() as session:
                    session.add(
                        RevokedTokenORM(
                            token=token, expiration=datetime.utcfromtimestamp(data["exp"])
                        )
                    )
                    session.commit()
                    print("salvei")
            if Settings.auth.jwt_revokes_store == "cache":
                raise NotImplementedError
        return True

    def renew(self, token: str):
        """Renew JWT."""
        # Fix Format
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        # Check if token is valid
        data = self.__parce(token)
        # Calculate new expiration
        old_expiration = datetime.utcfromtimestamp(float(data["exp"]))
        new_expiration = old_expiration + timedelta(
            minutes=Settings.auth.jwt_expiration_step
        )
        max_expiration = datetime.utcnow() + timedelta(
            minutes=Settings.auth.jwt_expiration_max
        )
        new_expiration = min(new_expiration, max_expiration)
        # Renew token
        return jwt.encode(
            {
                "sub": data["sub"],
                "iat": data["iat"],
                "exp": new_expiration.utcnow(),
            },
            key=Settings.auth.jwt_key,
            algorithm=Settings.auth.jwt_algorithm,
        )

    def __new__(cls):
        """Create a singleton."""
        if JWTFactory.__instance is None:
            JWTFactory.__instance = object.__new__(cls)
        return JWTFactory.__instance


def authenticate(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
    database: Session = Depends(get_database_session),
) -> UserOut:
    """Authenticate user."""
    email = jwt_factory.verify(token)
    q = database.query(UserORM).filter(UserORM.email == email).first()
    if not q:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized: Bad credentials.",
        )
    u = UserOut(**q.__dict__)  # type: ignore
    if u.blocked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized: User is blocked.",
        )
    return u


jwt_factory = JWTFactory()
