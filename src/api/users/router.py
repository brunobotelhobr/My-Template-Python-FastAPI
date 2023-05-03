"""User router."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db  # type: ignore
from api.settings.utils import global_settings
from api.users.model import UserORM
from api.users.schema import UserBase, UserDB, UserIn, UserOut
from api.utils import generator

router = APIRouter()

limit_max = global_settings.api.page_size_max
limit_init = global_settings.api.page_size_initial


@router.get("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, database: Session = Depends(get_db)):
    """Get a user."""
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    u = UserOut(**u.__dict__)
    return u


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = limit_init, database: Session = Depends(get_db)):
    """Get a list of users."""
    if limit > limit_max:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: Limit must be less than {limit_max}.")
    return database.query(UserORM).offset(skip).limit(limit).all()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, database: Session = Depends(get_db)):
    """Create a new user."""
    # Check if a user with the same email exists.
    u = database.query(UserORM).filter(UserORM.email == user_in.email).first()
    if u is not None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Not processed: Email already exists.")
    # Generate calculated fields.
    key = generator.uuid()
    salt = generator.salt()
    password_hash = generator.hasher(password=user_in.password, salt=salt)
    # Validate Model
    u = UserDB(**user_in.dict(), salt=salt, password_hash=password_hash, key=key)  # type: ignore
    # Convert to ORM and save.
    u = UserORM(**u.dict())  # type: ignore
    database.add(u)
    database.commit()
    return u


@router.patch("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user_in: UserBase, key: str, database: Session = Depends(get_db)):
    """Update a user."""
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    for k, v in user_in.dict(exclude_unset=True).items():
        setattr(u, k, v)
    return u


@router.delete("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Session = Depends(get_db)):
    """Delete a user."""
    if global_settings.users.allow_delete is False:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Not processed: User deletion is not allowed.")
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    database.delete(u)
    database.commit()
    return u
