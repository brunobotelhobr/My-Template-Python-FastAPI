"""User database model."""
from sqlalchemy import Boolean, Column, DateTime, String

from api.database import Base


class UserORM(Base):
    """User database model."""

    __tablename__ = "users"

    key = Column(String(64), primary_key=True, index=True)
    name = Column(String(240), index=True, nullable=True)
    email = Column(String(120), index=True, unique=True)
    hashed_password = Column(String(64), nullable=True)
    salt = Column(String(32), nullable=True)
    created_at = Column(DateTime)
    changed_at = Column(DateTime)
    is_verified = Column(Boolean)
    is_active = Column(Boolean)
    is_blocked = Column(Boolean)
    needs_password_reset = Column(Boolean)
