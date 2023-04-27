"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
Base = declarative_base()