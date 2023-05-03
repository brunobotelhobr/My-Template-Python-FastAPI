from pydantic import BaseModel, Field


class SimpleMessage(BaseModel):
    """Simple message model."""

    status: str = Field(example="OK", title="Status", description="Status message")
