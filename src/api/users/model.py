"""User database model."""
from sqlalchemy import Boolean, Column, Integer, String

from api.database import Base


class UserORM(Base):
    """User database model."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    key = Column(String(60), index=True, primary_key=True)
    name = Column(String(256), index=True, nullable=True)
    email = Column(String(256), index=True, unique=True)
    salt = Column(String(8))
    password_hash = Column(String(128), nullable=True)
    active = Column(Boolean, default=True)
    blocked = Column(Boolean, default=False)
    password_change = Column(Boolean, default=False)
    password_strickes = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
