"""Core Schema."""
from pydantic import BaseModel, Field


class SimpleMessage(BaseModel):
    """Simple message model."""

    status: str = Field(example="OK", title="Status", description="Status message")


class Singleton:
    """Singgleton implementation."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create a singleton instance of the settings."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
