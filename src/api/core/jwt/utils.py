"""JWT Utils."""
from fastapi import HTTPException, status

from api.core.database import session
from api.core.jwt.model import JWTFactory
from api.users.model import UserBase, UserDB
from api.users.orm import UserORM

jwt_factory = JWTFactory()


def authenticate(token: str) -> UserBase:
    """Validate Token, and return a UserBase object."""
    # Validate and get subject from token
    subject = jwt_factory.verify(token)
    # Get user from database
    with session() as database_session:
        user_from_database = (
            database_session.query(UserORM).filter(UserORM.email == subject).first()
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
        if not user_from_database.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: User is not active.",
            )
        # Validate if user is verified
        if not user_from_database.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized: User is not verified.",
            )
        return UserBase(**user_from_database.__dict__)
