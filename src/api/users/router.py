"""User router."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import Base, engine, session
from api.settings import settings
from api.users.model import UserORM
from api.users.schema import UserBase, UserDB, UserIn, UserOut
from api.utils import generator

router = APIRouter()

# Create database tables.
Base.metadata.create_all(bind=engine)


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
    user = database.query(UserORM).filter(UserORM.key == key).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = settings.api.get_default_page_size, database: Session = Depends(get_db)):
    """Get a list of users."""
    return database.query(UserORM).offset(skip).limit(limit).all()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, database: Session = Depends(get_db)):
    """Create a new user."""
    # Check if a user with the same email exists.
    user_orm = database.query(UserORM).filter(UserORM.email == user_in.email).first()
    if user_orm is not None:
        raise HTTPException(status_code=404, detail="Email already exists in the system")
    # Generate calculated fields.
    key = generator.uuid()
    salt = generator.uuid()
    password_hash = generator.hasher(password=user_in.password, salt=salt)
    # Validate Model
    user_db = UserDB(**user_in.dict(), salt=salt, password_hash=password_hash, key=key)
    # Convert to ORM and save.
    user_db = UserORM(**user_db.dict(exclude_unset=True))  # type: ignore
    database.add(user_db)
    database.commit()
    return user_db


@router.delete("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Session = Depends(get_db)):
    """Delete a user."""
    if settings.users.allow_delete is False:
        raise HTTPException(status_code=404, detail="Delete is not allowed.")
    user = get_user(key=key)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    database.delete(user)
    database.commit()
    return user


@router.patch("/{key}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user: UserBase, key: str, database: Session = Depends(get_db)):
    """Update a user."""
    user = get_user(key=key)
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(user).items():
        if var in vars(user):
            setattr(user, var, value)
    database.commit()
    return user
