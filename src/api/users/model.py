"""User database model."""
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from api.core.database import BaseModelORM


class UserORM(BaseModelORM):
    """User database model."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    key = Column(String(60), index=True, primary_key=True)
    name = Column(String(256), index=True, nullable=True)
    email = Column(String(256), index=True, unique=True)
    active = Column(Boolean)
    blocked = Column(Boolean)
    verified = Column(Boolean, default=False)
    password_hash = Column(String(128), nullable=True)
    password_strikes = Column(Integer, default=0)
    password_birthday = Column(DateTime(timezone=True))
