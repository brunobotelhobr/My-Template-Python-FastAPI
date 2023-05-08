"""Settings schema."""
import json

from pydantic import BaseModel, Field

from api.core.database import session
from api.core.environment import environment
from api.core.schema import Singleton
from api.core.settings.model import SettingsORM
from api.users.settings import RunningUserSettings, UserSettings


class APISettings(BaseModel):
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


class RunningAPISettings(APISettings, Singleton):
    """Teste."""


class Settings(BaseModel):
    """Application configuration model."""

    api: APISettings = APISettings()
    #    auth: AuthSettings = AuthSettings()
    users: UserSettings = UserSettings()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class RunningSettings(Settings, Singleton):
    """Application configuration model."""

    api: RunningAPISettings = RunningAPISettings()
    #    auth: RunningAuthSettings = RunningAuthSettings()
    users: RunningUserSettings = RunningUserSettings()

    def save(self) -> bool:
        """Save the configuration to the database."""
        with session() as database_session:
            # Query the database for the settings
            settings_from_database = (
                database_session.query(SettingsORM)
                .filter(SettingsORM.name == "global")
                .first()
            )
            # If the settings exist, update them
            if not settings_from_database:
                database_session.add(SettingsORM(name="global", data=str(self.json())))
                database_session.commit()
            else:
                settings_from_database.data = str(self.json())  # type: ignore
                database_session.commit()

        return True

    def load(self) -> bool:
        """Load the configuration from the database."""
        with session() as database_session:
            if environment.database_lazzy_loader:
                return True
            settings_from_database = (
                database_session.query(SettingsORM)
                .filter(SettingsORM.name == "global")
                .first()
            )
            if not settings_from_database:
                return True
            loaded = json.loads(str(settings_from_database.data))
            for key, value in loaded.items():
                if hasattr(self, key):
                    orm_model = self.__fields__[key].type_
                    if issubclass(orm_model, BaseModel):
                        setattr(self, key, orm_model(**value))
                    else:
                        setattr(self, key, value)
            return True

    def reset(self) -> bool:
        """Reset the configuration from the database."""
        with session() as database_session:
            # Query the database for the settings
            settings_from_database = (
                database_session.query(SettingsORM)
                .filter(SettingsORM.name == "global")
                .first()
            )
            # If the settings exist, update them
            new_data = str(Settings().json())
            if not settings_from_database:
                database_session.add(SettingsORM(name="global", data=new_data))
                database_session.commit()
            else:
                settings_from_database.data = new_data  # type: ignore
                database_session.commit()
            self.load()
        return True

    # def reset(self) -> bool:
    #     """Reset the configuration to the default values."""
    #     ...
