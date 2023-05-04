"""Settings schema."""
from pydantic import BaseModel, Field, root_validator

from api.auth.settings import SettingsAuth
from api.users.settings import SettingsUser


class SettingsAPI(BaseModel):
    """General API configuration."""

    # Get Parameters
    page_size_initial: int = Field(
        default=100, title="Initial page size", description="Initial number of items returned in a single page."
    )
    page_size_max: int = Field(
        default=1000, title="Maximum page size", description="Maximum number of items returned in a single page."
    )

    @root_validator
    def validate_get_max_page_size(cls, values):  # pylint: disable=E0213
        """Validate properties."""
        if values["page_size_initial"] <= 0:
            raise ValueError("page_size_initial must be greater than 0")
        if values["page_size_max"] <= 0:
            raise ValueError("page_size_max must be greater than 0")
        # if values["page_size_max"] >= values["page_size_initial"]:
        #     raise ValueError("page_size_initial must be less than or equal to page_size_max")
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
