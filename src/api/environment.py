"""Module to store the environment variables of the API."""
from enum import Enum

from pydantic import BaseSettings

from api.utils import generator


class Environment(str, Enum):
    """Supported environments and their properties."""

    LOCAL = "LOCAL"
    STAGING = "STAGING"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        """Return True if the environment is a debug environment."""
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        """Return True if the environment is a testing environment."""
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        """Return True if the environment is a deployed environment."""
        return self in (self.STAGING, self.PRODUCTION)


class DatabaseSettings(BaseSettings):
    """Class to store the configuration of the database, it loads the environment variables with a prefix."""

    __inscence = None

    url: str = "sqlite:///database.db"
    aut_create_models: bool = True

    class Config:  # pylint: disable=too-few-public-methods
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_DB_"
        case_sensitive = False

    def __new__(cls):
        """Create a singleton."""
        if DatabaseSettings.__inscence is None:
            DatabaseSettings.__inscence = object.__new__(cls)
        return DatabaseSettings.__inscence


class RunnigeEnviroment(BaseSettings):
    """Class to store the enviroment of the API."""

    __instance = None

    local: Environment = Environment.LOCAL
    jwt_key = generator.uuid()

    class Config:  # pylint: disable=too-few-public-methods
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_"
        case_sensitive = False

    def __new__(cls):
        """Create a singleton."""
        if RunnigeEnviroment.__instance is None:
            RunnigeEnviroment.__instance = object.__new__(cls)
        return RunnigeEnviroment.__instance


env = RunnigeEnviroment()
db = DatabaseSettings()
