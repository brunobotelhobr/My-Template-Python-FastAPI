"""User router."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.core.database import get_database_session  # type: ignore
from api.core.utils import generator, hash_handler
from api.settings.utils import global_settings
from api.users.model import UserORM
from api.users.schema import UserBase, UserDB, UserIn, UserOut

router = APIRouter()

limit_max = global_settings.api.page_size_max
limit_init = global_settings.api.page_size_initial


@router.get("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, database: Session = Depends(get_database_session)):
    """Get a user."""
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    return UserOut(**u.__dict__)


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = limit_init, database: Session = Depends(get_database_session)):
    """Get a list of users."""
    if limit > limit_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: Limit must be less than {limit_max}."
        )
    return database.query(UserORM).offset(skip).limit(limit).all()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, database: Session = Depends(get_database_session)):
    """Create a new user."""
    # Check if a user with the same email exists.
    user_in_db = database.query(UserORM).filter(UserORM.email == user_in.email).first()
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Not processed: Email already exists."
        )
    # Generate calculated fields.
    key = generator.uuid()
    password_hash = hash_handler.generate_hash(password=user_in.password)
    # Validate Model
    new_user = UserDB(**user_in.dict(), password_hash=password_hash, key=key)  # type: ignore
    # Convert to ORM and save.
    database.add(UserORM(**new_user.dict()))
    database.commit()
    return UserOut(**new_user.__dict__)


@router.patch("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user_in: UserBase, key: str, database: Session = Depends(get_database_session)):
    """Update a user."""
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    for k, v in user_in.dict(exclude_unset=True).items():
        setattr(u, k, v)
    return UserOut(**u.__dict__)


@router.delete("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Session = Depends(get_database_session)):
    """Delete a user."""
    if global_settings.users.allow_delete is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Not processed: User deletion is not allowed."
        )
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    database.delete(u)
    database.commit()
    return UserOut(**u.__dict__)
