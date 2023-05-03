from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Entity Model."""

    name: str = Field(alias="alias", example="db")
    status: str = Field(alias="status", example="Healthy")
    timeTaken: str = Field(alias="timeTaken", example="0:00:00.009619")
    details: dict[str, str] | None = Field(alias="details", example={"version": "1.0.0"})


class HealthCheck(BaseModel):
    """Health Check Entity Model."""

    status: str = Field(alias="status", example="Healthy")
    timeTaken: str = Field(alias="timeTaken", example="0:00:00.009619")
    details: dict[str, str] | None = Field(alias="details", example={"version": "1.0.0"})
    entities: list[Entity] = Field(alias="entities", example=[Entity(alias="db", status="Healthy", timeTaken="0:00:00.009619", details={"version": "1.0.0"})])
