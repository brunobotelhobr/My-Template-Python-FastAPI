"""JWT Utils."""
from fastapi import HTTPException, status

from api.core.database import session
from api.core.jwt.model import AuthRequest, JWTFactory, Token
from api.core.settings.utils import running_settings
from api.core.utils import hash_handler
from api.users.model import UserBase, UserDB
from api.users.orm import UserORM

jwt_factory = JWTFactory()


def validate(email: str) -> UserDB:
    """
    Validate a user status.

    Args:
        email (str): User email.

    Raises:
        HTTPException: If user is not found.

    Returns:
        UserBase: UserBase object.
    """
    # Get user from database
    with session() as database_session:
        user_from_database = (
            database_session.query(UserORM).filter(UserORM.email == email).first()
        )
        if not user_from_database:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Bad token.",
            )
        user_from_database = UserDB.from_orm(user_from_database)  # type: ignore
        # MyPy: Incompatible types in assignment (expression has type "UserDB", variable has type "Optional[UserORM]"
        # Validate if user is blocked
        if user_from_database.blocked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: User is blocked.",
            )
        # Validate if user is active
        if not user_from_database.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: User is not active.",
            )
        # Validate if user is verified
        if not user_from_database.verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: User is not verified.",
            )
        return user_from_database


def authenticate(credentials: AuthRequest) -> Token:
    """
    Login a user.

    Args:
        credentials (AuthRequest): AuthRequest object.

    Raises:
        HTTPException: If user is not found.

    Returns:
        UserBase: UserBase object.
    """
    # User Exists?
    user_from_database = None
    with session() as database_session:
        if running_settings.users.allow_login_with_email:
            user_from_database = (
                database_session.query(UserORM)
                .filter(UserORM.email == credentials.username)
                .first()
            )
        if (
            user_from_database is None
            and running_settings.users.allow_login_with_username
        ):
            user_from_database = (
                database_session.query(UserORM)
                .filter(UserORM.username == credentials.username)
                .first()
            )
        if user_from_database is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Bad credentials.",
            )
        # Validate user
        user_db = validate(email=user_from_database.email)  # type: ignore
        # MyPy: Incompatible types in assignment.
        # Validate password
        if (
            hash_handler.verify_hash(
                password=credentials.password, hash=user_db.password_hash
            )
            is False
        ):
            # Update password attempts count.
            user_from_database.password_strikes += 1  # type: ignore
            # MyPy: Incompatible types in assignment.
            if running_settings.users.block_user_on_password_strickes > 0:
                if user_db.password_strikes >= (
                    running_settings.users.password_strikes
                    - 1  # type: ignore
                    # MyPy: Incompatible types in assignment.
                ):
                    user_from_database.blocked = True  # type: ignore
                    # MyPy: Incompatible types in assignment.
            database_session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: Bad credentials.",
            )
        # Reset password attempts count.
        user_from_database.password_strikes = 0  # type: ignore
        # MyPy: Incompatible types in assignment.
        database_session.commit()
        return jwt_factory.create(email=user_db.email)


def identify(token: str) -> UserBase:
    """
    Validate Token, and return a UserBase object.

    Args:
        token (str): JWT Token.

    Raises:
        HTTPException: If user is not found.

    Returns:
        UserBase: UserBase object.
    """
    # Validate and get subject from token
    subject = jwt_factory.verify(token)
    # Validate user
    user_out = validate(email=subject)
    return UserBase(**user_out.dict())
