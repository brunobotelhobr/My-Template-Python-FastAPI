import json

from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import engine
from api.settings.model import SettingsORM
from api.users.settings import SettingsUser


class SettingsAPI(BaseModel):
    """General API configuration."""

    # Get Parameters
    get_max_page_size: int = 1000
    get_default_page_size: int = 100

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class SettingsModel(BaseModel):
    """Application configuration model."""

    name: str = "global"
    api: SettingsAPI = SettingsAPI()
    users: SettingsUser = SettingsUser()

    def save(self) -> bool:
        """Save the configuration to the database."""
        with Session(engine) as session:
            with Session(engine) as session:
                s = session.query(SettingsORM).filter(SettingsORM.name == self.name).first()
                if s:
                    s.data = str(self.json())  # type: ignore
                    session.commit()
                else:
                    s = SettingsORM(name=self.name, data=str(self.json()))
                    session.add(s)
                    session.commit()
                return True

    def load(self) -> bool:
        """Load the configuration from the database."""
        with Session(engine) as session:
            s = session.query(SettingsORM).filter(SettingsORM.name == self.name).first()
            if s:
                self.__dict__.update(json.loads(str(s.data)))
                return True
            return self.save()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
