"""Core Database."""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.core.environment import environment


# Create the engine
def _create_local_engine():
    """Create the database engine."""
    # Adjust the engine for sqlite
    if environment.database_connection_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        return create_engine(
            environment.database_connection_url,
            # Echo commandt to stdout, if environment is debug
            echo=environment.behavior.is_debug,
            connect_args=connect_args,
        )
    # Standard engine
    return create_engine(
        environment.database_connection_url,
        # Echo commandt to stdout, if environment is debug
        echo=environment.behavior.is_debug,
    )


# Spawn the engine
engine = _create_local_engine()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base model, if environment.aut_create_models is True
if environment.aut_create_models:
    BaseModelORM = declarative_base()


def reset() -> bool:
    """Reset the database."""
    BaseModelORM.metadata.drop_all(bind=engine)
    BaseModelORM.metadata.create_all(bind=engine)
    return True


def shutdown() -> bool:
    """Shutdown the database."""
    engine.dispose()
    return True


def initialize() -> bool:
    """Initialize the database."""
    if environment.aut_create_models:
        BaseModelORM.metadata.create_all(bind=engine)
        return True
    return False


def test() -> bool:
    """Test the database connection."""
    try:
        with session() as database_session:
            query = text("SELECT 1")
            database_session.execute(query)
            database_session.commit()
        return True
    except Exception as error:
        raise ValueError("Database connection error") from error


def get_database_session():
    """Return a database session."""
    try:
        database_session = session()
        yield database_session
    finally:
        database_session.close()
