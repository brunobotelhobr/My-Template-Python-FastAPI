"""General API database utilities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.core.environment import database_environment, running_environment


# Create the engine
def create_local_engine():
    """Create the database engine."""
    if database_environment.database_connection_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        return create_engine(
            database_environment.database_connection_url,
            echo=running_environment.local.is_debug,
            connect_args=connect_args,
        )
    return create_engine(
        database_environment.database_connection_url,
        echo=running_environment.local.is_debug,
    )


# Spawn the engine
engine = create_local_engine()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModelORM(DeclarativeBase):
    """BaseModelORM class for all the database models."""  # pylint: disable=too-few-public-methods

    pass  # pylint: disable=unnecessary-pass


def initialize_database() -> bool:
    """Initialize the database."""
    BaseModelORM.metadata.create_all(bind=engine)
    return True


def get_database_session():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()
