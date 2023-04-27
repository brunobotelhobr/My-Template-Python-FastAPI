"""Global API configuration."""
from pydantic import BaseModel, Field  # type: ignore

from api.users.config import UserConfig


class Config(BaseModel):
    """API Configuration model."""

    users: UserConfig = Field(title="Users configuration", description="Users configuration.", default=UserConfig())

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


configuration = Config()
