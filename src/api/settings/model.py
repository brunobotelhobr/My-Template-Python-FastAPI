from sqlalchemy import Column, String

from api.database import Base


class SettingsORM(Base):
    """Stores the configuration on the database."""

    __tablename__ = "settings"
    name = Column(String(length=120), primary_key=True)
    data = Column(String(length=16384))
