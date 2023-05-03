from typing import Literal

from pydantic import BaseModel, Field, root_validator

from api.environment import env


class SettingsAuth(BaseModel):
    """Settings model."""

    jwt_key: str = Field(title="JWT key", description="JWT key", default=env.jwt_key)
    jwt_algorithm: str = Field(title="JWT algorithm", description="JWT algorithm", default="HS256")
    jwt_expiration_initial: int = Field(title="JWT initial expiration in minutes", description="Initial duration for a JWT", default=30)
    jwt_expiration_step: int = Field(title="JWT increment in minutes", description="JWT increment in minutes", default=30)
    jwt_expiration_max: int = Field(title="JWT max expiration in minutes", description="JWT max expiration in minutes", default=120)
    jwt_revokes_store: Literal["memory", "cache", "database"] = Field(title="JWT revoked store", description="JWT revoked store", default="memory")
    block_user_after_fail_attempts: int = Field(title="Block user after fail attempts", description="Block user after fail attempts, if 0 disabled", default=5)

    @root_validator
    def jwt_expiration_validator(cls, v):  # pylint: disable=E0213
        """Validate JWT expiration."""
        if v["jwt_expiration_initial"] < 1:
            raise ValueError("JWT expiration initial must be greater than 0.")
        if v["jwt_expiration_step"] < 0:
            raise ValueError("JWT expiration step must be greater than or equal to 0.")
        if v["jwt_expiration_max"] < 1:
            raise ValueError("JWT expiration max must be greater than 0.")
        if v["jwt_expiration_initial"] > v["jwt_expiration_max"]:
            raise ValueError("JWT expiration initial must be less than JWT expiration max.")
        if v["jwt_expiration_step"] + v["jwt_expiration_initial"] > v["jwt_expiration_max"]:
            raise ValueError("JWT expiration step plus JWT expiration initial must be less than JWT expiration max.")
        return v

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True