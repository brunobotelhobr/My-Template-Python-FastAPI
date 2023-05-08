"""JWT settings."""
from typing import Literal

from pydantic import BaseModel, Field, root_validator

from api.core.model import Singleton


class JWTSettings(BaseModel):
    """JWT Settings."""

    jwt_algorithm: str = Field(
        title="JWT algorithm", description="JWT algorithm", default="HS256"
    )
    jwt_expiration_initial: int = Field(
        title="JWT initial expiration in minutes",
        description="Initial duration for a JWT",
        default=30,
    )
    jwt_expiration_step: int = Field(
        title="JWT increment in minutes",
        description="JWT increment in minutes",
        default=30,
    )
    jwt_expiration_max: int = Field(
        title="JWT max expiration in minutes",
        description="JWT max expiration in minutes",
        default=120,
    )
    jwt_revokes_store: Literal["memory", "cache", "database"] = Field(
        title="JWT revoked store", description="JWT revoked store", default="memory"
    )
    block_user_after_fail_attempts: int = Field(
        title="Block user after fail attempts",
        description="Block user after fail attempts, if 0 disabled",
        default=5,
    )

    @root_validator
    def jwt_expiration_validator(cls, values):  # pylint: disable=E0213
        """Validate JWT expiration."""
        if values["jwt_expiration_initial"] < 1:
            raise ValueError("JWT expiration initial must be greater than 0.")
        if values["jwt_expiration_step"] < 0:
            raise ValueError("JWT expiration step must be greater than or equal to 0.")
        if values["jwt_expiration_max"] < 1:
            raise ValueError("JWT expiration max must be greater than 0.")
        if values["jwt_expiration_initial"] > values["jwt_expiration_max"]:
            raise ValueError(
                "JWT expiration initial must be less than JWT expiration max."
            )
        if (
            values["jwt_expiration_step"] + values["jwt_expiration_initial"]
            > values["jwt_expiration_max"]
        ):
            raise ValueError(
                "JWT expiration step plus JWT expiration initial must be less than JWT expiration max."
            )
        return values

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class RunningJWTSettings(JWTSettings, Singleton):
    """Running JWT Settings."""
