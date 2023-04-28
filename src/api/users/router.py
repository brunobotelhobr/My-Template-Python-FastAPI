"""User router."""
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import Base, engine, session
from api.settings import settings
from api.users.model import UserORM
from api.users.schema import UserDB, UserIn, UserOut
from api.utils import generator

router = APIRouter()

# Create database tables.
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """Dependency to get a database session."""
    db = session()
    try:
        yield db
    finally:
        db.close()


@router.get("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, db: Session = Depends(get_db)):
    """Get a User"""
    try:
        return db.query(UserORM).filter(UserORM.key == key).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = settings.api.get_default_page_size, db: Session = Depends(get_db)):
    """Get a List of Users"""
    return db.query(UserORM).offset(skip).limit(limit).all()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if a user with the same email exists.
    recod = db.query(UserORM).filter(UserORM.email == user_in.email).first()
    if recod is not None:
        raise HTTPException(status_code=404, detail="Email already exists in the system")

    # Generate calculated fields.
    key = generator.uuid()
    salt = generator.uuid()
    hash = generator.hasher(password=user_in.password, salt=salt)
    # Validate Model
    user_db = UserDB(**user_in.dict(), salt=salt, password_hash=hash, key=key)
    # Convert to ORM and save.
    user_db = UserORM(**user_db.dict())
    db.add(user_db)
    db.commit()
    return user_db


# @router.get("/{key}}", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
# def get_user(key: str, database: Session = Depends(get_db)):
#     """Get a user."""
#     user = crud.user_get_by(database=database, attribute="key", value=key)
#     if user is not None:
#         return user
#     raise HTTPException(status_code=404, detail="Item not found")


# @router.delete("/{key}", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
# def delete_user(key: str, database: Session = Depends(get_db)):
#     """Delete a user."""
#     if configuration.users.allow_delete is False:
#         raise HTTPException(
#             status_code=404, detail="Delete is not allowed in this environment")
#     if crud.user_get_by(database=database, attribute="key", value=key) is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return crud.user_delete(database=database, key=key)
