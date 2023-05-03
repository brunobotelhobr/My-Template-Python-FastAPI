"""Auth Model."""
from datetime import datetime, timedelta
from time import process_time_ns

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.auth.schema import RevokedToken
from api.database import engine, get_db
from api.settings.utils import global_settings
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
                key=global_settings.auth.jwt_key,
                algorithms=global_settings.auth.jwt_algorithm,
            )
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.") from e
        return data

    def __check_revoked(self, token: str) -> bool:
        """Check if token is revoked."""
        data = self.__parce(token)
        if global_settings.auth.jwt_revokes_store == "memory":
            if RevokedToken(token=token, expiration=datetime.utcfromtimestamp(float(data["exp"]))) in bad_tokens:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        if global_settings.auth.jwt_revokes_store == "database":
            with Session(engine) as session:
                if session.query(RevokedToken).filter_by(token=token).first():
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        if global_settings.auth.jwt_revokes_store == "cache":
            raise NotImplementedError
        return True

    def create(self, email: str) -> str:
        """Generate JWT."""
        return str(
            jwt.encode(
                {
                    "sub": email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(minutes=global_settings.auth.jwt_expiration_initial),
                },
                key=global_settings.auth.jwt_key,
                algorithm=global_settings.auth.jwt_algorithm,
            )
        )

    def verify(self, token: str):
        """Verify JWT."""
        # Is it a Valit Tokern?
        data = self.__parce(token)
        # Is it expired?
        if datetime.utcfromtimestamp(float(data["exp"])) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Token expired.")
        # Is it issued in the future?
        if datetime.utcfromtimestamp(float(data["iat"])) > datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
        # Is it assigned to a user?
        if data["sub"] is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid token.")
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
            if global_settings.auth.jwt_revokes_store == "memory":
                bad_tokens.append(RevokedToken(token=token, expiration=datetime.utcfromtimestamp(data["exp"])))
            if global_settings.auth.jwt_revokes_store == "database":
                with Session(engine) as session:
                    session.add(RevokedToken(token=token, expiration=datetime.utcfromtimestamp(data["exp"])))
                    session.commit()
            if global_settings.auth.jwt_revokes_store == "cache":
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
        new_expiration = old_expiration + timedelta(minutes=global_settings.auth.jwt_expiration_step)
        max_expiration = datetime.utcnow() + timedelta(minutes=global_settings.auth.jwt_expiration_max)
        new_expiration = min(new_expiration, max_expiration)
        # Renew token
        return jwt.encode(
            {
                "sub": data["sub"],
                "iat": data["iat"],
                "exp": new_expiration.utcnow(),
            },
            key=global_settings.auth.jwt_key,
            algorithm=global_settings.auth.jwt_algorithm,
        )

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
