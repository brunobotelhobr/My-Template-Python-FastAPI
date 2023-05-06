"""User router."""
from fastapi import APIRouter, HTTPException, status

from api.core.dependencies import (
    Database,
    Generator,
    HashManager,
    PageUserOut,
    QueryParameters,
    Settings,
    query_executor,
)
from api.users.model import UserORM
from api.users.schema import UserBase, UserDB, UserIn, UserOut

router = APIRouter()


@router.get("/", response_model=PageUserOut, status_code=status.HTTP_200_OK)
def get_users(
    query: QueryParameters,
):
    """Get a list of users."""
    return query_executor(orm_model=UserORM, query=query, model=UserDB)


@router.get("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, database: Database):
    """Get a user."""
    # Check if user exists.
    user_from_database = database.query(UserORM).filter(UserORM.key == key).first()
    if not user_from_database:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    # Return user.
    return user_from_database


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserIn,
    database: Database,
    generator: Generator,
    hash_handler: HashManager,
):
    """Create a new user."""
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


@router.patch("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user_in: UserBase, key: str, database: Database):
    """Update a user."""
    # Check if user exists.
    user_from_database = database.query(UserORM).filter(UserORM.key == key).first()
    if user_from_database is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    # Update user.
    for item, value in user_in.dict(exclude_unset=True).items():
        setattr(user_from_database, item, value)
    database.commit()
    return user_from_database


@router.delete("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Database, settings: Settings):
    """Delete a user."""
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
