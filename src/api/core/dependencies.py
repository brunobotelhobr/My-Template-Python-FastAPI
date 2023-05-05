"""General API dependencies."""
from typing import Annotated

from fastapi import Depends, Query, RawParams
from pydantic import BaseModel, root_validator
from sqlalchemy.orm import Session

from api.core.database import session
from api.core.utils import HashHandler, RandomGenerator
from api.settings.schema import SettingsModel
from api.settings.utils import global_settings


def get_database_session():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()


def get_settings():
    """Dependency to get global settings."""
    return global_settings


class CommonQueryParameters(BaseModel):
    """Common query parameters schema."""

    skip: int | None = Query(0, title="Page number", description="Page number")
    limit: int | None = Query(1000, title="Page size", description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )
    
    @root_validator
    def validate_skip(cls, values):
        """Validate skip parameter."""
        if values["skip"] < 0:
            raise ValueError("Skip parameter must be greater than 0")
        if values["skip"] > get_settings().api.page_size_max:
            raise ValueError(
                f"Skip parameter must be less than {get_settings().api.page_size_max}."
            )
        return values


Database = Annotated[Session, Depends(get_database_session)]
Settings = Annotated[SettingsModel, Depends(get_settings)]
QueryParameters = Annotated[dict, Depends(CommonQueryParameters)]
HashManager = Annotated[HashHandler, Depends()]
Generator = Annotated[RandomGenerator, Depends()]
