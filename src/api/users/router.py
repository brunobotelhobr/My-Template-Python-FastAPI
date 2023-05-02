"""User router."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import session
from api.settings.router import settings
from api.users.model import UserORM
from api.users.schema import UserBase, UserDB, UserIn, UserOut
from api.utils import generator

router = APIRouter()


# Dependency
def get_db():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()


@router.get("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, database: Session = Depends(get_db)):
    """Get a user."""
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if not u:
        raise HTTPException(status_code=404, detail="Not found.")
    return u


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = settings.api.get_default_page_size, database: Session = Depends(get_db)):
    """Get a list of users."""
    return database.query(UserORM).offset(skip).limit(limit).all()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, database: Session = Depends(get_db)):
    """Create a new user."""
    # Check if a user with the same email exists.
    u = database.query(UserORM).filter(UserORM.email == user_in.email).first()
    if u is not None:
        raise HTTPException(status_code=404, detail="Not processed: Email already exists.")
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
        raise HTTPException(status_code=404, detail="Not found.")
    for k, v in user_in.dict(exclude_unset=True).items():
        setattr(u, k, v)
    return u


@router.delete("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Session = Depends(get_db)):
    """Delete a user."""
    if settings.users.allow_delete is False:
        raise HTTPException(status_code=404, detail="Not processed: User deletion is not allowed.")
    u = database.query(UserORM).filter(UserORM.key == key).first()
    if u is None:
        raise HTTPException(status_code=404, detail="Not found.")
    database.delete(u)
    database.commit()
    return u
