"""User Router."""
from fastapi import APIRouter, HTTPException, status

from api.core.dependencies import (
    Database,
    Generator,
    HashManager,
    QueryParameters,
    Settings,
)
from api.core.paginator.utils import executor
from api.users.model import PageUserOut, UserBase, UserDB, UserIn, UserOut
from api.users.orm import UserORM

router = APIRouter()


@router.get(
    "/",
    response_model=PageUserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        500: {"description": "Internal Server Error."},
    },
)
def get_users(
    query: QueryParameters,
):
    """
    Get all users.

    This method return a list of all users, paginated according to the query parameters.

    Args:
        query (QueryParameters): Query parameters.

    Returns:
        PageUserOut: Paginated list of users.
    """
    return executor(orm=UserORM, query=query, schema=UserDB)  # type: ignore[arg-type]
    # MyPy is not recognizing herance from PageBase


@router.get(
    "/{key}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        404: {"description": "Not Found: User not found."},
        500: {"description": "Internal Server Error."},
    },
)
def get_user(key: str, database: Database):
    """
    Get a user.

    This method return details of a idenfied user by the user's key.

    Args:
        key (str): User's key.

    Returns:
        UserOut: User details.
    """
    # Check if user exists.
    user_from_database = database.query(UserORM).filter(UserORM.key == key).first()
    if not user_from_database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    # Return user.
    return user_from_database


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Successful Response."},
        422: {"description": "Unprocessable Entity: Email or Username already exists."},
        500: {"description": "Internal Server Error."},
    },
)
def create_user(
    user_in: UserIn, database: Database, generator: Generator, hash_handler: HashManager
):
    """
    Post a user.

    This method create a new user.

    Args:
        user_in (UserIn): User data.

    Returns:
        UserOut: User details.
    """
    # Check if a user with the same email exists.
    user_in_db = database.query(UserORM).filter(UserORM.email == user_in.email).first()
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not processed: Email already exists.",
        )
    # Check if a user with the same username exists.
    user_in_db = (
        database.query(UserORM).filter(UserORM.username == user_in.username).first()
    )
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not processed: Username already exists.",
        )
    # Generate calculated fields.
    key = generator.uuid()
    password_hash = hash_handler.generate_hash(user_in.password)
    # Validate Model
    new_user = UserDB(**user_in.dict(), password_hash=password_hash, key=key)
    # Convert to ORM and save.
    database.add(UserORM(**new_user.dict()))
    database.commit()
    return new_user


@router.patch(
    "/{key}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        404: {"description": "Not Found: User not found."},
        500: {"description": "Internal Server Error."},
    },
)
def update_user(user_in: UserBase, key: str, database: Database):
    """
    Update a user.

    This method update a user.

    Args:
        user_in (UserBase): User data.

    Returns:
        UserOut: User details.
    """
    # Check if user exists.
    user_from_database = database.query(UserORM).filter(UserORM.key == key).first()
    if user_from_database is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    # Update user.
    for item, value in user_in.dict(exclude_unset=True).items():
        setattr(user_from_database, item, value)
    database.commit()
    return user_from_database


@router.delete(
    "/{key}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        404: {"description": "Not Found: User not found."},
        422: {"description": "Unprocessable Entity: User deletion is not allowed."},
        500: {"description": "Internal Server Error."},
    },
)
def delete_user(key: str, database: Database, settings: Settings):
    """
    Delete a user.

    This method delete a user.
    If the user deletion is not allowed on application settings, a 422 status code is returned.

    Args:
        key (str): User's key.

    Returns:
        UserOut: User details.
    """
    # Check if user deletion is allowed.
    if settings.users.allow_delete is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not processed: User deletion is not allowed.",
        )
    # Check if user exists.
    user_from_database = database.query(UserORM).filter(UserORM.key == key).first()
    if user_from_database is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    # Delete user.
    database.delete(user_from_database)
    database.commit()
    return user_from_database
