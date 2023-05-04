"""Userauth model."""
from sqlalchemy import Column, DateTime, String

from api.core.database import BaseModelORM


class RevokedTokenORM(BaseModelORM):
    """JWT Token Revoked Model."""

    __tablename__ = "revokedtokens"
    __table_args__ = {"extend_existing": True}

    token = Column(String(60), index=True, primary_key=True)
    expiration = Column(DateTime(timezone=True))
