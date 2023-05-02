from typing import Literal

from pydantic import BaseModel, Field, root_validator

from api.environment import env


class SettingsAuth(BaseModel):
    """Settings model."""

    jwt_key: str = Field(title="JWT key", description="JWT key", default=env.jwt_key)
    jwt_algorithm: str = Field(title="JWT algorithm", description="JWT algorithm", default="HS256")
    jwt_expiration: int = Field(title="JWT expiration time in minutes", description="JWT expiration time in minutes", default=60)
    jwt_refresh_every: int = Field(title="JWT refresh every in minutes", description="JWT refresh every in minutes", default=30)
    jwt_max_refresh: int = Field(title="JWT max refresh in minutes", description="JWT max refresh in minutes", default=300)
    jwt_bad_store: Literal["memory", "cache", "database"] = Field(title="JWT bad store", description="JWT bad store", default="memory")
    block_user_after_fail_attempts: int = Field(title="Block user after fail attempts", description="Block user after fail attempts, if 0 disabled", default=5)

    @root_validator
    def jwt_expiration_validator(cls, v):  # pylint: disable=E0213
        """Validate JWT expiration."""
        if v["jwt_expiration"] < 0:
            raise ValueError("jwt_expiration must be greater than or equal to 0")
        if v["jwt_key"] == "":
            raise ValueError("jwt_key must not be empty")
        if v["jwt_algorithm"] == "":
            raise ValueError("jwt_algorithm must not be empty")
        if v["jwt_bad_store"] == "":
            raise ValueError("jwt_bad_store must not be empty")
        if v["block_user_after_fail_attempts"] < 0:
            raise ValueError("block_user_after_fail_attempts must be greater than or equal to 0")
        return v

    class Config:  # pylint: disable=too-few-public-methods
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True
