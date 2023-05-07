"""Core Environment."""
from enum import Enum

from pydantic import BaseSettings

from api.core.utils import generator
from api.core.schema import Singleton


class EnvironmentBehavior(str, Enum):
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


class DatabaseEnvironment(BaseSettings, Singleton):
    """Class to store the configuration of the database, it loads the environment variables with a prefix."""

    database_connection_url: str = "sqlite:///database.db"
    aut_create_models: bool = True

    class Config:
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_DB_"
        case_sensitive = False


class RunnigeEnviroment(BaseSettings, Singleton):
    """Class to store the enviroment of the API."""

    local: EnvironmentBehavior = EnvironmentBehavior.LOCAL
    jwt_key: str = generator.uuid()

    class Config:
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_"
        case_sensitive = False


running_environment = RunnigeEnviroment()
database_environment = DatabaseEnvironment()
