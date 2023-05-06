"""General API dependencies."""
from math import ceil
from typing import Annotated, Any, List

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.core.database import BaseModelORM, session
from api.core.utils import HashHandler, RandomGenerator
from api.settings.schema import SettingsGlobal
from api.users.schema import UserOut


def get_database_session():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()


def get_settings():
    """Dependency to get global settings."""
    settings = SettingsGlobal()
    if settings.load() is False:
        settings.save()
    return settings


class QueryBase(BaseModel):
    """Common query parameters schema."""

    page: int | None = Query(
        default=1, title="Page number", description="Page number to return.", gt=0
    )
    records: int | None = Query(
        default=100,
        title="Records per page",
        description="Number of records to return.",
        gt=0,
        le=get_settings().api.page_size_max,
    )


class PageBase(BaseModel):
    """Page Base Model"""

    records: List[Any]
    query: QueryBase
    total_pages: int
    total_records: int


class PageUserOut(PageBase):
    """Page of UserOut."""

    records: List[UserOut]


def query_executor(orm_model, query: QueryBase, model):
    """Do SQL Alchmy queries."""
    # validate if the orm_model is known.
    if orm_model not in BaseModelORM.__subclasses__():
        raise ValueError(f"orm_model {orm_model} is unknown.")
    # Run Query
    with session() as database:
        total_records = database.query(orm_model).count()
        total_pages = ceil(total_records / query.records)
        records_database = (
            database.query(orm_model).offset((query.page) - 1).limit(query.records).all()
        )
        # Convert to Pydantic Model
        records: List[model] = [model.from_orm(record) for record in records_database]
        return PageUserOut(
            records=records,
            query=QueryBase(page=query.page, records=query.records),
            total_pages=total_pages,
            total_records=total_records,
        )


Database = Annotated[Session, Depends(get_database_session)]
Settings = Annotated[SettingsGlobal, Depends(get_settings)]
QueryParameters = Annotated[QueryBase, Depends()]
HashManager = Annotated[HashHandler, Depends()]
Generator = Annotated[RandomGenerator, Depends()]
