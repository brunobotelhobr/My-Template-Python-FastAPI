from pydantic import BaseModel  # type: ignore

from api.users.settings import UserConfig


class APIConfig(BaseModel):
    """General configuration model."""

    # Get Parameters
    get_max_page_size: int = 1000
    get_default_page_size: int = 100


class Config(BaseModel):
    """Application configuration model."""

    api: APIConfig = APIConfig()
    users: UserConfig = UserConfig()


settings = Config()
