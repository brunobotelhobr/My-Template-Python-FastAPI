from pydantic import BaseModel, root_validator

from api.auth.settings import SettingsAuth
from api.users.settings import SettingsUser


class SettingsAPI(BaseModel):
    """General API configuration."""

    # Get Parameters
    get_max_page_size: int = 1000
    get_default_page_size: int = 100

    @root_validator
    def validate_get_max_page_size(cls, values):  # pylint: disable=E0213
        """Validate get_max_page_size."""
        if values["get_max_page_size"] < 1:
            raise ValueError("get_max_page_size must be greater than 0")
        if values["get_max_page_size"] <= values["get_default_page_size"]:
            raise ValueError("get_max_page_size must be greater or equal than get_default_page_size")
        return values

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class SettingsModel(BaseModel):
    """Application configuration model."""

    name: str = "global"
    api: SettingsAPI = SettingsAPI()
    auth: SettingsAuth = SettingsAuth()
    users: SettingsUser = SettingsUser()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
