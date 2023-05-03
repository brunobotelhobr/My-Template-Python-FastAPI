"""Settings utilities."""
import json

from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import engine
from api.settings.model import SettingsORM
from api.settings.schema import SettingsModel


def save(settings: SettingsModel) -> bool:
    """Save the configuration to the database."""
    with Session(engine) as session:
        with Session(engine) as session:
            s = session.query(SettingsORM).filter(SettingsORM.name == settings.name).first()
            if s:
                s.name = settings.name  # type: ignore
                s.data = str(settings.json())  # type: ignore
                session.commit()
            else:
                s = SettingsORM(name=settings.name, data=str(settings.json()))
                session.add(s)
                session.commit()
            return True


def load(settings: SettingsModel) -> bool:
    """Load the configuration from the database."""
    with Session(engine) as session:
        s = session.query(SettingsORM).filter(SettingsORM.name == settings.name).first()
        if s:
            loaded = json.loads(str(s.data))
            for key, value in loaded.items():
                if hasattr(settings, key):
                    orm_model = settings.__fields__[key].type_
                    if issubclass(orm_model, BaseModel):
                        setattr(settings, key, orm_model(**value))
                    else:
                        setattr(settings, key, value)
            return True
        return False


def reset(settings: SettingsModel) -> bool:
    """Reset the configuration to the default values."""
    with Session(engine) as session:
        s = session.query(SettingsORM).filter(SettingsORM.name == settings.name).first()
        if s is None:
            return False
        session.delete(s)
        session.commit()
        return True


global_settings = SettingsModel(name="global")
