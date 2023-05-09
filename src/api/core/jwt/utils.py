"""JWT Utils."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.core.database import session
from api.core.jwt.model import AuthRequest, JWTFactory, Token
from api.core.settings.utils import running_settings
from api.core.utils import hash_handler
from api.users.model import UserBase, UserDB
from api.users.orm import UserORM

jwt_factory = JWTFactory()
barear = OAuth2PasswordBearer(tokenUrl="/auth/login-form")


def validete(username: str) -> UserDB:
    """Validate a user status."""
    # Get user from database
    with session() as database_session:
        if running_settings.users.allow_login_with_email:
            user = database_session.query(UserORM).filter(UserORM.email == username).first()
        if user is None and running_settings.users.allow_login_with_username:
            user = database_session.query(UserORM).filter(UserORM.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
            )
        user = UserDB.from_orm(user)  # type: ignore
        # MyPy: Incompatible types in assignment (expression has type "UserDB", variable has type "Optional[UserORM]"
        # Validate if user is blocked
        if user.blocked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
            )
        # Validate if user is active
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
            )
        # Validate if user is verified
        if not user.verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
            )
        return user


def authenticate(credentials: AuthRequest) -> Token:
    """Login a user."""
    user: UserDB = validete(username=credentials.username)
    # Validate password
    if hash_handler.verify_hash(password=credentials.password, hash=user.password_hash) is False:
        # Update password attempts count.
        user.password_strikes += 1
        if running_settings.users.block_user_on_password_strickes > 0:
            if user.password_strikes >= (running_settings.users.password_strikes - 1):
                user.blocked = True
        with session() as database_session:
            user_db = database_session.query(UserORM).filter(UserORM.email == user.email).first()
            for key, value in user.dict().items():
                setattr(user_db, key, value)
            database_session.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
            )
    # Reset password attempts count.
    user.password_strikes = 0  # type: ignore
    # MyPy: Incompatible types in assignment.
    with session() as database_session:
        user_db = database_session.query(UserORM).filter(UserORM.email == user.email).first()
        for key, value in user.dict().items():
            setattr(user_db, key, value)
    database_session.commit()
    token = jwt_factory.create(email=user.email)
    return Token(access_token=token)


def identify(token: Token) -> UserBase:
    """Validate Token, and return a UserBase object."""
    # Validate and get subject from token
    subject = jwt_factory.verify(token.access_token)
    user = validete(username=subject)
    # Validate user
    return UserBase(**user.dict())


def renew(token: Token) -> Token:
    """Renew a token."""
    # Validate and get subject from token
    if jwt_factory.verify(token.access_token) is not None:
        new_token = Token(access_token=jwt_factory.renew(token=token.access_token))
        jwt_factory.revoke(token.access_token)
        return new_token
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: Wrong credetials or user is not active, not verified or is blocked.",
    )


def revoke(token: Token) -> bool:
    """Revoke a token."""
    jwt_factory.revoke(token.access_token)
    return True


def get_current_user(token: Annotated[str, Depends(barear)]) -> UserBase:
    """Get current user."""
    return identify(token=Token(access_token=token))
