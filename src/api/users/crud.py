"""User router."""
from datetime import datetime  # pylint: disable=wrong-import-order
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.users.model import UserORM


def user_list(database: Session, skip: int = 0, limit: int = 100) -> List[UserORM]:
    """List all users."""
    return database.query(UserORM).offset(skip).limit(limit).all()


def user_save(database: Session, user: UserORM) -> UserORM:
    """Save user."""
    recod = database.query(UserORM).filter(UserORM.key == user.key).first()
    if recod is not None:
        raise HTTPException(status_code=404, detail="Item already exists")
    recod = database.query(UserORM).filter(UserORM.email == user.email).first()
    if recod is not None:
        raise HTTPException(status_code=404, detail="Email already exists in the system")
    database.add(user)
    database.commit()
    return user


def user_delete(database: Session, key: str) -> UserORM:
    """Delete user."""
    user = user_get_by(database=database, attribute="key", value=key)
    database.delete(user)
    database.commit()
    return user


def user_get_by(database: Session, attribute: str, value: str) -> UserORM | None:
    """Get a user by attribute."""
    return database.query(UserORM).filter(getattr(UserORM, attribute) == value).first()


def user_update(database: Session, user: UserORM, update_dict: dict) -> UserORM:
    """Update user."""
    recod = database.query(UserORM).filter(UserORM.key == user.key).first()
    if recod is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update record with user data
    for field, value in update_dict.items():
        setattr(user, field, value)
    user.changed_at = datetime.now()
    database.commit()
    database.refresh(user)
    return user
