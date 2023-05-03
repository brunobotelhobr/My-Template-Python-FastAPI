"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.environment import db, env


# Create the engine
def create_local_engine():
    """Create the database engine."""
    if db.url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        return create_engine(db.url, echo=env.local.is_debug, connect_args=connect_args)
    return create_engine(db.url, echo=True)


# Spawn the engine
engine = create_local_engine()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all the database models."""  # pylint: disable=too-few-public-methods

    pass  # pylint: disable=unnecessary-pass


def init_db() -> bool:
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
    return True


def get_db():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()
