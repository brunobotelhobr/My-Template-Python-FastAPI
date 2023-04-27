"""User database model."""
from sqlalchemy import Column, String

from api.database import Base


class UserORM(Base):
    """User database model."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    key = Column(String, index=True, primary_key=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, unique=True)
    salt = Column(String)
    password_hash = Column(String, nullable=True)
