"""Core Environment."""
from enum import Enum

from pydantic import BaseSettings, Field

from api.core.schema import Singleton
from api.core.utils import generator


class Behavior(str, Enum):
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

    database_lazzy_loader: bool = Field(
        default=True,
        env="API_DB_LAZZY_LOADER",
        title="Database lazzy loader",
        description=(
            "If True, the database will use the lazzy loader, "
            + "building tables and then, initializing the settings,"
            + "set this to false if you are using alembic, "
            + "don't enable it in production."
        ),
    )
    database_connection_url: str = Field(
        default="sqlite:///database.db",
        env="API_DB_CONNECTION_URL",
        title="Database connection url",
        description="The connection url of the database.",
    )
    aut_create_models: bool = Field(
        default=True,
        env="API_DB_AUT_CREATE_MODELS",
        title="Aut create models",
        description="If True, the models will be created automatically.",
    )

    class Config:
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_DB_"
        case_sensitive = False


class RunnigeEnviroment(BaseSettings, Singleton):
    """Class to store the enviroment of the API."""

    behavior: Behavior = Field(
        default=Behavior.LOCAL,
        env="API_BEHAVIOR",
        title="API behavior",
        description="The behavior of the API, it can be: LOCAL, STAGING, TESTING or PRODUCTION.",
    )
    jwt_key: str = Field(
        default=generator.uuid(),
        env="API_JWT_KEY",
        title="JWT key",
        description="The key used to encrypt the JWT, if not provided, a random key will be generated.",
    )

    class Config:
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_"
        case_sensitive = False


class Environment(DatabaseEnvironment, RunnigeEnviroment, Singleton):
    """Class to store the configuration of the API."""

    class Config:
        """Load environment variables with a prefix and make them case sensitive."""

        env_prefix = "API_"
        case_sensitive = False


# Environment settings
environment = Environment()
