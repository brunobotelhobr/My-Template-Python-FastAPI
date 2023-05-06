"""Settings schema."""
import json

from pydantic import BaseModel, Field

from api.auth.settings import SettingsAuth
from api.core.database import session
from api.settings.model import SettingsORM
from api.users.settings import UserSettings


class SettingsAPI(BaseModel):
    """General API configuration."""

    # Get Parameters
    page_size_initial: int = Field(
        default=100,
        title="Initial page size",
        description="Initial number of items returned in a single page.",
        gt=1,
    )
    page_size_max: int = Field(
        default=1000,
        title="Maximum page size",
        description="Maximum number of items returned in a single page.",
        gt=1,
    )

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class SettingsGlobal(BaseModel):
    """Application configuration model."""

    api: SettingsAPI = SettingsAPI()
    auth: SettingsAuth = SettingsAuth()
    users: UserSettings = UserSettings()

    def save(self) -> bool:
        """Save the configuration to the database."""
        with session() as database:
            # Query the database for the settings
            settings_database = (
                database.query(SettingsORM).filter(SettingsORM.name == "global").first()
            )
            # If the settings exist, update them
            if settings_database:
                settings_database.name = str("global")
                settings_database.data = str(self.json())
                database.commit()
            # Otherwise, create them
            else:
                database.add(SettingsORM(name="global", data=str(self.json())))
                database.commit()
            return True

    def load(self) -> bool:
        """Load the configuration from the database."""
        with session() as database:
            settings_database = (
                database.query(SettingsORM).filter(SettingsORM.name == "global").first()
            )
            # If the settings exist, load them
            if settings_database:
                loaded = json.loads(str(s.data))
                for key, value in loaded.items():
                    if hasattr(self, key):
                        orm_model = self.__fields__[key].type_
                        if issubclass(orm_model, BaseModel):
                            setattr(self, key, orm_model(**value))
                        else:
                            setattr(self, key, value)
                return True
            return False

    def reset(self) -> bool:
        """Reset the configuration to the default values."""
        with session() as database:
            settings_database = (
                database.query(SettingsORM).filter(SettingsORM.name == "global").first()
            )
            if settings_database is None:
                return False
            database.delete(settings_database)
            database.commit()
            return True

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
