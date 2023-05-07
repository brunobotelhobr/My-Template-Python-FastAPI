"""General API database utilities."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# Create the base model
BaseModelORM = declarative_base()


def reset_database() -> bool:
    """Reset the database."""
    BaseModelORM.metadata.drop_all(bind=engine)
    BaseModelORM.metadata.create_all(bind=engine)
    return True


def shutdown_database() -> bool:
    """Shutdown the database."""
    engine.dispose()
    return True


def get_database_session():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()
