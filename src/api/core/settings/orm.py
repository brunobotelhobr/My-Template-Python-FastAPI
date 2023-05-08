"""Settings ORM."""
from sqlalchemy import Column, String

from api.core.database import BaseModelORM


class SettingsORM(BaseModelORM):
    """Stores the configuration on the database."""

    __tablename__ = "settings"
    name = Column(String(length=120), primary_key=True)
    data = Column(String(length=16384))
